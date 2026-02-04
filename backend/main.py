from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")
from fastapi import FastAPI, UploadFile, File
from backend.services.llm import analyze_resume
from backend.utils.pdf_reader import extract_text

app = FastAPI()

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    role: str = "Software Engineer Intern"
):
    text = extract_text(file)

    if not text.strip():
        return {"error": "No readable text found in resume"}

    return analyze_resume(text, role)
