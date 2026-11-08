# AthleteHub – lokale startinstallatie

Dit is versie 0.1: een lokale Docker-basis met PostgreSQL, n8n, FastAPI en een eenvoudige website.

## Vereisten
- Windows 10/11
- Docker Desktop met WSL2-backend
- Minstens 8 GB vrij RAM aanbevolen voor deze basisinstallatie
- Een browser

Ollama/lokale AI is bewust nog niet opgenomen. Met 16 GB RAM is het verstandiger eerst de gegevensstroom werkend te krijgen en daarna een klein model te testen.

## 1. Configuratie
1. Open PowerShell in deze map.
2. Kopieer `.env.example` naar `.env`:
   `Copy-Item .env.example .env`
3. Genereer twee aparte geheimen:
   `python -c "import secrets; print(secrets.token_urlsafe(32))"`
4. Vervang `DB_PASSWORD` en `N8N_ENCRYPTION_KEY` in `.env`.
   Gebruik voor DB_PASSWORD bij voorkeur letters en cijfers om URL-encodingproblemen te vermijden.
5. Bewaar `.env` privé en commit dit bestand nooit naar Git.

## 2. Starten
In PowerShell, vanuit de AthleteHub-map:

```powershell
docker compose up -d --build
docker compose ps
docker compose logs -f api
```

Open:
- Website: http://localhost:8080
- n8n: http://localhost:5678
- API-documentatie: http://localhost:8080/api/docs
- API-health: http://localhost:8080/api/health

Bij de eerste start maakt de API automatisch de tabel aan.

## 3. Testactiviteit toevoegen
Voer dit uit in PowerShell:

```powershell
$body = @{
  source = "test"
  sport = "Cycling"
  started_at = "2026-11-06T18:00:00+01:00"
  duration_seconds = 3600
  distance_meters = 25000
  average_heart_rate = 140
  average_power = 165
  notes = "Voorbeeldactiviteit"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri "http://localhost:8080/api/activities" `
  -ContentType "application/json" `
  -Body $body
```

Vernieuw daarna http://localhost:8080.

## 4. Stoppen en opnieuw starten
```powershell
docker compose down
```
Data blijft bewaard in Docker-volumes.

Opnieuw starten:
```powershell
docker compose up -d
```

Om ook alle opgeslagen data te verwijderen (LET OP: onomkeerbaar):
```powershell
docker compose down -v
```

## 5. Belangrijke grenzen van versie 0.1
- De website en database werken, en de API kan activiteiten opslaan en tonen.
- n8n draait, maar er zijn nog geen workflows geïmporteerd.
- MyWhoosh, Strava, Intervals.icu en OnePlus zijn nog niet gekoppeld.
- Voeg pas echte koppelingen toe nadat de API-sleutels en toegangsrechten gecontroleerd zijn.
- Deze installatie is uitsluitend bedoeld voor lokaal gebruik. Zet poorten niet open naar het internet.
- Maak regelmatig back-ups van de database.

## 6. Volgende ontwikkelstap
Koppel eerst Intervals.icu aan de backend, haal activiteiten op via de officiële API en sla ze op met een stabiele `external_id`. Daarna kan n8n periodiek de synchronisatie starten.
