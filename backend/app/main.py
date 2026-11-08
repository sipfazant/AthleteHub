
import os
import hashlib
import secrets

from datetime import datetime, timedelta, timezone
from typing import Optional

import psycopg
from psycopg.rows import dict_row

from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError,
)

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Response,
    Depends,
    Cookie,
)

from pydantic import BaseModel, Field


DATABASE_URL = os.environ["DATABASE_URL"]

COOKIE_NAME = "athletehub_session"
SESSION_DAYS = 14
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"

password_hasher = PasswordHasher()

app = FastAPI(
    title="AthleteHub API",
    version="0.2.0"
)


def connect():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_session(account_id: int, request: Request, response: Response):
    token = secrets.token_urlsafe(32)
    token_hash = hash_token(token)

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=SESSION_DAYS
    )

    with connect() as conn:
        conn.execute("""
            INSERT INTO athletehub.auth_sessions
            (account_id, token_hash, expires_at, user_agent)
            VALUES (%s, %s, %s, %s)
        """, (
            account_id,
            token_hash,
            expires_at,
            request.headers.get("user-agent")
        ))

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        max_age=SESSION_DAYS * 86400,
        path="/"
    )


def get_current_account(
    request: Request,
    token: Optional[str] = Cookie(default=None, alias=COOKIE_NAME)
):
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Niet aangemeld."
        )

    token_hash = hash_token(token)
    now = datetime.now(timezone.utc)

    with connect() as conn:
        session = conn.execute("""
            SELECT
                s.account_id,
                a.email,
                a.is_active
            FROM athletehub.auth_sessions s
            JOIN athletehub.app_account a
                ON a.id = s.account_id
            WHERE s.token_hash = %s
              AND s.revoked_at IS NULL
              AND s.expires_at > %s
        """, (token_hash, now)).fetchone()

        if not session or not session["is_active"]:
            raise HTTPException(
                status_code=401,
                detail="Sessie ongeldig of verlopen."
            )

        conn.execute("""
            UPDATE athletehub.auth_sessions
            SET last_used_at = NOW()
            WHERE token_hash = %s
        """, (token_hash,))

    return session


class SetupInput(BaseModel):
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=12, max_length=128)


class LoginInput(BaseModel):
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=1, max_length=128)

