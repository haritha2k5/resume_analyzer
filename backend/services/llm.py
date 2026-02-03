import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def analyze_resume(text: str, role: str) -> dict:
    prompt = f"""
You are an expert resume reviewer.

Analyze the resume below for the role of {role}.

Return STRICTLY valid JSON with this structure:
{{
  "resume_score": number (0-10),
  "strengths": [strings],
  "improvements": [strings],
  "missing_requirements": [strings],
  "suggestions": [strings]
}}

Resume:
{text}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()

        raw = response.json().get("response", "").strip()

        # Try strict JSON parse
        return json.loads(raw)

    except json.JSONDecodeError:
        return {
            "error": "Model returned invalid JSON",
            "raw_output": raw
        }
    except Exception as e:
        return {
            "error": str(e)
        }
