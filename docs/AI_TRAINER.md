
# AI Trainer

## Doel

De AI Trainer is de sportgerichte AI-assistent binnen AthleteHub.

De assistent ondersteunt bij:
- Trainingsschema's
- Hardlopen en fietsen
- Analyse van sportactiviteiten
- Trainingsbelasting
- Herstel
- Interpretatie van sportgegevens
- Algemene sport- en conditievragen

De assistent stelt geen medische diagnoses.

## Technologie

- FastAPI
- PostgreSQL
- n8n
- AI Agent
- Ollama Chat Model
- Simple Memory
- Model: qwen3:8b
- Temperatuur: 0.3

## n8n-workflow

De workflow bevat twee ingangen:

1. When chat message received
2. Webhook voor communicatie met AthleteHub

Beide gebruiken een AI Agent met Ollama Chat Model en Simple Memory.

De webhook gebruikt:
- Methode: POST
- Productiepad: `/webhook/athletehub-ai`
- Header-authenticatie: `X-AthleteHub-Secret`
- Response Mode: When Last Node Finishes
- Response Data: First Entry JSON

De AI Agent retourneert het antwoord in het veld `output`.

## Backendintegratie

De berichtenstroom:

1. Frontend verstuurt een bericht naar FastAPI.
2. FastAPI controleert de gebruikerssessie.
3. FastAPI controleert of het gesprek bestaat.
4. Het gebruikersbericht wordt opgeslagen in PostgreSQL.
5. FastAPI verstuurt het bericht naar n8n.
6. n8n voert de AI-workflow uit.
7. Het AI-antwoord wordt teruggestuurd.
8. FastAPI slaat het antwoord op in PostgreSQL.
9. De frontend kan de berichten ophalen.

## API-endpoints

- `POST /ai/conversations`: nieuw gesprek.
- `GET /ai/conversations`: gesprekken ophalen.
- `GET /ai/conversations/{id}/messages`: berichten ophalen.
- `POST /ai/conversations/{id}/messages`: bericht versturen.

## Geheugen

Simple Memory gebruikt de conversation-ID als session-ID.

Daardoor wordt het geheugen per gesprek gescheiden.

De context window length staat momenteel op 10.

## Configuratie

De backend gebruikt de volgende omgevingsvariabelen:

- `N8N_WEBHOOK_URL`
- `N8N_WEBHOOK_SECRET`

Gevoelige waarden worden uitsluitend lokaal in `.env` opgeslagen.

## Foutafhandeling

- Een niet-bereikbare webhook resulteert in HTTP 502.
- Een ontbrekende webhookconfiguratie resulteert in HTTP 503.
- Het gebruikersbericht blijft bewaard wanneer n8n niet bereikbaar is.
- Er wordt geen fictief AI-antwoord opgeslagen.

## Nog te realiseren of controleren

- Frontendintegratie met de nieuwe API-endpoints.
- Volledige test van de berichtenstroom.
- Controleren of geheugen correct blijft werken bij meerdere gesprekken.
- Controleren of gesprekken na herstart beschikbaar blijven.

## Veiligheid

De AI Trainer houdt rekening met leeftijd, ervaring en beschikbare trainingsgegevens.

De assistent geeft algemene sportinformatie en stelt geen medische diagnoses.
