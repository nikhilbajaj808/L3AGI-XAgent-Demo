# backend/tests/test_integration.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_run_echo_debug():
    r = client.post("/run?debug=true", json={"prompt": "echo hello"})
    assert r.status_code == 200
    data = r.json()
    assert data["tool_used"] in ("echo", "add")
    assert "assistant" in data

def test_run_echo_clean():
    r = client.post("/run", json={"prompt": "echo hello"})
    assert r.status_code == 200
    data = r.json()
    assert "result" in data
    assert isinstance(data["result"], str)

def test_run_add_debug():
    r = client.post("/run?debug=true", json={"prompt": "please add 5 and 7"})
    assert r.status_code == 200
    data = r.json()
    assert data["tool_used"] == "add"
    assert abs(data["observation"]["result"] - 12.0) < 1e-9

def test_run_add_clean():
    r = client.post("/run", json={"prompt": "please add 5 and 7"})
    assert r.status_code == 200
    data = r.json()
    assert "result" in data
    assert "12" in data["result"]  # The string should contain the number
