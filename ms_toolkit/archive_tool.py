"""ZIP arxivlarni o'qish funksiyalari (stdlib zipfile — qo'shimcha dependency shart emas)."""

import os
import zipfile


def list_archive_contents(file_path: str) -> dict:
    """ZIP arxiv ichidagi barcha fayllar ro'yxatini (nom, hajm, siqilgan hajm) qaytaradi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}
    if not zipfile.is_zipfile(file_path):
        return {"error": f"Fayl to'g'ri ZIP arxiv emas: {file_path}"}

    entries = []
    with zipfile.ZipFile(file_path, "r") as zf:
        for info in zf.infolist():
            entries.append(
                {
                    "name": info.filename,
                    "size": info.file_size,
                    "compressed_size": info.compress_size,
                    "is_dir": info.is_dir(),
                }
            )

    return {"file_path": file_path, "entries": entries, "entry_count": len(entries)}


def read_archive_file(file_path: str, entry_name: str, encoding: str = "utf-8") -> dict:
    """ZIP arxiv ichidagi bitta matnli faylni o'qib, matnini qaytaradi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}
    if not zipfile.is_zipfile(file_path):
        return {"error": f"Fayl to'g'ri ZIP arxiv emas: {file_path}"}

    with zipfile.ZipFile(file_path, "r") as zf:
        if entry_name not in zf.namelist():
            return {"error": f"Arxiv ichida topilmadi: {entry_name}"}
        try:
            content = zf.read(entry_name).decode(encoding)
        except UnicodeDecodeError:
            return {"error": f"Fayl matn sifatida o'qilmadi (binary bo'lishi mumkin): {entry_name}"}

    return {"file_path": file_path, "entry_name": entry_name, "text": content}
