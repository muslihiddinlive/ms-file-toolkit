"""CSV fayllarni yaratish va qator qo'shish funksiyalari (stdlib csv)."""

import csv
import os


def create_csv(
    file_path: str,
    headers: list = None,
    rows: list = None,
    delimiter: str = ",",
    overwrite: bool = False,
) -> dict:
    """Yangi CSV fayl yaratadi (ixtiyoriy sarlavha va boshlang'ich qatorlar bilan)."""
    if os.path.exists(file_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {file_path} (overwrite=True qiling)"}

    os.makedirs(os.path.dirname(os.path.abspath(file_path)) or ".", exist_ok=True)
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=delimiter)
        if headers:
            writer.writerow(headers)
        for row in rows or []:
            writer.writerow(row)

    return {"file_path": file_path, "status": "created", "row_count": len(rows or [])}


def append_csv_rows(file_path: str, rows: list, delimiter: str = ",") -> dict:
    """Mavjud CSV faylning oxiriga yangi qatorlar qo'shadi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}
    if not rows:
        return {"error": "rows bo'sh — qo'shiladigan qator yo'q"}

    with open(file_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=delimiter)
        for row in rows:
            writer.writerow(row)

    return {"file_path": file_path, "status": "appended", "added_row_count": len(rows)}
