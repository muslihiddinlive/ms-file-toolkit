"""CSV fayllarni o'qish funksiyalari (stdlib csv — qo'shimcha dependency shart emas)."""

import csv
import os


def read_csv_data(file_path: str, max_rows: int = None, delimiter: str = ",") -> dict:
    """CSV fayldan sarlavha va qatorlarni o'qiydi (birinchi qator sarlavha deb olinadi)."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)

    headers = rows[0] if rows else []
    data_rows = rows[1:]
    if max_rows is not None:
        data_rows = data_rows[:max_rows]

    return {
        "file_path": file_path,
        "headers": headers,
        "rows": data_rows,
        "row_count": len(data_rows),
    }


def get_csv_summary(file_path: str, delimiter: str = ",") -> dict:
    """CSV faylning umumiy tuzilishi: ustunlar, qatorlar soni, dastlabki 5 qator."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)

    headers = rows[0] if rows else []
    data_rows = rows[1:]

    return {
        "file_path": file_path,
        "headers": headers,
        "column_count": len(headers),
        "row_count": len(data_rows),
        "sample_rows": data_rows[:5],
    }
