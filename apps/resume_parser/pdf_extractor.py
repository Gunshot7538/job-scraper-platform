
import pdfplumber
from docx import Document
import io


def extract_text_from_file(file):
    """Extract text from PDF or DOCX file object"""
    file_name = file.name.lower()
    
    try:
        if file_name.endswith('.pdf'):
            return _extract_from_pdf(file)
        elif file_name.endswith(('.docx', '.doc')):
            return _extract_from_docx(file)
        else:
            return ""
    except Exception as e:
        print(f"Extraction error: {e}")
        return ""


def _extract_from_pdf(file):
    """Extract text from PDF"""
    text = ""
    file_bytes = file.read()
    
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    return text.strip()


def _extract_from_docx(file):
    """Extract text from DOCX"""
    file_bytes = file.read()
    doc = Document(io.BytesIO(file_bytes))
    
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    
    return text.strip()