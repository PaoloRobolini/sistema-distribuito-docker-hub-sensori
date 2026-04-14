# Report Tecnico - Parte B: Analisi e Valutazione della Rete

**Nome e Cognome:** ___________________________  
**Classe:** ___________________________  
**Data:** ___________________________

---

## B1. Risoluzione dei Nomi (DNS Interno)

> All'interno del codice Python della Webapp e del Worker, per connetterti al broker MQTT
> hai utilizzato l'indirizzo host "emqx". Spiega dettagliatamente come fanno i container
> a risolversi a vicenda senza conoscere i rispettivi indirizzi IP.
> Quale meccanismo viene messo a disposizione da Docker Compose in merito alle reti
> personalizzate (bridge)?

### Risposta:

_(Scrivi qui la tua risposta. Suggerimento: parla del DNS server interno di Docker,
della rete bridge personalizzata e di come i nomi dei servizi vengono risolti
automaticamente in indirizzi IP.)_

---

## B2. Esposizione delle Porte e Sicurezza Perimetrale

> Nel definire il servizio del broker MQTT all'interno del docker-compose.yml,
> è emersa la questione sull'esposizione della porta standard MQTT (1883).

### B2a. È necessario mappare la porta 1883 verso l'host?

> È necessario mappare la porta 1883 verso l'host fisico (es. ports: ["1883:1883"])
> affinché il Worker e la Webapp possano comunicare con il broker?
> Giustifica la tua risposta.

### Risposta:

_(Scrivi qui la tua risposta. Suggerimento: considera la differenza tra comunicazione
interna alla rete Docker e comunicazione verso l'esterno.)_

### B2b. Rischi di sicurezza

> Quali sarebbero i rischi di sicurezza se esponessi pubblicamente la porta 1883
> senza un proxy TCP (layer 4)?

### Risposta:

_(Scrivi qui la tua risposta. Suggerimento: considera accesso non autenticato,
intercettazione dati, attacchi DoS, pubblicazione di messaggi malevoli.)_

---

## B3. Flusso di Rete della "Forward Authentication"

> Fai riferimento alla configurazione implementata nella Fase 4.
> Traccia e descrivi l'esatto percorso di rete di un pacchetto HTTP (dall'esterno
> fino alla Webapp) quando un utente non autenticato tenta di accedere alla risorsa
> protetta, evidenziando il ruolo di Caddy come API Gateway tra la rete esterna
> e la rete isolata dei container.

### Risposta:

_(Scrivi qui la tua risposta. Suggerimento: descrivi ogni passaggio numerandolo,
dal browser fino alla webapp, passando per Caddy e Authelia. Indica cosa succede
quando l'utente NON è autenticato e cosa succede DOPO il login.)_

**Percorso utente NON autenticato:**

1. _..._
2. _..._
3. _..._

**Percorso utente DOPO il login:**

1. _..._
2. _..._
3. _..._

---

## Schema di Rete (Opzionale)

> Disegna uno schema che rappresenti la rete del sistema, indicando i servizi,
> le porte e i flussi di comunicazione.

_(Puoi usare un diagramma ASCII, un disegno a mano fotografato, o uno strumento
come draw.io)_
