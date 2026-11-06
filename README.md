# AppAgentica: consigli per algoritmi di ordinamento

Progetto Python che cerca in un catalogo di algoritmi (Python, Java, C++, JavaScript, C#, Go, Rust e implementazioni manuali) e usa un modello OpenAI economico per consigliare quello adatto. Qdrant conserva gli embedding nel database vettoriale.

## Requisiti

- Python 3.10 o successivo
- Docker Desktop con Docker Compose
- Una chiave API OpenAI (gli embedding usano `text-embedding-3-small`, la chat `gpt-4o-mini`)

## Avvio da Windows PowerShell

```powershell
cd C:\projects\AppAgentica
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Inserisci la chiave in `.env`, poi avvia il database e indicizza il catalogo:

```powershell
docker compose up -d
python ingest.py
python app.py
```

La dashboard Qdrant è disponibile a `http://localhost:6333/dashboard`. Per fermarlo: `docker compose down` (i dati restano nel volume Docker); per cancellare anche i dati: `docker compose down -v`.

## Jupyter Notebook

Il notebook `appagentica.ipynb` importa le stesse funzioni di `app.py` e `ingest.py`, così la logica non diverge. Dopo aver installato `requirements.txt`, avvia `jupyter lab`, apri il notebook ed esegui le celle dall'alto. Le prime celle indicizzano il dataset; poi puoi chiamare `ask("Mi servono solo i 10 elementi più grandi di una lista enorme in Python")`.

## File principali

- `algorithms.json`: catalogo di 36 schede con complessità, stabilità, casi d'uso e codice.
- `config.py`: configurazione e caricamento del `.env` dalla cartella del progetto.
- `ingest.py`: crea embedding e aggiorna la collection Qdrant senza cancellarla.
- `app.py`: prompt engine interattivo e funzione `ask()` riusabile dal notebook.
- `docker-compose.yml`: servizio Qdrant e volume persistente.

La prima indicizzazione e ogni domanda inviano testo all'API OpenAI e possono avere un costo. Aggiungi nuove schede a `algorithms.json` e rilancia `python ingest.py`.
