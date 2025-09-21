import os
import json
import logging
from typing import Optional
import requests

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gemini-pro"  # placeholder; change to the exact model name if needed

def generate_text(prompt: str, model: str = DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens: int = 1000, temperature: float = 0.3) -> str:
    """Generate text using Google Gemini (Generative Language API) via REST.

    This is a minimal wrapper that uses an API key. For production, prefer
    the official Google client libraries and proper OAuth credentials.
    """
    try:
        if api_key is None:
            api_key = os.getenv('GOOGLE_GEMINI_API_KEY')

        if not api_key:
            raise ValueError("GOOGLE_GEMINI_API_KEY is not set")

        url = f"https://generativelanguage.googleapis.com/v1beta2/models/{model}:generate?key={api_key}"

        body = {
            "prompt": {
                "text": prompt
            },
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }

        headers = {
            "Content-Type": "application/json"
        }

        resp = requests.post(url, headers=headers, data=json.dumps(body), timeout=30)
        resp.raise_for_status()

        data = resp.json()

        # The response format may vary; try to extract text safely
        if 'candidates' in data and isinstance(data['candidates'], list) and len(data['candidates']) > 0:
            return data['candidates'][0].get('content', '').strip()

        # Fallback: try common field
        return data.get('output', {}).get('text', '') or json.dumps(data)

    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return ""
