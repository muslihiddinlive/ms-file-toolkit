"""OpenDocument fayllarni (.odt/.ods/.odp) yaratish funksiyalari (odfpy kutubxonasi)."""

import os
from odf.opendocument import OpenDocumentText, OpenDocumentSpreadsheet, OpenDocumentPresentation
from odf.text import P, H
from odf.table import Table, TableRow, TableCell
from odf.style import MasterPage, PageLayout
from odf.draw import Page, Frame, TextBox


def create_odt(
    file_path: str,
    title: str = None,
    paragraphs: list = None,
    overwrite: bool = False,
) -> dict:
    """Yangi OpenDocument Text (.odt) hujjat yaratadi (sarlavha + paragraflar bilan)."""
    if os.path.exists(file_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {file_path} (overwrite=True qiling)"}

    doc = OpenDocumentText()
    if title:
        doc.text.addElement(H(outlinelevel=1, text=title))
    for para in paragraphs or []:
        doc.text.addElement(P(text=para))

    os.makedirs(os.path.dirname(os.path.abspath(file_path)) or ".", exist_ok=True)
    doc.save(file_path)

    return {"file_path": file_path, "status": "created", "paragraph_count": len(paragraphs or [])}


def create_ods(
    file_path: str,
    rows: list,
    sheet_name: str = "Sheet1",
    overwrite: bool = False,
) -> dict:
    """Yangi OpenDocument Spreadsheet (.ods) fayl yaratadi (2-o'lchamli rows ro'yxatidan)."""
    if os.path.exists(file_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {file_path} (overwrite=True qiling)"}

    doc = OpenDocumentSpreadsheet()
    table = Table(name=sheet_name)
    for row_data in rows or []:
        tr = TableRow()
        for val in row_data:
            tc = TableCell(valuetype="string")
            tc.addElement(P(text=str(val)))
            tr.addElement(tc)
        table.addElement(tr)
    doc.spreadsheet.addElement(table)

    os.makedirs(os.path.dirname(os.path.abspath(file_path)) or ".", exist_ok=True)
    doc.save(file_path)

    return {"file_path": file_path, "status": "created", "row_count": len(rows or [])}


def create_odp(
    file_path: str,
    slides: list,
    overwrite: bool = False,
) -> dict:
    """Yangi OpenDocument Presentation (.odp) fayl yaratadi.

    `slides` — har biri bitta slaydning matni bo'lgan string'lar ro'yxati.
    """
    if os.path.exists(file_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {file_path} (overwrite=True qiling)"}

    doc = OpenDocumentPresentation()
    layout = PageLayout(name="PL1")
    doc.automaticstyles.addElement(layout)
    master = MasterPage(name="Default", pagelayoutname=layout)
    doc.masterstyles.addElement(master)

    for i, slide_text in enumerate(slides or [], start=1):
        page = Page(name=f"Slide{i}", masterpagename="Default")
        frame = Frame(width="24cm", height="14cm", x="1cm", y="1cm")
        tb = TextBox()
        tb.addElement(P(text=slide_text))
        frame.addElement(tb)
        page.addElement(frame)
        doc.presentation.addElement(page)

    os.makedirs(os.path.dirname(os.path.abspath(file_path)) or ".", exist_ok=True)
    doc.save(file_path)

    return {"file_path": file_path, "status": "created", "slide_count": len(slides or [])}
