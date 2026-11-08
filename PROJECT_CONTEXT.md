# AthleteHub

**AthleteHub** is een persoonlijk sportplatform waarmee sportactiviteiten, trainingsgegevens en accountinformatie centraal beheerd kunnen worden. Het project draait lokaal via Docker en gebruikt een eigen backend, PostgreSQL-database en webinterface.

## Projectstatus

| Onderdeel | Technologie | Status |
|---|---|---|
| Frontend | HTML, CSS, JavaScript | In ontwikkeling |
| Backend | Python, FastAPI | Actief |
| Database | PostgreSQL 17 | Actief |
| Authenticatie | FastAPI, Argon2, sessiecookies | Actief |
| Automatisering | n8n 2.46.6 | Geïnstalleerd |
| Web search | SearXNG | Geïnstalleerd |
| n8n sandbox | n8n Sandbox Service | Geconfigureerd |
| AI Trainer | n8n, Ollama | In ontwikkeling |
| Sportplatformintegraties | Externe API's | In voorbereiding |

## Architectuur

AthleteHub bestaat uit verschillende Docker-services die samenwerken via een intern Docker-netwerk.

```text
                 Gebruiker
                     |
                     v
              Webinterface
              localhost:8080
                     |
                     v
                 Nginx
                     |
                     v
               FastAPI
              localhost:8000
                     |
                     v
               PostgreSQL
                     |
          +----------+----------+
          |                     |
          v                     v
         n8n                 Database
      localhost:5678
          |
          +----------+
          |          |
          v          v
       SearXNG    AI Trainer
      :8888       Ollama
```

### Docker-services

| Service | Functie | Lokale poort |
|---|---|---|
| `web` | Webinterface via Nginx | 8080 |
| `api` | FastAPI-backend | 8000 |
| `postgres` | PostgreSQL-database | Intern |
| `n8n` | Workflows en automatisering | 5678 |
| `searxng` | Zelfgehoste zoekmachine | 8888 |
| `sandbox-api` | n8n sandbox API | Intern |
| `sandbox-runner-1` | Sandbox runner | Intern |
| `sandbox-certs` | TLS-certificaten voor sandbox | Intern |

## Vereisten

- Windows 10/11
- Docker Desktop met WSL2
- PowerShell
- Git
- Een moderne webbrowser
- Voldoende RAM voor de Docker-services en eventuele lokale AI-modellen

## Installatie

### 1. Repository ophalen

```powershell
git clone https://github.com/sipfazant/AthleteHub.git
cd AthleteHub
```

### 2. Omgevingsvariabelen configureren

Maak in de hoofdmap een `.env`-bestand aan.

De Docker-configuratie gebruikt onder andere deze variabelen:

```env
DB_USER=athletehub
DB_PASSWORD=

N8N_ENCRYPTION_KEY=

SEARXNG_SECRET=
N8N_INSTANCE_AI_SEARXNG_URL=http://searxng:8080

N8N_SANDBOX_VERSION=

SANDBOX_API_KEYS=
SANDBOX_RUNNER_REGISTRATION_TOKEN=
SANDBOX_API_RUNNER_API_KEY=
```

Vul alle vereiste waarden in voordat je de containers start.

Gebruik sterke, willekeurig gegenereerde geheimen. Bewaar het `.env`-bestand privé.

**Belangrijk:** commit nooit `.env`-bestanden, wachtwoorden, API-sleutels of andere toegangsgegevens naar GitHub.

### 3. Docker starten

Voer vanuit de hoofdmap uit:

```powershell
docker compose up -d --build
```

Controleer vervolgens de containers:

```powershell
docker compose ps
```

Bekijk de logs van de backend:

```powershell
docker compose logs -f api
```

### 4. Applicaties openen

| Applicatie | URL |
|---|---|
| AthleteHub | http://localhost:8080 |
| FastAPI-documentatie | http://localhost:8080/api/docs |
| API-healthcheck | http://localhost:8080/api/health |
| n8n | http://localhost:5678 |
| SearXNG | http://localhost:8888 |

## Backend

De backend is ontwikkeld met FastAPI en gebruikt PostgreSQL voor gegevensopslag.

### Authenticatie

AthleteHub gebruikt een eigen accountsysteem.

Belangrijke eigenschappen:

- Eenmalige accountinitialisatie.
- Aanmelden met e-mailadres en wachtwoord.
- Wachtwoordhashing met Argon2.
- Sessies via beveiligde HTTP-cookies.
- Sessieverval na 14 dagen.
- Accountgegevens wijzigen.
- Uitloggen en sessies intrekken.

### Beschikbare API-endpoints

