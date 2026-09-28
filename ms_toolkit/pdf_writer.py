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


# ---------- Rasmlardan PDF (LaborantRobot'dagi images_to_pdf mantiqi asosida) ----------

_A4_PORTRAIT_150DPI = (1240, 1754)  # A4 @ 150 DPI, piksellarda
MAX_PDF_IMAGES = 200
_MAX_SIDE_ORIGINAL = 3000  # "original" rejimda hajm portlab ketmasligi uchun


def _load_flat_rgb(path: str):
    """Rasmni ochib, EXIF aylanishini qo'llaydi va shaffoflikni OQ fonga yotqizadi
    (oddiy .convert('RGB') shaffof PNG'ni QORA qilib yuborardi)."""
    from PIL import Image, ImageOps

    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        rgba = img.convert("RGBA")
        background = Image.new("RGB", rgba.size, (255, 255, 255))
        background.paste(rgba, mask=rgba.split()[-1])
        return background
    return img.convert("RGB")


def _fit_on_a4(img, margin: int = 40):
    from PIL import Image

    landscape = img.width > img.height
    page_w, page_h = _A4_PORTRAIT_150DPI[::-1] if landscape else _A4_PORTRAIT_150DPI
    canvas = Image.new("RGB", (page_w, page_h), (255, 255, 255))
    max_w, max_h = page_w - 2 * margin, page_h - 2 * margin
    ratio = min(max_w / img.width, max_h / img.height)  # kichik rasmni ham A4'ga moslab kattalashtiradi
    new_size = (max(1, int(img.width * ratio)), max(1, int(img.height * ratio)))
    resized = img.resize(new_size, Image.LANCZOS)
    canvas.paste(resized, ((page_w - new_size[0]) // 2, (page_h - new_size[1]) // 2))
    return canvas


def create_pdf_from_images(
    image_paths: list,
    output_path: str,
    page_size: str = "original",
    overwrite: bool = False,
) -> dict:
    """Bir yoki bir nechta rasmdan PDF yaratadi (har rasm — alohida sahifa).

    page_size="original": har sahifa o'z rasmi o'lchamida (LaborantRobot'dagidek);
    page_size="a4": rasm A4 sahifa o'rtasiga (yo'nalishi avtomatik) sig'diriladi.
    """
    if page_size not in ("original", "a4"):
        return {"error": "page_size: 'original' yoki 'a4' bo'lishi kerak"}
    if not image_paths:
        return {"error": "image_paths bo'sh — kamida bitta rasm kerak"}
    if len(image_paths) > MAX_PDF_IMAGES:
        return {"error": f"Rasmlar juda ko'p: {len(image_paths)} (ruxsat: {MAX_PDF_IMAGES})"}
    if os.path.exists(output_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {output_path} (overwrite=True qiling)"}

    pages = []
    for p in image_paths:
        if not os.path.exists(p):
            return {"error": f"Fayl topilmadi: {p}"}
        try:
            img = _load_flat_rgb(p)
        except Exception as e:  # noqa: BLE001 — rasm bo'lmagan/buzilgan fayl
            return {"error": f"Rasmni ochib bo'lmadi: {p} ({type(e).__name__}: {e})"}
        if page_size == "a4":
            img = _fit_on_a4(img)
        else:
            img.thumbnail((_MAX_SIDE_ORIGINAL, _MAX_SIDE_ORIGINAL))
        pages.append(img)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    pages[0].save(output_path, "PDF", save_all=True, append_images=pages[1:], resolution=150.0)

    return {
        "file_path": output_path,
        "status": "created",
        "page_count": len(pages),
        "page_size": page_size,
    }
