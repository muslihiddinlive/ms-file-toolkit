"""Rasm fayllarini konvertatsiya qilish va thumbnail yaratish funksiyalari (Pillow)."""

import os
from PIL import Image


def convert_image(
    file_path: str,
    output_path: str,
    target_format: str = None,
    width: int = None,
    height: int = None,
    overwrite: bool = False,
) -> dict:
    """Rasmni boshqa formatga o'giradi va/yoki o'lchamini o'zgartiradi.

    `target_format` berilmasa, `output_path` kengaytmasidan avtomatik aniqlanadi
    (masalan .jpg -> JPEG, .png -> PNG, .webp -> WEBP).
    `width`/`height` — ikkalasi berilsa aniq o'lchamga, faqat bittasi berilsa
    proporsional ravishda o'zgartiriladi.
    """
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}
    if os.path.exists(output_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {output_path} (overwrite=True qiling)"}

    with Image.open(file_path) as img:
        if width or height:
            orig_w, orig_h = img.size
            if width and height:
                new_size = (width, height)
            elif width:
                new_size = (width, int(orig_h * width / orig_w))
            else:
                new_size = (int(orig_w * height / orig_h), height)
            img = img.resize(new_size)

        fmt = (target_format or os.path.splitext(output_path)[1].lstrip(".") or "PNG").upper()
        if fmt == "JPG":
            fmt = "JPEG"
        if fmt == "JPEG" and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
        img.save(output_path, format=fmt)
        final_size = img.size

    return {
        "file_path": output_path,
        "status": "converted",
        "format": fmt,
        "width": final_size[0],
        "height": final_size[1],
    }


def create_thumbnail(file_path: str, output_path: str, size: int = 128, overwrite: bool = False) -> dict:
    """Rasmdan (proporsiyani saqlab) kvadrat chegarali thumbnail yaratadi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}
    if os.path.exists(output_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {output_path} (overwrite=True qiling)"}

    with Image.open(file_path) as img:
        img = img.copy()
        img.thumbnail((size, size))
        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
        img.save(output_path)
        final_size = img.size

    return {"file_path": output_path, "status": "created", "width": final_size[0], "height": final_size[1]}
