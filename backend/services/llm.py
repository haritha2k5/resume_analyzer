from openai import OpenAI

client = OpenAI()   # now env WILL be found

def analyze_resume(text: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=text
    )
    return response.output_text
