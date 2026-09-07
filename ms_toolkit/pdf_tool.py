"""PDF fayllarni o'qish funksiyalari (pdfplumber — matn/jadval, pypdf — metama'lumot)."""

import os
import pdfplumber
from pypdf import PdfReader


def read_pdf_text(file_path: str, max_pages: int = None) -> dict:
    """PDF fayldan barcha (yoki birinchi max_pages ta) sahifa matnini o'qiydi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    pages_text = []
    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages[:max_pages] if max_pages else pdf.pages
        for i, page in enumerate(pages):
            pages_text.append(page.extract_text() or "")

    return {
        "file_path": file_path,
        "page_count": len(pages_text),
        "text": "\n\n".join(pages_text),
    }


def read_pdf_tables(file_path: str) -> dict:
    """PDF fayldagi har bir sahifadan jadvallarni ajratib oladi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    all_tables = []
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            for table in page.extract_tables():
                all_tables.append({"page": page_num, "table": table})

    return {"file_path": file_path, "table_count": len(all_tables), "tables": all_tables}


def get_pdf_metadata(file_path: str) -> dict:
    """PDF faylning metama'lumotini (sarlavha, muallif, sahifalar soni) qaytaradi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    reader = PdfReader(file_path)
    meta = reader.metadata or {}

    return {
        "file_path": file_path,
        "page_count": len(reader.pages),
        "title": meta.get("/Title"),
        "author": meta.get("/Author"),
        "subject": meta.get("/Subject"),
        "creator": meta.get("/Creator"),
        "encrypted": reader.is_encrypted,
    }
