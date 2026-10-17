import os
import fitz
from docx import Document


def extract_text_from_pdf(file_path):
    """Extract plain text from a PDF file using PyMuPDF."""
    text_parts = []
    with fitz.open(file_path) as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "\n".join(text_parts).strip()


def extract_text_from_docx(file_path):
    """Extract plain text from a DOCX file using python-docx."""
    document = Document(file_path)
    paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs).strip()


def extract_resume_text(file_path):
    """Extract text from a resume file based on its extension."""
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)
    if extension == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError("Unsupported file format. Only PDF and DOCX are allowed.")
