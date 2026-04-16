# Smart City Hub: Infrastruttura Distribuita per Sensoristica IoT

## Descrizione del Progetto

Piattaforma distribuita a microservizi per raccogliere e analizzare in tempo reale
i dati provenienti da sensori ambientali IoT di una smart city.

L'architettura è composta da:
- **Caddy** — API Gateway, reverse proxy e load balancer
- **Flask** (2 repliche) — Webapp per l'interfaccia utente e l'invio dati
- **EMQX** — Broker MQTT per la comunicazione asincrona IoT
- **Worker Python** — Microservizio per l'elaborazione dei messaggi MQTT
- **Authelia** — Forward authentication per proteggere le rotte sensibili

## Architettura

```
                    ┌─────────────────────────────────────────────┐
                    │            Rete Docker: smartcity-net       │
  Browser :80 ───►  │  Caddy ──┬──► app1:5000 (Flask)             │
                    │          └──► app2:5000 (Flask)             │
                    │                    │                        │
                    │          forward_auth                       │
                    │          ┌──► Authelia:9091                 │
                    │          │                                  │
                    │          EMQX:1883 (MQTT interno)           │
                    │              │                              │
                    │          Worker (subscriber)                │
                    └─────────────────────────────────────────────┘
```

## Prerequisiti

| Strumento | Scopo |
|-----------|-------|
| **Docker Desktop** | Esecuzione dei container |
| **VS Code** | Editor di codice (estensione Docker consigliata) |
| **Browser** | Accesso all'interfaccia web |
| **curl / Postman** | Test delle API REST |

## Struttura del Progetto

```
.
├── docker-compose.yml          # Orchestrazione dei servizi
├── Caddyfile                   # Configurazione reverse proxy
├── webapp/
│   ├── Dockerfile              # Immagine Docker della webapp
│   ├── requirements.txt        # Dipendenze Python
│   ├── app.py                  # Applicazione Flask
│   └── templates/
│       └── index.html          # Interfaccia utente
├── worker/
│   ├── Dockerfile              # Immagine Docker del worker (TODO)
│   ├── requirements.txt        # Dipendenze Python
│   └── worker.py               # Subscriber MQTT (TODO)
├── authelia/
│   ├── configuration.yml       # Configurazione Authelia (fornito)
│   └── users_database.yml      # Database utenti (fornito)
└── docs/
    ├── guida-step-by-step.md   # Guida implementativa dettagliata
    └── report-template.md      # Template per il report (Parte B)
```

## Come Procedere

### Fasi di implementazione

| Fase | Descrizione | File da modificare |
|------|-------------|-------------------|
| **Fase 1** | Bilanciamento del carico | `docker-compose.yml`, `Caddyfile` |
| **Fase 2** | Comunicazione MQTT | `docker-compose.yml`, `webapp/app.py` |
| **Fase 3** | Worker di elaborazione | `worker/Dockerfile`, `worker/worker.py`, `docker-compose.yml` |
| **Fase 4** | Forward Authentication | `docker-compose.yml`, `Caddyfile` |

### Istruzioni

1. Leggi la guida dettagliata in `docs/guida-step-by-step.md`
2. Completa i file contrassegnati con `TODO` seguendo l'ordine delle fasi
3. Testa ogni fase prima di passare alla successiva
4. Compila il report tecnico in `docs/report-template.md`

## Comandi Rapidi

```bash
# Avvia tutti i servizi (ricostruendo le immagini)
docker compose up --build

# Ferma tutti i servizi
docker compose down

# Reset completo (rimuove anche i volumi)
docker compose down -v

# Visualizza i log di un servizio specifico
docker compose logs -f worker

# Invia un messaggio di test alla rotta /publish
curl -X POST http://localhost/publish \
  -H "Content-Type: application/json" \
  -d '{"sensore": "temperatura", "valore": 22.5}'
```

## Credenziali di Test

| Servizio | Username | Password |
|----------|----------|----------|
| **Authelia** | `studente` | `password123` |
| **EMQX Dashboard** | `admin` | `public` |

## Porte Esposte

| Servizio | Porta | URL |
|----------|-------|-----|
| Caddy (webapp) | 80 | http://localhost |
| EMQX Dashboard | 18083 | http://localhost:18083 |
| Authelia | 9091 | http://localhost:9091 |
