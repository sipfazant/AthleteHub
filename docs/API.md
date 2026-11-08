# API-documentatie

## Technologie
De backend gebruikt FastAPI en is intern bereikbaar op poort 8000.

Via Nginx zijn de API-endpoints beschikbaar onder `/api/`.

API-documentatie:
http://localhost:8080/api/docs

## Authenticatie

| Methode | Endpoint | Functie |
|---|---|---|
| POST | /auth/setup | Eerste account aanmaken |
| POST | /auth/login | Aanmelden |
| GET | /auth/me | Huidige gebruiker |
| PUT | /auth/account | Accountgegevens wijzigen |
| POST | /auth/logout | Uitloggen |

## Activiteiten

| Methode | Endpoint | Functie |
|---|---|---|
| GET | /activities | Activiteiten ophalen |
| POST | /activities | Activiteit opslaan |
| GET | /stats | Trainingsstatistieken |

## Healthcheck

| Methode | Endpoint | Functie |
|---|---|---|
| GET | /health | Backend en database controleren |

Via Nginx:
http://localhost:8080/api/health

## Authenticatiebeveiliging
- Sessiecookies worden gebruikt.
- Sessietokens worden gehasht opgeslagen.
- Wachtwoorden worden gehasht met Argon2.
- Sessies verlopen na 14 dagen.
- Beschermde endpoints gebruiken de authenticatieafhankelijkheid van FastAPI.

## Belangrijk
Controleer altijd de actuele backendcode voordat endpoints worden gewijzigd of toegevoegd.

Deze documentatie moet worden bijgewerkt wanneer API-endpoints veranderen.
