# Docker-documentatie

## Vereisten
- Windows 10/11
- Docker Desktop
- WSL2
- PowerShell

## Containers starten

```powershell
docker compose up -d
```

## Containers opnieuw bouwen

```powershell
docker compose up -d --build
```

## Status bekijken

```powershell
docker compose ps
```

## Logs bekijken

```powershell
docker compose logs -f
```

Voor de API:

```powershell
docker compose logs -f api
```

Voor PostgreSQL:

```powershell
docker compose logs -f postgres
```

## Containers stoppen

```powershell
docker compose down
```

## Volumes

De applicatie gebruikt onder andere:
- postgres_data
- n8n_data
- sandbox-tls

Deze volumes bewaren gegevens buiten de levenscyclus van de containers.

**Waarschuwing:** `docker compose down -v` verwijdert ook de gekoppelde volumes. Gebruik dit niet zonder een gecontroleerde back-up.

## Configuratie

Docker Compose gebruikt omgevingsvariabelen uit `.env`.

Gevoelige waarden mogen nooit in Git worden opgeslagen.

## Controle

Bij problemen:
1. Controleer `docker compose ps`.
2. Controleer de logs van de betrokken service.
3. Controleer de omgevingsvariabelen zonder geheimen te delen.
4. Controleer netwerkverbindingen tussen containers.
5. Wijzig niet onnodig bestaande volumes of databases.
