"""ZIP arxiv yaratish va chiqarish (extract) funksiyalari (stdlib zipfile).

`extract_archive` **zip-slip** hujumidan himoyalangan: arxiv ichidagi hech
qanday fayl `output_dir` tashqarisiga chiqib keta olmaydi (masalan
"../../etc/passwd" nomli yozuv bo'lsa, rad etiladi).
"""

import os
import zipfile


def create_archive(output_path: str, file_paths: list, overwrite: bool = False) -> dict:
    """Berilgan fayllardan yangi ZIP arxiv yaratadi (fayllar arxiv ichida tekis, papkasiz saqlanadi)."""
    if os.path.exists(output_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {output_path} (overwrite=True qiling)"}

    for p in file_paths or []:
        if not os.path.exists(p):
            return {"error": f"Fayl topilmadi: {p}"}

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in file_paths or []:
            zf.write(p, arcname=os.path.basename(p))

    return {"file_path": output_path, "status": "created", "entry_count": len(file_paths or [])}


def extract_archive(file_path: str, output_dir: str) -> dict:
    """ZIP arxivni papkaga chiqaradi (zip-slip himoyasi bilan)."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}
    if not zipfile.is_zipfile(file_path):
        return {"error": f"Fayl to'g'ri ZIP arxiv emas: {file_path}"}

    os.makedirs(output_dir, exist_ok=True)
    out_base = os.path.abspath(output_dir)
    extracted = []

    with zipfile.ZipFile(file_path, "r") as zf:
        for member in zf.infolist():
            target = os.path.abspath(os.path.join(out_base, member.filename))
            if os.path.commonpath([target, out_base]) != out_base:
                return {"error": f"Xavfsizlik xatosi: arxiv yozuvi papkadan tashqariga chiqadi: {member.filename}"}

        zf.extractall(out_base)
        extracted = zf.namelist()

    return {"file_path": file_path, "status": "extracted", "output_dir": out_base, "extracted_files": extracted}
