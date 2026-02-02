from pypdf import PdfReader

def extract_text(file):
    try:
        file.file.seek(0)
        reader = PdfReader(file.file)

        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        return text

    except Exception:
        return ""

