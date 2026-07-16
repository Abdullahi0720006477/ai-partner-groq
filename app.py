import os
from flask import Flask, jsonify, render_template, request, session
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-in-production")

SYSTEM_PROMPT = """You are Nova, a supportive AI partner. Help the user plan, learn, write, solve problems, and stay organised. Be warm, honest, practical, and concise. Ask useful questions only when necessary. Never claim to perform actions you cannot actually perform."""

MAX_HISTORY = 16


def get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured.")
    return Groq(api_key=api_key)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    history = session.get("history", [])
    history.append({"role": "user", "content": message})
    history = history[-MAX_HISTORY:]

    try:
        completion = get_client().chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *history],
            temperature=0.7,
            max_completion_tokens=700,
        )
        reply = completion.choices[0].message.content or "I could not generate a reply."
    except Exception as exc:
        app.logger.exception("Groq request failed")
        return jsonify({"error": f"AI request failed: {exc}"}), 500

    history.append({"role": "assistant", "content": reply})
    session["history"] = history[-MAX_HISTORY:]
    return jsonify({"reply": reply})


@app.post("/api/reset")
def reset():
    session.pop("history", None)
    return jsonify({"ok": True})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
