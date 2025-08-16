# L3AGI → XAgent Demo

A minimal full-stack demo:
- **FastAPI** backend with `/health` and `/run`
- **Static** frontend served from the same server
- Simple agent that supports `echo` and `add` via keyword routing

## Run
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8008
```
Open: http://localhost:8008/

## Tests
```bash
cd backend
pytest -q
```
