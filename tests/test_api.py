
from fastapi.testclient import TestClient

from app.main import app
import app.main as main_module

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_list_employees():
    response = client.get("/employees")

    assert response.status_code == 200
    assert len(response.json()["employees"]) == 4


def test_employee_not_found():
    response = client.get("/employees/999")

    assert response.status_code == 404


def test_search_python():
    response = client.get(
        "/employees/search",
        params={"skill": "Python"}
    )

    assert response.status_code == 200
    assert response.json()["count"] == 3


def test_generate(monkeypatch):
    def fake_generate(prompt, temperature=1.0):
        return {
            "response": "A mocked AI response",
            "model": "test-model"
        }

    monkeypatch.setattr(
        main_module,
        "generate_ai_response",
        fake_generate
    )

    response = client.post(
        "/generate",
        json={
            "prompt": "Explain APIs",
            "temperature": 0.5
        }
    )

    assert response.status_code == 200
    assert response.json()["response"] == "A mocked AI response"


def test_empty_prompt_is_rejected():
    response = client.post(
        "/generate",
        json={
            "prompt": "",
            "temperature": 1.0
        }
    )

    assert response.status_code == 422
