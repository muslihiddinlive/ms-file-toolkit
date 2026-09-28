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


def extract_pdf_images(
    file_path: str,
    output_dir: str,
    min_width: int = 64,
    min_height: int = 64,
    max_images: int = 200,
) -> dict:
    """PDF ichiga joylangan rasmlarni alohida fayllar qilib chiqaradi (PyMuPDF).

    Bir xil rasm bir necha sahifada takrorlansa (logotip va h.k.) — faqat bir marta
    saqlanadi. Juda kichik rasmlar (ikonka/ajratgich chiziqlar) o'tkazib yuboriladi.
    Sahifaning O'ZINI rasmga aylantirish kerak bo'lsa — `convert_pdf_to_images`.
    """
    import fitz

    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    doc = fitz.open(file_path)
    try:
        if doc.needs_pass:
            return {"error": "PDF parol bilan himoyalangan — avval parolni olib tashlash kerak"}

        os.makedirs(output_dir, exist_ok=True)
        saved, seen, skipped_small = [], set(), 0

        for page_index in range(len(doc)):
            if len(saved) >= max_images:
                break
            for img_no, info in enumerate(doc[page_index].get_images(full=True), start=1):
                xref = info[0]
                if xref in seen:
                    continue
                seen.add(xref)
                if len(saved) >= max_images:
                    break

                raw = doc.extract_image(xref)
                width, height = raw.get("width", 0), raw.get("height", 0)
                if width < min_width or height < min_height:
                    skipped_small += 1
                    continue

                name_base = f"page{page_index + 1}_img{img_no}"
                # Oddiy (maskasiz, RGB/kulrang) jpeg/png — asl baytlarni o'zgartirmay yozamiz;
                # aks holda (CMYK, shaffoflik-maskasi, jpx va h.k.) — Pixmap orqali PNG'ga.
                if raw.get("smask", 0) == 0 and raw.get("colorspace") in (1, 3) and raw["ext"] in ("jpeg", "png"):
                    ext = "jpg" if raw["ext"] == "jpeg" else "png"
                    out_path = os.path.join(output_dir, f"{name_base}.{ext}")
                    with open(out_path, "wb") as f:
                        f.write(raw["image"])
                else:
                    pix = fitz.Pixmap(doc, xref)
                    if raw.get("smask", 0):
                        pix = fitz.Pixmap(pix, fitz.Pixmap(doc, raw["smask"]))
                    if pix.n - pix.alpha >= 4:  # CMYK -> RGB
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    ext = "png"
                    out_path = os.path.join(output_dir, f"{name_base}.png")
                    pix.save(out_path)
                    pix = None

                saved.append({"path": out_path, "page": page_index + 1, "width": width, "height": height, "format": ext})

        result = {
            "file_path": file_path,
            "output_dir": output_dir,
            "image_count": len(saved),
            "images": saved,
            "skipped_small": skipped_small,
            "page_count": len(doc),
        }
        if not saved:
            result["note"] = (
                "Ichki rasm topilmadi. Agar PDF skaner qilingan bo'lsa yoki sahifalarni rasm sifatida "
                "kerak bo'lsa — convert_pdf_to_images ishlating."
            )
        return result
    finally:
        doc.close()
