"""
Resume analysis via Groq. Set GROQ_API_KEY from console.groq.com
"""
import os
import requests
import json

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"

def _build_prompt(text: str, role: str) -> str:
    return f"""Analyze the resume for the role of {role}.

Return ONLY valid JSON in this exact structure (no markdown, no extra text):
{{
  "resume_score": <number 0-10>,
  "strengths": ["item1", "item2"],
  "improvements": ["item1", "item2"],
  "missing_requirements": ["item1", "item2"],
  "suggestions": ["item1", "item2"]
}}

Resume:
{text[:6000]}"""


def _parse_json_response(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    return json.loads(raw)


def analyze_resume(text: str, role: str) -> dict:
    prompt = _build_prompt(text, role)
    raw = ""

    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return {"error": "GROQ_API_KEY environment variable not set"}

        resp = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "max_tokens": 1024,
            },
            timeout=30,
        )
        resp.raise_for_status()
        raw = resp.json()["choices"][0]["message"]["content"]

        return _parse_json_response(raw)

    except json.JSONDecodeError as e:
        return {"error": "Model returned invalid JSON", "raw_output": raw, "parse_error": str(e)}
    except Exception as e:
        return {"error": str(e)}
