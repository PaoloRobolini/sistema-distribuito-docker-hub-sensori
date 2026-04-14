# Guida Step-by-Step: Smart City Hub

Questa guida ti accompagna passo passo nella realizzazione dell'infrastruttura
distribuita per la piattaforma Smart City Hub.

**Procedi in ordine. Testa ogni fase prima di passare alla successiva.**

---

## Prerequisiti

- Docker Desktop installato e funzionante
- Editor di codice (VS Code consigliato)
- Browser web moderno
- Terminale (PowerShell, CMD, o Bash)

### Comandi Docker Compose Essenziali

| Comando | Descrizione |
|---------|-------------|
| `docker compose up --build` | Avvia tutti i servizi, ricostruendo le immagini |
| `docker compose down` | Ferma e rimuove tutti i container |
| `docker compose down -v` | Come sopra + rimuove i volumi (reset completo) |
| `docker compose logs -f <servizio>` | Mostra i log in tempo reale di un servizio |
| `docker compose ps` | Mostra lo stato dei servizi |

---

## Panoramica dell'Architettura

```
                    ┌─────────────────────────────────────────────┐
                    │            Rete Docker: smartcity-net        │
  Browser :80 ───►  │  Caddy ──┬──► app1:5000 (Flask)             │
                    │          └──► app2:5000 (Flask)             │
                    │                    │                         │
                    │          forward_auth                        │
                    │          ┌──► Authelia:9091                  │
                    │          │                                   │
                    │          EMQX:1883 (MQTT interno)            │
                    │              │                               │
                    │          Worker (subscriber)                 │
                    └─────────────────────────────────────────────┘
```

---

## Fase 1: Bilanciamento del Carico (Load Balancing)

### Obiettivo
Configurare due istanze della webapp Flask dietro un reverse proxy Caddy
che bilancia il traffico con politica round-robin.

### File da modificare

#### 1.1 — `docker-compose.yml`: Aggiungi app2, Caddy e la rete

Devi aggiungere:

