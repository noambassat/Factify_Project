# utils/pdf_loader.py
import fitz  # PyMuPDF
import os
import re
from .document_types import Document

def read_pdf(path):
    pdf = fitz.open(path)
    return "".join([p.get_text() for p in pdf]).strip()

def get_true_label(filename):
    match = re.match(r'^([A-Za-zא-ת]+)', filename)
    return match.group(1).capitalize() if match else "Unknown"

def load_documents(folder):
    docs = []
    for fname in os.listdir(folder):
        if not fname.lower().endswith(".pdf") or fname.lower().startswith("home"):
            continue
        path = os.path.join(folder, fname)
        text = read_pdf(path)
        doc = Document(
            filename=fname,
            raw_text=text,
            true_label=get_true_label(fname),
            metadata={
                "num_pages": len(fitz.open(path)),
                "num_words": len(text.split())
            }
        )
        docs.append(doc)
    return docs
