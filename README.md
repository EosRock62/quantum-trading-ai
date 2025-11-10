# Quantum Trading AI — Minimal Starter (FastAPI + GPT + UI)

**Zweck:** Ein seriöses, minimalistisches Starterpaket: Chat-Oberfläche (wie ChatGPT), einfache Signal-Simulation
(EUR/USD, S&P 500, Gold), stündliche Selbst-Evaluations-Schleife (Stub) und Docker-Setup.

> **Hinweis:** Dies ist ein *Starter*. Er ist so gebaut, dass er sofort lauffähig ist und sich Schritt für Schritt
> erweitern lässt (DB, Redis, echtes LSTM, Live-Daten).

## Quickstart

### 1) Env anlegen
Kopiere `.env.example` zu `.env` und trage deinen OpenAI-Key ein (optional, sonst Mock-Antworten):

```bash
cp .env.example .env
# Datei bearbeiten und OPENAI_API_KEY=... setzen
```

### 2) Lokal ohne Docker
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.app:app --reload --port 8000
```

Dann öffne http://localhost:8000 – das Frontend wird von FastAPI als statische Website ausgeliefert.

### 3) Mit Docker (empfohlen)
```bash
docker-compose up --build
```
Danach: http://localhost:8000

## Projektstruktur

```
.
├── .github/ISSUE_TEMPLATE/feature.md
├── .gitignore
├── .env.example
├── LICENSE
├── README.md
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   ├── gpt_client.py
│   ├── models.py
│   ├── schemas.py
│   ├── signal_engine.py
│   ├── self_improve.py
│   ├── tasks.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   └── assets/
│       ├── app.js
│       └── logo.svg
├── data/
│   └── sample_prices.csv
└── tests/
    └── test_health.py
```

## Nächste Schritte (Roadmap)
1. **DB/Redis anschließen** (Postgres/Redis sind in `docker-compose.yml` vorbereitet).
2. **Echte Daten-Feeds** einbinden (z. B. Broker/Market-Data-API).
3. **LSTM-Modul** (PyTorch/TensorFlow) ersetzen den Stub aus `signal_engine.py`.
4. **Stündliche Selbst-Verbesserung** ausbauen (`self_improve.py` + `tasks.py`).

> **Kein Finanzrat:** Dieses Projekt dient Forschungs- und Entwicklungszwecken.
