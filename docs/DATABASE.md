# Database

## Technologie
AthleteHub gebruikt PostgreSQL 17.

Database:
- Naam: athletehub
- Applicatieschema: athletehub
- n8n-schema: n8n

## Verbinding

De FastAPI-backend gebruikt de omgevingsvariabele DATABASE_URL.

De backend maakt verbinding met PostgreSQL via psycopg.

## Bekende tabellen

De volgende tabellen zijn in de huidige projectontwikkeling gebruikt of vastgesteld:

| Tabel | Doel |
|---|---|
| app_account | Gebruikersaccount |
| auth_sessions | Authenticatiesessies |
| athlete_profile | Atleetprofiel |
| user_preferences | Gebruikersvoorkeuren |
| activities | Sportactiviteiten |
| ai_conversations | AI-gesprekken |
| ai_messages | Berichten binnen AI-gesprekken |

De precieze kolommen en relaties moeten worden gecontroleerd aan de hand van het actuele SQL-schema.

n8n gebruikt een afzonderlijk databaseschema.

## Activiteiten

De backend maakt de tabel `athletehub.activities` automatisch aan bij het opstarten als deze nog niet bestaat.

Bekende velden:
- id
- external_id
- source
- sport
- started_at
- duration_seconds
- distance_meters
- average_heart_rate
- average_power
- notes
- created_at

## Databasebeheer

Wijzigingen aan de databasestructuur moeten gecontroleerd en gedocumenteerd worden.

Voer nooit zomaar `docker compose down -v` uit. Hiermee kunnen databasegegevens en andere opgeslagen gegevens verloren gaan.

## Nog te documenteren
- Volledige tabelstructuur
- Foreign keys en relaties
- Indexen
- Constraints
- Migratiestrategie
- Back-up- en herstelprocedure
