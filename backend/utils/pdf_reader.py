from pypdf import PdfReader

def extract_text(file):
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
