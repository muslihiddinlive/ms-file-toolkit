"""DOCX (Word) fayllarni yaratish va tahrirlash (yozish) funksiyalari."""

import os
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_BREAK


def create_docx(
    file_path: str,
    title: str = None,
    paragraphs: list = None,
    table_data: list = None,
    overwrite: bool = False,
) -> dict:
    """Yangi Word (.docx) hujjat yaratadi.

    paragraphs: matn qatorlari ro'yxati (har biri alohida paragraf bo'ladi).
    table_data: jadval uchun 2-o'lchamli ro'yxat, masalan
        [["Ism", "Yosh"], ["Ali", "25"], ["Vali", "30"]] — birinchi qator sarlavha
        sifatida qalin (bold) qilib chiqariladi.
    """
    if os.path.exists(file_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {file_path} (overwrite=True qiling)"}

    doc = Document()

    if title:
        doc.add_heading(title, level=1)

    for para in paragraphs or []:
        doc.add_paragraph(para)

    if table_data:
        rows = len(table_data)
        cols = len(table_data[0]) if rows else 0
        if rows and cols:
            table = doc.add_table(rows=rows, cols=cols)
            table.style = "Light Grid Accent 1"
            for r, row_data in enumerate(table_data):
                for c, cell_value in enumerate(row_data):
                    cell = table.cell(r, c)
                    cell.text = str(cell_value)
                    if r == 0:
                        for p in cell.paragraphs:
                            for run in p.runs:
                                run.font.bold = True

    os.makedirs(os.path.dirname(os.path.abspath(file_path)) or ".", exist_ok=True)
    doc.save(file_path)

    return {
        "file_path": file_path,
        "status": "created",
        "paragraph_count": len(paragraphs or []),
        "table_added": bool(table_data),
    }


def append_docx_text(file_path: str, text: str, bold: bool = False) -> dict:
    """Mavjud Word hujjatining oxiriga yangi paragraf qo'shadi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    doc = Document(file_path)
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    doc.save(file_path)

    return {"file_path": file_path, "status": "appended", "paragraph_count": len(doc.paragraphs)}


def replace_docx_text(file_path: str, find: str, replace: str, save_as: str = None) -> dict:
    """Hujjatdagi barcha 'find' matnini 'replace' bilan almashtiradi.

    save_as berilmasa, asl faylning ustiga yoziladi.
    """
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    doc = Document(file_path)
    replacements = 0

    for p in doc.paragraphs:
        if find in p.text:
            for run in p.runs:
                if find in run.text:
                    run.text = run.text.replace(find, replace)
                    replacements += 1

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if find in cell.text:
                    cell.text = cell.text.replace(find, replace)
                    replacements += 1

    out_path = save_as or file_path
    doc.save(out_path)

    return {"file_path": out_path, "status": "replaced", "replacements": replacements}


def add_docx_heading(file_path: str, text: str, level: int = 1) -> dict:
    """Mavjud Word hujjatiga sarlavha (heading, 1-9 daraja) qo'shadi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}
    if not 0 <= level <= 9:
        return {"error": "level 0 dan 9 gacha bo'lishi kerak"}

    doc = Document(file_path)
    doc.add_heading(text, level=level)
    doc.save(file_path)
    return {"file_path": file_path, "status": "heading_added", "level": level}


def add_docx_image(file_path: str, image_path: str, width_inches: float = 6.0) -> dict:
    """Mavjud Word hujjatining oxiriga rasm qo'shadi."""
    if not os.path.exists(file_path):
        return {"error": f"Hujjat topilmadi: {file_path}"}
    if not os.path.exists(image_path):
        return {"error": f"Rasm fayli topilmadi: {image_path}"}

    doc = Document(file_path)
    doc.add_picture(image_path, width=Inches(width_inches))
    doc.save(file_path)
    return {"file_path": file_path, "status": "image_added", "image_path": image_path}


def add_docx_page_break(file_path: str) -> dict:
    """Mavjud Word hujjatining oxiriga sahifa bo'linishi (page break) qo'shadi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    doc = Document(file_path)
    p = doc.add_paragraph()
    run = p.add_run()
    run.add_break(WD_BREAK.PAGE)
    doc.save(file_path)
    return {"file_path": file_path, "status": "page_break_added"}
