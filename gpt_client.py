import os
import asyncio
from typing import Optional

OPENAI_MODEL_DEFAULT = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# We import lazily so the app can run without the package or API key (mock mode).
_client = None

async def _ensure_client():
    global _client
    if _client is None:
        try:
            from openai import OpenAI
            _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception:
            _client = None
    return _client

async def generate_reply(message: str, system_hint: Optional[str] = None) -> str:
    """Return a GPT reply. If no API key/client available -> return a mock answer."""
    client = await _ensure_client()
    if client is None:
        return f"(Mock) Ich habe deine Nachricht erhalten: '{message}'. In der Starter-Version antworte ich ohne GPT-Key."

    system_prompt = system_hint or (
        "Du bist ein professioneller, präziser Trading-Assistent. Erkläre sauber, gib keine Finanzberatung."
    )
    try:
        resp = client.chat.completions.create(
            model=OPENAI_MODEL_DEFAULT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            temperature=0.3,
        )
        return resp.choices[0].message.content
    except Exception as e:
        # Fallback to mock if anything goes wrong
        return f"(Mock) Antwort wegen Fehler im GPT-Client: {e}"
