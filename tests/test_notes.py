from fastapi.testclient import TestClient


def test_list_notes_returns_empty_list(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.get(
        "/notes/",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []


def test_create_note_persists_and_retrieves_note(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.post(
        "/notes/",
        headers=auth_headers,
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

    get_response = client.get(
        "/notes/",
        headers=auth_headers,
    )

    assert get_response.status_code == 200
    assert get_response.json() == [created_note]


def test_list_notes_returns_multiple_persisted_notes(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    first_response = client.post(
        "/notes/",
        headers=auth_headers,
        json={
            "title": "First note",
            "content": "First content.",
        },
    )

    second_response = client.post(
        "/notes/",
        headers=auth_headers,
        json={
            "title": "Second note",
            "content": "Second content.",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert first_response.json()["id"] != second_response.json()["id"]

    get_response = client.get(
        "/notes/",
        headers=auth_headers,
    )

    assert get_response.status_code == 200
    assert get_response.json() == [
        first_response.json(),
        second_response.json(),
    ]


def test_create_note_rejects_empty_title(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.post(
        "/notes/",
        headers=auth_headers,
        json={
            "title": "",
            "content": "This should fail.",
        },
    )

    assert response.status_code == 422


def test_users_can_only_see_their_own_notes(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    user1_response = client.post(
        "/notes/",
        headers=auth_headers,
        json={
            "title": "User 1 note",
            "content": "Private to user 1.",
        },
    )

    assert user1_response.status_code == 201

    user1_note = user1_response.json()

    user2_register_response = client.post(
        "/auth/register",
        json={
            "email": "user2@example.com",
            "password": "password123",
        },
    )

    assert user2_register_response.status_code == 201

    user2_login_response = client.post(
        "/auth/login",
        json={
            "email": "user2@example.com",
            "password": "password123",
        },
    )

    assert user2_login_response.status_code == 200

    user2_token = user2_login_response.json()["access_token"]

    user2_headers = {
        "Authorization": f"Bearer {user2_token}",
    }

    user2_response = client.post(
        "/notes/",
        headers=user2_headers,
        json={
            "title": "User 2 note",
            "content": "Private to user 2.",
        },
    )

    assert user2_response.status_code == 201

    user2_note = user2_response.json()

    user1_notes_response = client.get(
        "/notes/",
        headers=auth_headers,
    )

    assert user1_notes_response.status_code == 200
    assert user1_notes_response.json() == [user1_note]
    assert user2_note not in user1_notes_response.json()

    user2_notes_response = client.get(
        "/notes/",
        headers=user2_headers,
    )

    assert user2_notes_response.status_code == 200
    assert user2_notes_response.json() == [user2_note]
    assert user1_note not in user2_notes_response.json()


def test_get_note_returns_note(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    create_response = client.post(
        "/notes/",
        headers=auth_headers,
        json={
            "title": "Get this note",
            "content": "Testing GET by ID.",
        },
    )

    assert create_response.status_code == 201
    created_note = create_response.json()

    response = client.get(
        f"/notes/{created_note['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == created_note


def test_get_note_returns_404_for_missing_note(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.get(
        "/notes/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_user_cannot_get_another_users_note(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    create_response = client.post(
        "/notes/",
        headers=auth_headers,
        json={
            "title": "Private note",
            "content": "Only user 1 should access this.",
        },
    )

    assert create_response.status_code == 201
    note_id = create_response.json()["id"]

    register_response = client.post(
        "/auth/register",
        json={
            "email": "another-user@example.com",
            "password": "password123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "another-user@example.com",
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    user2_headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}",
    }

    response = client.get(
        f"/notes/{note_id}",
        headers=user2_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_update_note(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    create_response = client.post(
        "/notes/",
        headers=auth_headers,
        json={
            "title": "Original title",
            "content": "Original content.",
        },
    )

    assert create_response.status_code == 201
    note_id = create_response.json()["id"]

    response = client.put(
        f"/notes/{note_id}",
        headers=auth_headers,
        json={
            "title": "Updated title",
            "content": "Updated content.",
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["title"] == "Updated title"
    assert response.json()["content"] == "Updated content."


def test_user_cannot_update_another_users_note(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    create_response = client.post(
        "/notes/",
        headers=auth_headers,
        json={
            "title": "User 1 note",
            "content": "Private content.",
        },
    )

    assert create_response.status_code == 201
    note_id = create_response.json()["id"]

    register_response = client.post(
        "/auth/register",
        json={
            "email": "update-user@example.com",
            "password": "password123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "update-user@example.com",
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    user2_headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}",
    }

    response = client.put(
        f"/notes/{note_id}",
        headers=user2_headers,
        json={
            "title": "Hacked title",
            "content": "Hacked content.",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    original_response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers,
    )

    assert original_response.status_code == 200
    assert original_response.json()["title"] == "User 1 note"
    assert original_response.json()["content"] == "Private content."


def test_delete_note(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    create_response = client.post(
        "/notes/",
        headers=auth_headers,
        json={
            "title": "Delete me",
            "content": "This note should disappear.",
        },
    )

    assert create_response.status_code == 201
    note_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/notes/{note_id}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404


def test_user_cannot_delete_another_users_note(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    create_response = client.post(
        "/notes/",
        headers=auth_headers,
        json={
            "title": "Protected note",
            "content": "This should not be deleted.",
        },
    )

    assert create_response.status_code == 201
    note_id = create_response.json()["id"]

    register_response = client.post(
        "/auth/register",
        json={
            "email": "delete-user@example.com",
            "password": "password123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "delete-user@example.com",
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    user2_headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}",
    }

    response = client.delete(
        f"/notes/{note_id}",
        headers=user2_headers,
    )

    assert response.status_code == 404

    original_response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers,
    )

    assert original_response.status_code == 200
