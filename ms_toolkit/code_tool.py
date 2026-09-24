"""
Kod va matn fayllarini o'qish/yaratish/tahrirlash funksiyalari.

Word/Excel/PowerPoint kabi binary formatlardan farqli o'laroq, bu yerdagi
fayllar oddiy matn (plain text) sifatida saqlanadi: .py, .js, .ts, .html,
.css, .json, .csv, .md, .txt, .yaml va shunga o'xshash kengaytmalar.

Xavfsizlik eslatmasi: bu modul ixtiyoriy matnni diskka yozadi va ixtiyoriy
matn faylini o'qiydi. registry.py orqali chaqirilganda file_path/save_as/
output_path qiymatlari avtomatik ravishda security.resolve_safe_path()
orqali tekshiriladi (MS_TOOLKIT_BASE_DIR bilan). Kod bajarilmaydi — faqat
matn sifatida o'qiladi/yoziladi.
"""

import os

# Juda katta fayllarni tasodifan butunlay o'qib, javobni portlatib
# yubormaslik uchun standart chegara (belgilar soni).
_DEFAULT_MAX_CHARS = 200_000

_TEXT_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".html", ".htm", ".css", ".scss",
    ".json", ".csv", ".tsv", ".txt", ".md", ".yaml", ".yml", ".toml",
    ".ini", ".cfg", ".sh", ".bash", ".sql", ".xml", ".java", ".c", ".cpp",
    ".h", ".hpp", ".go", ".rs", ".php", ".rb", ".kt", ".swift", ".env",
}


def _read_lines(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.readlines()


def read_code_file(file_path: str, max_chars: int = _DEFAULT_MAX_CHARS) -> dict:
    """Kod/matn faylini o'qib, mazmunini qatorlar bilan birga qaytaradi.

    max_chars: shu belgi sonidan ko'p bo'lsa, matn kesib qo'yiladi
    (truncated=True bilan belgilanadi), lekin line_count to'liq hisoblanadi.
    """
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}
    if os.path.isdir(file_path):
        return {"error": f"Bu papka, fayl emas: {file_path}"}

    lines = _read_lines(file_path)
    content = "".join(lines)
    truncated = False
    if len(content) > max_chars:
        content = content[:max_chars]
        truncated = True

    return {
        "file_path": file_path,
        "line_count": len(lines),
        "char_count": sum(len(l) for l in lines),
        "content": content,
        "truncated": truncated,
    }


def read_code_lines(file_path: str, start_line: int = 1, end_line: int = None) -> dict:
    """Fayldan faqat berilgan qator oralig'ini o'qiydi (1-based, end_line inklyuziv).

    Katta fayllarning ma'lum qismini o'qish uchun qulay (masalan, xato
    xabarida ko'rsatilgan qator atrofini ko'rish).
    """
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    lines = _read_lines(file_path)
    total = len(lines)
    start = max(1, start_line)
    end = total if end_line is None else min(total, end_line)
    if start > total:
        return {"error": f"start_line ({start}) fayldagi qatorlar sonidan ({total}) katta"}

    selected = lines[start - 1:end]
    return {
        "file_path": file_path,
        "start_line": start,
        "end_line": end,
        "total_lines": total,
        "content": "".join(selected),
    }


