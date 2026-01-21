from services.llm import analyze_resume
from utils.pdf_reader import extract_text
from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
load_dotenv()   # MUST be first line


app = FastAPI()


@app.get("/")
def root():
    return {"status": "API is running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), role: str = "Software Engineer Intern"):
    text = extract_text(file)
    result = analyze_resume(text, role)
    return {"analysis": result}
