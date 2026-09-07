"""
Xavfsizlik: AI tool-calling orqali kelgan `file_path` qiymatlarini tekshirish.

Muammo: AI (yoki uni boshqarayotgan foydalanuvchi) `file_path` sifatida
ixtiyoriy qiymat yuborishi mumkin — masalan "../../etc/passwd" yoki
"/etc/shadow". Bu tekshirilmasa, toolkit ruxsatsiz fayllarni o'qishi yoki
ustiga yozishi mumkin.

Yechim: agar MS_TOOLKIT_BASE_DIR muhit o'zgaruvchisi (yoki dispatch() ga
uzatilgan base_dir) o'rnatilgan bo'lsa, barcha fayl amallari faqat o'sha
papka ichida ruxsat etiladi. O'rnatilmagan bo'lsa (standart holat), faqat
eng xavfli patternlar (null-byte, aniq tizim papkalari) bloklanadi.
"""

import os

_DANGEROUS_PREFIXES = (
    "/etc/", "/proc/", "/sys/", "/root/", "/boot/",
    "/var/run/", "/dev/",
)


class UnsafePathError(ValueError):
    """file_path xavfsizlik tekshiruvidan o'tmadi."""


def resolve_safe_path(file_path: str, base_dir: str = None) -> str:
    """`file_path`ni tekshirib, xavfsiz bo'lsa normallashtirilgan absolyut yo'lni qaytaradi.

    base_dir berilmasa, MS_TOOLKIT_BASE_DIR muhit o'zgaruvchisi ishlatiladi
    (u ham bo'lmasa, faqat asosiy tizim papkalariga cheklov qo'yiladi).
    """
    if not isinstance(file_path, str) or not file_path:
        raise UnsafePathError("file_path bo'sh yoki noto'g'ri turda")

    if "\x00" in file_path:
        raise UnsafePathError("file_path tarkibida ruxsat etilmagan belgi (null byte)")

    base_dir = base_dir or os.environ.get("MS_TOOLKIT_BASE_DIR")
    abs_path = os.path.abspath(os.path.normpath(file_path))

    if base_dir:
        base_abs = os.path.abspath(base_dir)
        if os.path.commonpath([abs_path, base_abs]) != base_abs:
            raise UnsafePathError(
                f"file_path ruxsat etilgan papka tashqarisida: {file_path} "
                f"(ruxsat etilgan: {base_abs})"
            )
    else:
        for prefix in _DANGEROUS_PREFIXES:
            if abs_path.startswith(prefix):
                raise UnsafePathError(
                    f"file_path tizim papkasiga ishora qiladi va bloklandi: {abs_path} "
                    f"(cheklashni sozlash uchun MS_TOOLKIT_BASE_DIR o'rnating)"
                )

    return abs_path
