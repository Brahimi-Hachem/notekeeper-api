# Phase 07 — GUI / Integration

## Goal
Build a simple user interface for the NoteKeeper API and optionally provide a conversational access channel via Telegram or WhatsApp.

## Option 1: Streamlit web UI

The Streamlit UI now lives in a separate repository, `notekeeper-ui`.

This is the fastest path to a GUI:

- Streamlit is Python-native and easy to connect to the existing API.
- It can run locally or be deployed separately.
- It provides forms for registration, login, note creation, and note listing.

### UI features

- Register new user
- Login and store JWT
- Create notes
- List notes
- View note details
- Edit and delete notes

### Why Streamlit?

- Minimal frontend code.
- No React/Vue learning curve required.
- Works well for prototypes and demos.

## Option 2: Telegram interface

If a conversational interface is preferred, Telegram is a good first choice:

- Free bot API.
- Simple webhook or polling integration.
- Can be used as a desktop/mobile “GUI.”

### Telegram flow

- User sends `/register` or `/login`.
- Bot prompts for credentials.
- Bot stores the JWT temporarily per chat.
- User sends commands like `/newnote`, `/listnotes`, `/getnote <id>`.

## Option 3: WhatsApp interface

WhatsApp typically requires a third-party provider or API gateway.
It is more complex and less free than Telegram, so it is better as a later extension.

## Recommended path

1. Build a Streamlit UI first.
2. If more conversational access is desired, add a Telegram bot next.

## Phase 07 deliverables

- A Streamlit app in `ui/streamlit_app.py` or `streamlit_app.py`.
- README instructions for running the UI.
- Example API usage from the UI.
- Optional Telegram bot documentation and code.
