import json
import time
import urllib.error
import urllib.request

BASE_URL = "http://127.0.0.1:8000"


def request(path, method="GET", payload=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        f"{BASE_URL}{path}", method=method, data=data, headers=headers
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.load(resp)
    except urllib.error.HTTPError as exc:
        print("HTTP error:", exc.code, exc.read().decode())
        raise


email = f"noteuser{int(time.time())}@example.com"
password = "password123"

print("Registering user:", email)
status, body = request(
    "/auth/register", method="POST", payload={"email": email, "password": password}
)
print("Register:", status, body)

status, body = request(
    "/auth/login", method="POST", payload={"email": email, "password": password}
)
print("Login:", status, body)
token = body["access_token"]

note_payload = {
    "title": "My new note",
    "content": "This note was added via cmd script.",
}
status, body = request("/notes/", method="POST", payload=note_payload, token=token)
print("Create note:", status, body)

status, body = request("/notes/", method="GET", token=token)
print("List notes:", status)
print(json.dumps(body, indent=2))
