"""PDF fayllarni yaratish va birlashtirish funksiyalari (reportlab, pypdf)."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from pypdf import PdfReader, PdfWriter


def create_pdf(
    file_path: str,
    title: str = None,
    paragraphs: list = None,
    overwrite: bool = False,
) -> dict:
    """Yangi PDF hujjat yaratadi (sarlavha + paragraflar bilan)."""
    if os.path.exists(file_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {file_path} (overwrite=True qiling)"}

    styles = getSampleStyleSheet()
    story = []

    if title:
        story.append(Paragraph(title, styles["Title"]))
        story.append(Spacer(1, 12))

    for para in paragraphs or []:
        story.append(Paragraph(para, styles["Normal"]))
        story.append(Spacer(1, 8))

    os.makedirs(os.path.dirname(os.path.abspath(file_path)) or ".", exist_ok=True)
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    doc.build(story or [Paragraph(" ", styles["Normal"])])

    return {"file_path": file_path, "status": "created", "paragraph_count": len(paragraphs or [])}


def merge_pdfs(file_paths: list, output_path: str, overwrite: bool = False) -> dict:
    """Bir nechta PDF faylni ketma-ket bitta faylga birlashtiradi."""
    if os.path.exists(output_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {output_path} (overwrite=True qiling)"}

    for p in file_paths:
        if not os.path.exists(p):
            return {"error": f"Fayl topilmadi: {p}"}

    writer = PdfWriter()
    for p in file_paths:
        reader = PdfReader(p)
        for page in reader.pages:
            writer.add_page(page)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        writer.write(f)

    return {"file_path": output_path, "status": "merged", "source_count": len(file_paths)}


def split_pdf(file_path: str, output_dir: str) -> dict:
    """PDF faylni har bir sahifa alohida faylga bo'linadi (page_1.pdf, page_2.pdf, ...)."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    os.makedirs(output_dir, exist_ok=True)
    reader = PdfReader(file_path)
    output_files = []

    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        out_path = os.path.join(output_dir, f"page_{i}.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
        output_files.append(out_path)

    return {"file_path": file_path, "status": "split", "output_files": output_files}
