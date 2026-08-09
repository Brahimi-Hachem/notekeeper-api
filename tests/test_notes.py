from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_note() -> None:
    response = client.post(
        "/notes/",
        json={
            "title": "Learning FastAPI",
            "content": "Testing the API with pytest.",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Learning FastAPI",
        "content": "Testing the API with pytest.",
    }


def test_create_note_rejects_empty_title() -> None:
    response = client.post(
        "/notes/",
        json={
            "title": "",
            "content": "This should fail.",
        },
    )

    assert response.status_code == 422