class AccountUpdateInput(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_email: Optional[str] = Field(default=None, min_length=5, max_length=254)
    new_password: Optional[str] = Field(default=None, min_length=12, max_length=128)


class ActivityIn(BaseModel):
    external_id: Optional[str] = None
    source: str = Field(default="manual", max_length=80)
    sport: str = Field(min_length=1, max_length=40)
    started_at: datetime
    duration_seconds: int = Field(ge=0)
    distance_meters: Optional[float] = Field(default=None, ge=0)
    average_heart_rate: Optional[int] = Field(default=None, ge=1, le=250)
    average_power: Optional[int] = Field(default=None, ge=0)
    notes: Optional[str] = None


@app.on_event("startup")
def init_db():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS athletehub.activities (
                id BIGSERIAL PRIMARY KEY,
                external_id TEXT UNIQUE,
                source TEXT NOT NULL DEFAULT 'manual',
                sport TEXT NOT NULL,
                started_at TIMESTAMPTZ NOT NULL,
                duration_seconds INTEGER NOT NULL
                    CHECK (duration_seconds >= 0),
                distance_meters DOUBLE PRECISION,
                average_heart_rate INTEGER,
                average_power INTEGER,
                notes TEXT,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_activities_started_at
            ON athletehub.activities(started_at DESC)
        """)


# EENMALIGE ACCOUNTINITIALISATIE

@app.post("/auth/setup", status_code=201)
def setup_account(data: SetupInput):
    email = data.email.strip().lower()

    if "@" not in email:
        raise HTTPException(400, "Ongeldig e-mailadres.")

    password_hash = password_hasher.hash(data.password)

    try:
        with connect() as conn:
            existing = conn.execute("""
                SELECT COUNT(*) AS total
                FROM athletehub.app_account
            """).fetchone()

            if existing["total"] > 0:
                raise HTTPException(
                    status_code=403,
                    detail="Account is al geïnitialiseerd."
                )

            account = conn.execute("""
                INSERT INTO athletehub.app_account
                    (email, password_hash)
                VALUES (%s, %s)
                RETURNING id, email
            """, (email, password_hash)).fetchone()

            conn.execute("""
                INSERT INTO athletehub.athlete_profile (id)
                VALUES (%s)
                ON CONFLICT (id) DO NOTHING
            """, (account["id"],))

            conn.execute("""
                INSERT INTO athletehub.user_preferences (id)
                VALUES (%s)
                ON CONFLICT (id) DO NOTHING
            """, (account["id"],))

        return {
            "status": "created",
            "email": account["email"]
        }

    except HTTPException:
        raise
    except psycopg.Error as exc:
        raise HTTPException(
            400,
            "Account kon niet worden aangemaakt."
        ) from exc


# LOGIN

@app.post("/auth/login")
def login(
    data: LoginInput,
    request: Request,
    response: Response
):
    email = data.email.strip().lower()

    with connect() as conn:
        account = conn.execute("""
            SELECT id, email, password_hash, is_active
            FROM athletehub.app_account
            WHERE email = %s
        """, (email,)).fetchone()

    if not account or not account["is_active"]:
        raise HTTPException(401, "Ongeldige inloggegevens.")

    try:
        password_hasher.verify(
            account["password_hash"],
            data.password
        )
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        raise HTTPException(401, "Ongeldige inloggegevens.")

    if password_hasher.check_needs_rehash(account["password_hash"]):
        new_hash = password_hasher.hash(data.password)

        with connect() as conn:
            conn.execute("""
                UPDATE athletehub.app_account
                SET password_hash = %s,
                    updated_at = NOW()
                WHERE id = %s
            """, (new_hash, account["id"]))

    with connect() as conn:
        conn.execute("""
            UPDATE athletehub.app_account
            SET last_login_at = NOW()
            WHERE id = %s
        """, (account["id"],))

    create_session(account["id"], request, response)

    return {
        "status": "authenticated",
        "email": account["email"]
    }


# HUIDIGE GEBRUIKER

@app.get("/auth/me")
def current_user(
    account=Depends(get_current_account)
):
    with connect() as conn:
        profile = conn.execute("""
            SELECT display_name, timezone, preferred_units
            FROM athletehub.athlete_profile
            WHERE id = %s
        """, (account["account_id"],)).fetchone()

    return {
        "id": account["account_id"],
        "email": account["email"],
        "profile": profile
    }

# ACCOUNTINSTELLINGEN

@app.put("/auth/account")
def update_account(
    data: AccountUpdateInput,
    request: Request,
    response: Response,
    account=Depends(get_current_account)
):
    new_email = (
        data.new_email.strip().lower()
        if data.new_email
        else account["email"]
    )

    if data.new_email and "@" not in new_email:
        raise HTTPException(400, "Ongeldig e-mailadres.")

    if not data.new_email and not data.new_password:
        raise HTTPException(
            400,
            "Geef een nieuw e-mailadres of wachtwoord op."
        )

    with connect() as conn:
        current = conn.execute("""
            SELECT password_hash
            FROM athletehub.app_account
            WHERE id = %s
        """, (account["account_id"],)).fetchone()

        if not current:
            raise HTTPException(404, "Account niet gevonden.")

        try:
            password_hasher.verify(
                current["password_hash"],
                data.current_password
            )
        except (
            VerifyMismatchError,
            VerificationError,
            InvalidHashError
        ):
            raise HTTPException(
                401,
                "Het huidige wachtwoord is onjuist."
            )

        new_hash = (
            password_hasher.hash(data.new_password)
            if data.new_password
            else current["password_hash"]
        )

        try:
            conn.execute("""
                UPDATE athletehub.app_account
                SET email = %s,
                    password_hash = %s,
                    updated_at = NOW()
                WHERE id = %s
            """, (
                new_email,
                new_hash,
                account["account_id"]
            ))

            conn.execute("""
                UPDATE athletehub.auth_sessions
                SET revoked_at = NOW()
                WHERE account_id = %s
                  AND revoked_at IS NULL
            """, (account["account_id"],))

        except psycopg.errors.UniqueViolation:
            raise HTTPException(
                409,
                "Dit e-mailadres is al in gebruik."
            )

    create_session(
        account["account_id"],
        request,
        response
    )

    return {
        "status": "updated",
        "email": new_email
    }


# LOGOUT

@app.post("/auth/logout")
def logout(
    response: Response,
    token: Optional[str] = Cookie(
        default=None,
        alias=COOKIE_NAME
    )
):
    if token:
        with connect() as conn:
            conn.execute("""
                UPDATE athletehub.auth_sessions
                SET revoked_at = NOW()
                WHERE token_hash = %s
                  AND revoked_at IS NULL
            """, (hash_token(token),))

    response.delete_cookie(
        key=COOKIE_NAME,
        path="/",
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax"
    )

    return {"status": "logged_out"}


# HEALTH

@app.get("/health")
def health():
    try:
        with connect() as conn:
            conn.execute("SELECT 1")

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception as exc:
        raise HTTPException(
            503,
            "Database unavailable"
        ) from exc


# ACTIVITEITEN

@app.get("/activities")
def list_activities(
    limit: int = 50,
    account=Depends(get_current_account)
):
    limit = max(1, min(limit, 200))

    with connect() as conn:
        rows = conn.execute("""
            SELECT *
            FROM athletehub.activities
            ORDER BY started_at DESC
            LIMIT %s
        """, (limit,)).fetchall()

    return rows


@app.post("/activities", status_code=201)
def create_activity(
    activity: ActivityIn,
    account=Depends(get_current_account)
):
    started_at = activity.started_at

    if started_at.tzinfo is None:
        started_at = started_at.replace(
            tzinfo=timezone.utc
        )

    values = activity.model_dump()
    values["started_at"] = started_at

    try:
        with connect() as conn:
            row = conn.execute("""
                INSERT INTO athletehub.activities
                (
                    external_id, source, sport, started_at,
                    duration_seconds, distance_meters,
                    average_heart_rate, average_power, notes
                )
                VALUES (
                    %(external_id)s, %(source)s, %(sport)s,
                    %(started_at)s, %(duration_seconds)s,
                    %(distance_meters)s, %(average_heart_rate)s,
                    %(average_power)s, %(notes)s
                )
                ON CONFLICT (external_id) DO UPDATE SET
                    source = EXCLUDED.source,
                    sport = EXCLUDED.sport,
                    started_at = EXCLUDED.started_at,
                    duration_seconds = EXCLUDED.duration_seconds,
                    distance_meters = EXCLUDED.distance_meters,
                    average_heart_rate = EXCLUDED.average_heart_rate,
                    average_power = EXCLUDED.average_power,
                    notes = EXCLUDED.notes
                RETURNING *
            """, values).fetchone()

        return row

    except psycopg.Error as exc:
        raise HTTPException(
            400,
            "Activiteit kon niet worden opgeslagen."
        ) from exc


@app.get("/stats")
def stats(account=Depends(get_current_account)):
    with connect() as conn:
        row = conn.execute("""
            SELECT
                COUNT(*) AS activity_count,
                COALESCE(SUM(duration_seconds), 0) AS total_seconds,
                COALESCE(SUM(distance_meters), 0)
                    AS total_distance_meters
            FROM athletehub.activities
        """).fetchone()

    return row
