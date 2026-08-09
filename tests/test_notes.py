from fastapi.testclient import TestClient


def test_list_notes_returns_empty_list(client: TestClient) -> None:
    response = client.get("/notes/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_note_persists_and_retrieves_note(client: TestClient) -> None:
    response = client.post(
        "/notes/",
        json={
            "title": "Learning FastAPI",
            "content": "Testing the API with pytest.",
        },
    )

    assert response.status_code == 201
    created_note = response.json()
    assert isinstance(created_note["id"], int)
    assert created_note["title"] == "Learning FastAPI"
    assert created_note["content"] == "Testing the API with pytest."

    get_response = client.get("/notes/")

    assert get_response.status_code == 200
    assert get_response.json() == [created_note]


def test_list_notes_returns_multiple_persisted_notes(client: TestClient) -> None:
    first_response = client.post(
        "/notes/",
        json={"title": "First note", "content": "First content."},
    )
    second_response = client.post(
        "/notes/",
        json={"title": "Second note", "content": "Second content."},
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert first_response.json()["id"] != second_response.json()["id"]

    get_response = client.get("/notes/")

    assert get_response.status_code == 200
    assert get_response.json() == [first_response.json(), second_response.json()]


def test_create_note_rejects_empty_title(client: TestClient) -> None:
    response = client.post(
        "/notes/",
        json={
            "title": "",
            "content": "This should fail.",
        },
    )

    assert response.status_code == 422