| Methode | Endpoint | Functie |
|---|---|---|
| POST | `/auth/setup` | Eerste account aanmaken |
| POST | `/auth/login` | Aanmelden |
| GET | `/auth/me` | Huidige gebruiker ophalen |
| PUT | `/auth/account` | Accountgegevens wijzigen |
| POST | `/auth/logout` | Uitloggen |
| GET | `/health` | Backend en database controleren |
| GET | `/activities` | Activiteiten ophalen |
| POST | `/activities` | Activiteit opslaan |
| GET | `/stats` | Trainingsstatistieken ophalen |

De endpoints zijn via Nginx beschikbaar onder `/api/`.

### Accountinitialisatie

Het eerste account wordt aangemaakt via:

```http
POST /api/auth/setup
```

Voorbeeld:

```json
{
  "email": "jouw@email.be",
  "password": "EenSterkWachtwoord123!"
}
```

De accountinitialisatie kan slechts één keer uitgevoerd worden zolang er al een account bestaat.

## Database

AthleteHub gebruikt PostgreSQL 17.

De applicatie gebruikt onder andere het schema `athletehub`. n8n gebruikt een afzonderlijk databaseschema.

De database bevat gegevens voor onder andere:

- Gebruikersaccounts.
- Authenticatiesessies.
- Sportactiviteiten.
- Atleetprofielen.
- Gebruikersvoorkeuren.
- AI-gesprekken en berichten.

De backend maakt de tabel `activities` en de bijbehorende index automatisch aan bij het opstarten.

Andere tabellen worden beheerd via de bestaande databasestructuur.

## AI Trainer en automatisering

AthleteHub bevat een n8n-omgeving voor automatisering en AI-functionaliteit.

De beoogde AI Trainer moet onder andere kunnen helpen met:

- Trainingsschema's.
- Hardloop- en fietstraining.
- Analyse van sportactiviteiten.
- Trainingsbelasting en herstel.
- Interpretatie van sportgegevens.
- Algemene sport- en conditievragen.

De AI-functionaliteit wordt ontwikkeld met n8n en een lokaal AI-model via Ollama.

De uiteindelijke architectuur voorziet dat FastAPI gebruikersauthenticatie en opslag van gesprekken beheert, terwijl n8n de AI-workflow uitvoert.

De volledige koppeling tussen de AthleteHub-backend en de n8n-workflow wordt afzonderlijk ontwikkeld.

## Frontend

De frontend bestaat uit:

- HTML5.
- CSS3.
- JavaScript.
- Nginx als webserver en reverse proxy.

De huidige interface bevat:

- Aanmeldscherm.
- Persoonlijk dashboard.
- Activiteitenoverzicht.
- Trainingsstatistieken.
- Accountinstellingen.
- E-mailadres en wachtwoord wijzigen.
- Uitloggen.

## Sportplatformintegraties

AthleteHub wordt voorbereid op koppelingen met externe sportplatformen.

Mogelijke integraties zijn:

- Strava.
- Intervals.icu.
- MyWhoosh.
- Garmin.
- OnePlus/OHealth.

Deze koppelingen moeten via officiële API's of ondersteunde integratiemethoden worden uitgewerkt.

## Docker-beheer

### Containers starten

```powershell
docker compose up -d
```

### Containers opnieuw bouwen

```powershell
docker compose up -d --build
```

### Status controleren

```powershell
docker compose ps
```

### Logs bekijken

```powershell
docker compose logs -f
```

Voor één specifieke service:

```powershell
docker compose logs -f api
```

### Containers stoppen

```powershell
docker compose down
```

De gegevens in de Docker-volumes blijven behouden.

### Volledige verwijdering

```powershell
docker compose down -v
```

**Waarschuwing:** hiermee worden ook de gekoppelde Docker-volumes verwijderd. Databasegegevens en n8n-data kunnen daardoor verloren gaan.

## Back-ups

Maak regelmatig back-ups van de PostgreSQL-database en belangrijke configuratiebestanden.

Bewaar back-ups en gevoelige configuratie buiten de publieke GitHub-repository.

## Beveiliging

AthleteHub is momenteel bedoeld voor lokaal gebruik.

- Stel de applicatie niet zomaar publiek beschikbaar.
- Bewaar geheimen uitsluitend in `.env`.
- Gebruik sterke wachtwoorden en API-sleutels.
- Commit nooit gevoelige gegevens naar GitHub.
- Maak regelmatig back-ups.
- Controleer netwerk- en firewallinstellingen voordat externe toegang wordt ingeschakeld.

## Ontwikkeling

De broncode staat op GitHub:

https://github.com/sipfazant/AthleteHub

De hoofdbranch is `main`.

### Wijzigingen ophalen

```powershell
git pull origin main
```

### Wijzigingen controleren

```powershell
git status
```

### Wijzigingen publiceren

```powershell
git add .
git commit -m "Beschrijving van de wijziging"
git push origin main
```

Controleer vóór het committen altijd of er geen wachtwoorden, tokens, `.env`-bestanden of andere gevoelige gegevens worden toegevoegd.

---

**AthleteHub — persoonlijk sportplatform in ontwikkeling.**