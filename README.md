# Nova AI Partner

A simple personal AI partner built with Flask and the Groq API. It provides a clean chat interface, short-term conversation memory, reset chat, mobile-friendly design, and secure server-side API-key handling.

## Important security rule

Never paste your Groq API key into the source code or commit a `.env` file to GitHub. Store the key as an environment variable.

## Run locally

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and add your Groq API key.
5. Start the app:

```bash
python app.py
```

6. Open `http://localhost:5000`.

## Deploy from GitHub using Render

1. Push this project to a GitHub repository.
2. Sign in to Render and create a new Blueprint or Web Service from the repository.
3. Add `GROQ_API_KEY` as a secret environment variable.
4. Deploy.

GitHub Pages cannot safely run this application because the Groq API key must remain on a private server, not inside browser JavaScript.

## Main files

- `app.py`, Flask server and Groq integration
- `templates/index.html`, chat interface
- `static/style.css`, responsive design
- `static/app.js`, browser chat behaviour
- `render.yaml`, Render deployment configuration

## Licence

MIT