def create_code_file(file_path: str, content: str = "", overwrite: bool = False) -> dict:
    """Yangi kod/matn faylini yaratadi (papkalar mavjud bo'lmasa, avtomatik yaratiladi)."""
    if os.path.exists(file_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {file_path} (overwrite=True qiling)"}

    os.makedirs(os.path.dirname(os.path.abspath(file_path)) or ".", exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "file_path": file_path,
        "status": "created",
        "line_count": content.count("\n") + (1 if content else 0),
        "char_count": len(content),
    }


def append_code_text(file_path: str, text: str, newline_before: bool = True) -> dict:
    """Mavjud fayl oxiriga matn qo'shadi. Fayl mavjud bo'lmasa, yangi yaratadi."""
    exists = os.path.exists(file_path)
    os.makedirs(os.path.dirname(os.path.abspath(file_path)) or ".", exist_ok=True)

    with open(file_path, "a", encoding="utf-8") as f:
        if exists and newline_before:
            f.write("\n")
        f.write(text)

    lines = _read_lines(file_path)
    return {"file_path": file_path, "status": "appended", "line_count": len(lines)}


def replace_code_text(file_path: str, find: str, replace: str, save_as: str = None, count: int = -1) -> dict:
    """Fayldagi 'find' matnini 'replace' bilan almashtiradi (oddiy string almashtirish, regex emas).

    count: nechta marta almashtirish (-1 = hammasi).
    save_as berilmasa, asl faylning ustiga yoziladi.
    """
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    if find not in content:
        return {"file_path": file_path, "status": "not_found", "replacements": 0}

    replacements = content.count(find) if count == -1 else min(count, content.count(find))
    new_content = content.replace(find, replace, count if count != -1 else -1)

    out_path = save_as or file_path
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return {"file_path": out_path, "status": "replaced", "replacements": replacements}


def insert_code_lines(file_path: str, line_number: int, text: str) -> dict:
    """Berilgan qator raqami OLDIGA yangi matn qatorini/qatorlarini qo'shadi (1-based).

    line_number fayldagi qatorlar sonidan bittaga katta bo'lsa, matn faylning
    oxiriga qo'shiladi.
    """
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    lines = _read_lines(file_path)
    total = len(lines)
    if line_number < 1 or line_number > total + 1:
        return {"error": f"line_number 1 dan {total + 1} gacha bo'lishi kerak"}

    insert_text = text if text.endswith("\n") else text + "\n"
    lines.insert(line_number - 1, insert_text)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return {"file_path": file_path, "status": "inserted", "at_line": line_number, "line_count": len(lines)}


def delete_code_lines(file_path: str, start_line: int, end_line: int = None) -> dict:
    """Berilgan qator oralig'ini fayldan o'chiradi (1-based, end_line inklyuziv)."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    lines = _read_lines(file_path)
    total = len(lines)
    end = end_line or start_line
    if start_line < 1 or start_line > total:
        return {"error": f"start_line 1 dan {total} gacha bo'lishi kerak"}

    new_lines = lines[:start_line - 1] + lines[end:]

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    return {
        "file_path": file_path,
        "status": "deleted",
        "removed_lines": min(end, total) - start_line + 1,
        "line_count": len(new_lines),
    }


def list_directory_files(dir_path: str, extensions: list = None, recursive: bool = True) -> dict:
    """Papka ichidagi kod/matn fayllarini ro'yxatlaydi.

    extensions: masalan [".py", ".js"] — faqat shu kengaytmalarni ko'rsatadi
        (berilmasa, taniqli matn/kod kengaytmalarining hammasi qaytariladi).
    """
    if not os.path.isdir(dir_path):
        return {"error": f"Papka topilmadi: {dir_path}"}

    allowed = set(extensions) if extensions else _TEXT_EXTENSIONS
    results = []

    if recursive:
        for root, _dirs, filenames in os.walk(dir_path):
            for name in filenames:
                ext = os.path.splitext(name)[1]
                if ext in allowed:
                    full = os.path.join(root, name)
                    results.append({
                        "path": full,
                        "size_bytes": os.path.getsize(full),
                        "extension": ext,
                    })
    else:
        for name in os.listdir(dir_path):
            full = os.path.join(dir_path, name)
            ext = os.path.splitext(name)[1]
            if os.path.isfile(full) and ext in allowed:
                results.append({
                    "path": full,
                    "size_bytes": os.path.getsize(full),
                    "extension": ext,
                })

    return {"dir_path": dir_path, "file_count": len(results), "files": results}


def search_in_files(dir_path: str, query: str, extensions: list = None, case_sensitive: bool = False) -> dict:
    """Papka ichidagi kod/matn fayllarida berilgan matnni qidiradi (grep uslubida).

    Har bir topilgan joy uchun fayl yo'li, qator raqami va qator matnini qaytaradi.
    """
    listing = list_directory_files(dir_path, extensions=extensions, recursive=True)
    if "error" in listing:
        return listing

    matches = []
    needle = query if case_sensitive else query.lower()

    for file_info in listing["files"]:
        path = file_info["path"]
        try:
            lines = _read_lines(path)
        except Exception:
            continue
        for i, line in enumerate(lines, start=1):
            haystack = line if case_sensitive else line.lower()
            if needle in haystack:
                matches.append({"file_path": path, "line_number": i, "line": line.rstrip("\n")})

    return {"dir_path": dir_path, "query": query, "match_count": len(matches), "matches": matches}
