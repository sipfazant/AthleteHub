# AI Trainer

## Doel

De AI Trainer is de sportgerichte AI-assistent binnen AthleteHub.

De assistent moet gebruikers ondersteunen bij:
- Trainingsschema's
- Hardlopen en fietsen
- Analyse van sportactiviteiten
- Trainingsbelasting
- Herstel
- Interpretatie van sportgegevens
- Algemene sport- en conditievragen

De assistent stelt geen medische diagnoses.

## Huidige technologie
- n8n
- AI Agent
- Ollama Chat Model
- Simple Memory
- Model: qwen3:8b
- Temperatuur: 0.3

## Huidige workflow

De bestaande workflow bevat:

1. When chat message received
2. AI Agent
3. Ollama Chat Model
4. Simple Memory

## Gewenste architectuur

1. Frontend verstuurt een bericht naar FastAPI.
2. FastAPI controleert de gebruikerssessie.
3. FastAPI haalt het gesprek op of maakt een nieuw gesprek aan.
4. FastAPI stuurt het bericht naar n8n.
5. n8n voert de AI-workflow uit.
6. Het antwoord wordt teruggestuurd naar FastAPI.
7. FastAPI slaat het antwoord op in PostgreSQL.
8. Frontend toont het antwoord.

## Geheugen

AI-gesprekken moeten correct gescheiden blijven.

Het geheugen moet rekening houden met de juiste gebruiker en het juiste gesprek.

## Nog te realiseren of controleren
- Koppeling FastAPI met n8n
- Correcte webhookconfiguratie
- Response Mode van de chattrigger
- Productie- en test-URL
- Authenticatie tussen backend en n8n
- Opslag van gesprekken en berichten
- Scheiding van geheugen per gesprek
- Foutafhandeling en time-outs
- Testen van volledige berichtenstroom

## Veiligheid
De AI Trainer moet rekening houden met leeftijd, ervaring en beschikbare trainingsgegevens.

De assistent geeft algemene sportinformatie en verwijst bij medische vragen naar een geschikte zorgprofessional.
