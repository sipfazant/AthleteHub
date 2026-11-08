# Architectuur

## Overzicht

AthleteHub bestaat uit meerdere Docker-services die samenwerken via het interne Docker-netwerk.

```text
Browser
   |
   v
Nginx / Frontend
   |
   v
FastAPI Backend
   |
   v
PostgreSQL

n8n ---- SearXNG
 |
 AI Agent
 |
 Ollama
```

## Docker-services

| Service | Functie | Poort |
|---|---|---|
| web | Frontend via Nginx | 8080 |
| api | FastAPI | 8000 |
| postgres | PostgreSQL 17 | Intern |
| n8n | Workflows en automatisering | 5678 |
| searxng | Zoekmachine | 8888 |
| sandbox-api | n8n sandbox API | Intern |
| sandbox-runner-1 | Sandbox runner | Intern |
| sandbox-certs | Sandboxcertificaten | Intern |

## Verkeersstromen

1. De gebruiker opent de frontend via poort 8080.
2. Nginx serveert de frontendbestanden.
3. API-verzoeken onder `/api/` worden doorgestuurd naar FastAPI.
4. FastAPI communiceert met PostgreSQL.
5. n8n voert automatiseringsworkflows uit.
6. SearXNG levert zoekresultaten aan ondersteunde n8n-functionaliteit.

## Netwerk

De services gebruiken het Docker-netwerk `athletehub`.

De API is op de host gebonden aan `127.0.0.1:8000`.
De frontend, n8n en SearXNG hebben de poortpublicaties uit docker-compose.yml.

## Belangrijk

Controleer docker-compose.yml en nginx.conf voordat netwerkconfiguraties worden gewijzigd.

Dit document beschrijft de huidige basisarchitectuur. Verdere uitbreidingen moeten hier worden bijgehouden.
