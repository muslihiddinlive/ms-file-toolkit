"""PPTX (PowerPoint) fayllarni yaratish va tahrirlash (yozish) funksiyalari."""

import os
from pptx import Presentation
from pptx.util import Inches, Emu


def create_pptx(file_path: str, title: str = None, subtitle: str = None, overwrite: bool = False) -> dict:
    """Yangi PowerPoint (.pptx) taqdimot yaratadi (title-slide bilan boshlanadi)."""
    if os.path.exists(file_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {file_path} (overwrite=True qiling)"}

    prs = Presentation()
    layout = prs.slide_layouts[0]  # Title Slide
    slide = prs.slides.add_slide(layout)
    if title:
        slide.shapes.title.text = title
    if subtitle and len(slide.placeholders) > 1:
        slide.placeholders[1].text = subtitle

    os.makedirs(os.path.dirname(os.path.abspath(file_path)) or ".", exist_ok=True)
    prs.save(file_path)

    return {"file_path": file_path, "status": "created", "slide_count": len(prs.slides)}


def add_pptx_slide(
    file_path: str,
    title: str = None,
    bullet_points: list = None,
    notes: str = None,
) -> dict:
    """Mavjud taqdimotga sarlavha + bullet-point matnli yangi slayd qo'shadi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    prs = Presentation(file_path)
    layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(layout)

    if title and slide.shapes.title:
        slide.shapes.title.text = title

    if bullet_points:
        body = slide.placeholders[1]
        tf = body.text_frame
        tf.text = bullet_points[0]
        for point in bullet_points[1:]:
            p = tf.add_paragraph()
            p.text = point

    if notes:
        slide.notes_slide.notes_text_frame.text = notes

    prs.save(file_path)
    return {"file_path": file_path, "status": "slide_added", "slide_count": len(prs.slides)}


def add_pptx_image(
    file_path: str,
    image_path: str,
    slide_index: int = None,
    left_inches: float = 1.0,
    top_inches: float = 1.5,
    width_inches: float = None,
) -> dict:
    """Taqdimotga rasm qo'shadi.

    slide_index berilmasa, oxirgi slaydga qo'shiladi. width_inches berilmasa,
    rasm o'z asl o'lchamida (piksellardan EMU'ga o'girib) qo'yiladi.
    """
    if not os.path.exists(file_path):
        return {"error": f"Taqdimot topilmadi: {file_path}"}
    if not os.path.exists(image_path):
        return {"error": f"Rasm fayli topilmadi: {image_path}"}

    prs = Presentation(file_path)
    if not prs.slides:
        return {"error": "Taqdimotda hech qanday slayd yo'q"}

    idx = slide_index if slide_index is not None else len(prs.slides) - 1
    if not 0 <= idx < len(prs.slides):
        return {"error": f"Noto'g'ri slide_index: {idx} (jami slaydlar: {len(prs.slides)})"}

    slide = prs.slides[idx]
    kwargs = {"width": Inches(width_inches)} if width_inches else {}
    slide.shapes.add_picture(image_path, Inches(left_inches), Inches(top_inches), **kwargs)

    prs.save(file_path)
    return {"file_path": file_path, "status": "image_added", "slide_index": idx}


def set_pptx_background_color(file_path: str, slide_index: int, hex_color: str) -> dict:
    """Belgilangan slaydning fon rangini o'rnatadi (hex_color: masalan 'FFFFFF')."""
    from pptx.dml.color import RGBColor

    if not os.path.exists(file_path):
        return {"error": f"Taqdimot topilmadi: {file_path}"}

    prs = Presentation(file_path)
    if not 0 <= slide_index < len(prs.slides):
        return {"error": f"Noto'g'ri slide_index: {slide_index} (jami slaydlar: {len(prs.slides)})"}

    slide = prs.slides[slide_index]
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(hex_color.lstrip("#").upper())

    prs.save(file_path)
    return {"file_path": file_path, "status": "background_set", "slide_index": slide_index}