- **Servizio `app2`**: clone di `app1` con `container_name: app2`
- **Servizio `caddy`**:
  - Immagine: `caddy:2-alpine`
  - Porta: `80:80` (mappata sull'host)
  - Volume: `./Caddyfile:/etc/caddy/Caddyfile` (monta il file di configurazione)
  - Rete: `smartcity-net`
- **Rete `smartcity-net`** con driver `bridge`
- Aggiungi `networks: [smartcity-net]` a **tutti** i servizi (app1, app2, caddy)

#### 1.2 — `Caddyfile`: Configura il load balancing

Dentro il blocco `http://localhost`, aggiungi:

```
reverse_proxy app1:5000 app2:5000 {
    lb_policy round_robin
}
```

### Verifica

```bash
docker compose up --build
```

Apri `http://localhost` nel browser e ricarica più volte la pagina.
Dovresti vedere l'**hostname** cambiare tra `app1` e `app2` (effetto round-robin).

---

## Fase 2: Comunicazione Asincrona IoT (MQTT)

### Obiettivo
Integrare il broker MQTT EMQX e implementare la rotta `/publish` nella webapp
per pubblicare messaggi sul topic `notifications`.

### File da modificare

#### 2.1 — `docker-compose.yml`: Aggiungi il broker EMQX

Aggiungi il servizio `emqx`:
- Immagine: `emqx/emqx:latest`
- Porta: `18083:18083` (solo dashboard web)
- **IMPORTANTE:** NON esporre la porta `1883` verso l'host!
- Rete: `smartcity-net`

> **Domanda chiave (Parte B):** Perché non serve esporre la porta 1883?

#### 2.2 — `webapp/app.py`: Implementa la rotta `/publish`

Nella funzione `publish()`, devi:

1. Ricevere il payload JSON: `data = request.get_json()`
2. Importare e creare un client MQTT:
   ```python
   import paho.mqtt.client as mqtt
   client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
   ```
3. Connetterti al broker: `client.connect("emqx", 1883, 60)`
4. Pubblicare sul topic: `client.publish("notifications", json.dumps(data))`
5. Disconnetterti: `client.disconnect()`
6. Ritornare conferma: `return jsonify({"status": "ok", ...})`

### Verifica

```bash
docker compose up --build
```

Invia un messaggio di test:
```bash
curl -X POST http://localhost/publish \
  -H "Content-Type: application/json" \
  -d '{"sensore": "temperatura", "valore": 22.5}'
```

Controlla la **dashboard EMQX**: `http://localhost:18083` (login: `admin` / `public`)

---

## Fase 3: Il Worker di Elaborazione

### Obiettivo
Creare un microservizio Python indipendente che si sottoscrive al topic MQTT
`notifications` e stampa ogni messaggio ricevuto.

### File da completare

#### 3.1 — `worker/Dockerfile`

Completa il Dockerfile basandoti sul modello di `webapp/Dockerfile`:
- Immagine base: `python:3.11-slim`
- Directory di lavoro: `/app`
- Copia e installa `requirements.txt`
- Copia il codice sorgente
- Comando: `python worker.py`

#### 3.2 — `worker/worker.py`

Implementa il subscriber MQTT:

```python
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connesso al broker MQTT!")
    client.subscribe("notifications")

def on_message(client, userdata, message):
    print(f"Messaggio ricevuto su {message.topic}: {message.payload.decode()}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("emqx", 1883, 60)
client.loop_forever()
```

#### 3.3 — `docker-compose.yml`: Aggiungi il servizio worker

- Build: `./worker`
- `container_name: worker`
- `depends_on: [emqx]`
- Rete: `smartcity-net`

### Verifica

```bash
docker compose up --build
```

In un altro terminale, invia un messaggio:
```bash
curl -X POST http://localhost/publish \
  -H "Content-Type: application/json" \
  -d '{"sensore": "umidita", "valore": 65}'
```

Controlla i log del worker:
```bash
docker compose logs -f worker
```

Dovresti vedere: `Messaggio ricevuto su notifications: {"sensore": "umidita", "valore": 65}`

---

## Fase 4: Sicurezza e Forward Authentication

### Obiettivo
Proteggere la rotta `/publish` con Authelia, richiedendo l'autenticazione
prima di poter inviare dati al broker MQTT.

### File da modificare

#### 4.1 — `docker-compose.yml`: Aggiungi Authelia

Aggiungi il servizio `authelia`:
- Immagine: `authelia/authelia:latest`
- Volume: `./authelia:/config`
- Porta: `9091:9091`
- Rete: `smartcity-net`

> I file di configurazione di Authelia (`configuration.yml` e `users_database.yml`)
> sono già forniti e pre-configurati.

#### 4.2 — `Caddyfile`: Configura la Forward Authentication

Devi modificare il Caddyfile per:

1. Usare un **matcher** per intercettare `/publish`:
   ```
   @publish path /publish
   ```

2. Per le richieste a `/publish`, applicare `forward_auth` prima del reverse_proxy:
   ```
   handle @publish {
       forward_auth authelia:9091 {
           uri /api/authz/forward-auth
           copy_headers Remote-User Remote-Groups Remote-Email Remote-Name
       }
       reverse_proxy app1:5000 app2:5000 {
           lb_policy round_robin
       }
   }
   ```

3. Mantenere la rotta `/` senza protezione (in un blocco `handle` separato)

### Credenziali di Test

| Campo | Valore |
|-------|--------|
| Username | `studente` |
| Password | `password123` |

### Verifica

```bash
docker compose up --build
```

1. **Test senza autenticazione:**
   Apri `http://localhost/publish` nel browser → verrai reindirizzato al login di Authelia

2. **Test con autenticazione:**
   Effettua il login su `http://localhost:9091` con `studente` / `password123`,
   poi riprova ad accedere a `/publish` → accesso consentito

3. **Test rotta pubblica:**
   `http://localhost/` → accessibile senza autenticazione

---

## Riepilogo dei Servizi

| Servizio | Porta Host | Descrizione |
|----------|-----------|-------------|
| Caddy | 80 | API Gateway, Load Balancer, Forward Auth |
| app1 | — (interna) | Webapp Flask, istanza 1 |
| app2 | — (interna) | Webapp Flask, istanza 2 |
| EMQX | 18083 (dashboard) | Broker MQTT |
| Worker | — (interna) | Subscriber MQTT |
| Authelia | 9091 | Portale di autenticazione |

---

## Dopo aver completato tutte le fasi

Compila il report tecnico in `docs/report-template.md` rispondendo alle domande
della Parte B (B1, B2, B3).
