from dotenv import load_dotenv
from pathlib import Path

# explicitly load backend/.env
load_dotenv(Path(__file__).parent / ".env")

from fastapi import FastAPI, UploadFile, File
from backend.services.llm import analyze_resume
from backend.utils.pdf_reader import extract_text

app = FastAPI()

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        text = extract_text(file)

        if not text.strip():
            return {"error": "No readable text found in PDF"}

        result = analyze_resume(text)
        return {"analysis": result}

    except Exception as e:
        return {"error": str(e)}


