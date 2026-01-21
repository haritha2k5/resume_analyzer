from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_resume(text, role):
    prompt = f"""
You are a recruiter.
Review this resume for a {role} role.
Give:
- Strengths
- Missing skills
- Suggestions to improve

Resume:
{text}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text
