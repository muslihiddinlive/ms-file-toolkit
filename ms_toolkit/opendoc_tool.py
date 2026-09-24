"""OpenDocument fayllarni (.odt/.ods/.odp) o'qish funksiyalari (odfpy kutubxonasi).

Talab: `pip install odfpy` (LibreOffice/OpenOffice hujjatlari uchun ochiq standart).
"""

import os
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.draw import Page
from odf import teletype


def read_odt_text(file_path: str) -> dict:
    """OpenDocument Text (.odt) fayldan barcha matnni hujjat tartibida o'qiydi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    doc = load(file_path)
    lines = [teletype.extractText(child) for child in doc.text.childNodes]
    lines = [line for line in lines if line]

    return {"file_path": file_path, "text": "\n".join(lines), "paragraph_count": len(lines)}


def get_ods_sheet_names(file_path: str) -> dict:
    """OpenDocument Spreadsheet (.ods) fayldagi barcha varaq nomlarini qaytaradi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    doc = load(file_path)
    names = [t.getAttribute("name") for t in doc.getElementsByType(Table)]
    return {"file_path": file_path, "sheet_names": names, "sheet_count": len(names)}


def read_ods_data(file_path: str, sheet_name: str = None, max_rows: int = None) -> dict:
    """OpenDocument Spreadsheet (.ods) faylidan varaq ma'lumotlarini o'qiydi.

    sheet_name berilmasa, birinchi varaq o'qiladi.
    """
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    doc = load(file_path)
    tables = doc.getElementsByType(Table)
    if not tables:
        return {"error": "Faylda hech qanday varaq topilmadi"}

    table = tables[0]
    if sheet_name:
        matches = [t for t in tables if t.getAttribute("name") == sheet_name]
        if not matches:
            return {"error": f"Varaq topilmadi: {sheet_name}"}
        table = matches[0]

    rows_out = []
    for row in table.getElementsByType(TableRow):
        cells = row.getElementsByType(TableCell)
        rows_out.append([teletype.extractText(c) for c in cells])
        if max_rows is not None and len(rows_out) >= max_rows:
            break

    return {
        "file_path": file_path,
        "sheet_name": table.getAttribute("name"),
        "rows": rows_out,
        "row_count": len(rows_out),
    }


def read_odp_text(file_path: str) -> dict:
    """OpenDocument Presentation (.odp) fayldan har bir slayd matnini o'qiydi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    doc = load(file_path)
    slides = doc.getElementsByType(Page)
    slide_texts = [teletype.extractText(p) for p in slides]

    return {
        "file_path": file_path,
        "slide_count": len(slides),
        "slides": slide_texts,
        "text": "\n\n".join(slide_texts),
    }


def get_odp_slide_count(file_path: str) -> dict:
    """OpenDocument Presentation (.odp) fayldagi slaydlar sonini qaytaradi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    doc = load(file_path)
    return {"file_path": file_path, "slide_count": len(doc.getElementsByType(Page))}
