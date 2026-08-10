import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

import streamlit as st

DEFAULT_API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")
PAGES = ["Register", "Login", "Notes"]


def api_request(path, method="GET", payload=None, token=None, base_url=DEFAULT_API_URL):
    url = urllib.parse.urljoin(base_url, path)
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read().decode("utf-8")
            if raw:
                return response.status, json.loads(raw)
            return response.status, None
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8")
        try:
            message = json.loads(body)
        except ValueError:
            message = body
        return error.code, message
    except urllib.error.URLError as error:
        return None, str(error.reason)


def show_error(message):
    st.error(message)


def show_success(message):
    st.success(message)


def clear_edit_state():
    for key in ["edit_note_id", "edit_title", "edit_content"]:
        if key in st.session_state:
            del st.session_state[key]


def register_page():
    st.header("Register")
    with st.form("register_form"):
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        submit = st.form_submit_button("Register")

    if submit:
        if not email or not password:
            show_error("Email and password are required.")
            return

        status, payload = api_request(
            "/auth/register",
            method="POST",
            payload={"email": email, "password": password},
            base_url=st.session_state.api_url,
        )

        if status == 201:
            show_success("Registration succeeded. You can now log in.")
            st.session_state.page = "Login"
        else:
            show_error(f"Registration failed: {payload}")


def login_page():
    st.header("Login")
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submit = st.form_submit_button("Login")

    if submit:
        if not email or not password:
            show_error("Email and password are required.")
            return

        status, payload = api_request(
            "/auth/login",
            method="POST",
            payload={"email": email, "password": password},
            base_url=st.session_state.api_url,
        )

        if status == 200:
            st.session_state.token = payload["access_token"]
            st.session_state.user_email = email
            st.session_state.page = "Notes"
            show_success("Logged in successfully.")
        else:
            show_error(f"Login failed: {payload}")


def create_note_form():
    st.subheader("Create note")
    with st.form("note_form"):
        title = st.text_input("Title", key="new_title")
        content = st.text_area("Content", key="new_content")
        submit = st.form_submit_button("Create note")

    if submit:
        if not title or not content:
            show_error("Title and content are required.")
            return

        status, payload = api_request(
            "/notes/",
            method="POST",
            payload={"title": title, "content": content},
            token=st.session_state.token,
            base_url=st.session_state.api_url,
        )

        if status == 201:
            show_success("Note created successfully.")
            clear_edit_state()
        else:
            show_error(f"Create note failed: {payload}")


def update_note_form():
    note_id = st.session_state.get("edit_note_id")
    if not note_id:
        return

    st.subheader("Edit note")
    with st.form("edit_note_form"):
        title = st.text_input(
            "Title", value=st.session_state.get("edit_title", ""), key="edit_title"
        )
        content = st.text_area(
            "Content",
            value=st.session_state.get("edit_content", ""),
            key="edit_content",
        )
        submit = st.form_submit_button("Save changes")

    if submit:
        if not title or not content:
            show_error("Title and content are required.")
            return

        status, payload = api_request(
            f"/notes/{note_id}",
            method="PUT",
            payload={"title": title, "content": content},
            token=st.session_state.token,
            base_url=st.session_state.api_url,
        )

        if status == 200:
            show_success("Note updated successfully.")
            clear_edit_state()
        else:
            show_error(f"Update failed: {payload}")

    if st.button("Cancel edit"):
        clear_edit_state()


def format_timestamp(value: str | None) -> str:
    if not value:
        return "unknown"

    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return value

    return parsed.strftime("%Y-%m-%d %H:%M")


def list_notes():
    st.subheader("My notes")
    status, payload = api_request(
        "/notes/",
        method="GET",
        token=st.session_state.token,
        base_url=st.session_state.api_url,
    )

    if status == 200 and isinstance(payload, list):
        if not payload:
            st.info("No notes yet.")
            return

        for note in payload:
            with st.expander(note["title"]):
                st.write(note["content"])
                created_at = format_timestamp(note.get("created_at"))
                updated_at = format_timestamp(note.get("updated_at"))
                st.caption(f"Created: {created_at} | Updated: {updated_at}")
                cols = st.columns([1, 1, 1])
                if cols[0].button("Edit", key=f"edit_{note['id']}"):
                    st.session_state.edit_note_id = note["id"]
                    st.session_state.edit_title = note["title"]
                    st.session_state.edit_content = note["content"]
                if cols[1].button("Delete", key=f"delete_{note['id']}"):
                    delete_note(note["id"])
                if cols[2].button("Refresh", key=f"refresh_{note['id']}"):
                    pass
    else:
        show_error(f"Could not load notes: {payload}")


def delete_note(note_id):
    status, payload = api_request(
        f"/notes/{note_id}",
        method="DELETE",
        token=st.session_state.token,
        base_url=st.session_state.api_url,
    )
    if status == 200:
        show_success("Note deleted successfully.")
        clear_edit_state()


def notes_page():
    if not st.session_state.token:
        st.warning("Please log in first to access notes.")
        return

    st.header("Notes")
    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.user_email = None
        clear_edit_state()
        st.session_state.page = "Login"

    if st.session_state.get("edit_note_id"):
        update_note_form()

    create_note_form()
    list_notes()


def app():
    st.set_page_config(page_title="NoteKeeper UI", page_icon="📝")
    st.title("NoteKeeper Streamlit UI")

    if "api_url" not in st.session_state:
        st.session_state.api_url = DEFAULT_API_URL
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "page" not in st.session_state:
        st.session_state.page = "Register"
    if "edit_note_id" not in st.session_state:
        st.session_state.edit_note_id = None
    if "edit_title" not in st.session_state:
        st.session_state.edit_title = ""
    if "edit_content" not in st.session_state:
        st.session_state.edit_content = ""

    st.sidebar.title("Navigation")
    st.session_state.page = st.sidebar.radio(
        "Menu", PAGES, index=PAGES.index(st.session_state.page)
    )
    st.sidebar.write("API URL")
    st.session_state.api_url = st.sidebar.text_input(
        "Backend API URL", value=st.session_state.api_url
    )

    if st.session_state.token:
        st.sidebar.success(f"Logged in as {st.session_state.user_email}")
    else:
        st.sidebar.info("Not logged in")

    if st.session_state.page == "Register":
        register_page()
    elif st.session_state.page == "Login":
        login_page()
    else:
        notes_page()


if __name__ == "__main__":
    app()
