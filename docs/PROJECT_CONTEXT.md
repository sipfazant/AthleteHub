# AthleteHub – Projectcontext

## Doel
AthleteHub is een persoonlijk sportplatform voor het verzamelen, beheren en analyseren van sportactiviteiten en trainingsgegevens.

Het project wordt lokaal ontwikkeld en draait via Docker Compose.

## Ontwikkelomgeving
- Besturingssysteem: Windows
- Projectmap: D:\docker\AthleteHub
- GitHub: https://github.com/sipfazant/AthleteHub
- Git-branch: main

## Technologieën
- Frontend: HTML, CSS en JavaScript
- Webserver: Nginx
- Backend: Python en FastAPI
- Database: PostgreSQL 17
- Automatisering: n8n 2.46.6
- Web search: SearXNG
- AI: Ollama met Qwen3 8B
- Containers: Docker Compose

## Huidige functionaliteit

### Backend
- Accountinitialisatie
- Aanmelden en uitloggen
- Sessiebeheer via cookies
- Wachtwoordhashing met Argon2
- Accountgegevens wijzigen
- Sportactiviteiten opslaan en ophalen
- Trainingsstatistieken ophalen
- Database-healthcheck

### Frontend
- Aanmeldscherm
- Persoonlijk dashboard
- Activiteitenoverzicht
- Trainingsstatistieken
- Accountinstellingen
- Uitloggen

### Automatisering en AI
- n8n draait via Docker.
- Een AI Trainer-workflow is aangemaakt.
- De workflow gebruikt een AI Agent, Ollama Chat Model en Simple Memory.
- Het gebruikte model is qwen3:8b.
- De volledige koppeling tussen FastAPI, PostgreSQL en de AI-workflow moet nog verder worden uitgewerkt en gecontroleerd.

## Belangrijke afspraken
- AthleteHub is bedoeld als persoonlijk platform.
- De bestaande architectuur moet behouden blijven.
- Controleer bestaande code voordat je wijzigingen voorstelt.
- Verzin geen bestaande functionaliteit.
- Houd deze documentatie actueel.
- Vraag nooit om wachtwoorden of de inhoud van .env.

## Ontwikkelstatus
Dit document wordt bijgewerkt naarmate AthleteHub verder wordt ontwikkeld.
