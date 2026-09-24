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
import ipaddress
import socket
from urllib.parse import urlparse

_DANGEROUS_PREFIXES = (
    "/etc/", "/proc/", "/sys/", "/root/", "/boot/",
    "/var/run/", "/dev/",
)


class UnsafePathError(ValueError):
    """file_path xavfsizlik tekshiruvidan o'tmadi."""


class UnsafeUrlError(ValueError):
    """url xavfsizlik tekshiruvidan (SSRF himoyasi) o'tmadi."""


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


def resolve_safe_url(url: str, allow_private: bool = False) -> str:
    """`url`ni tekshirib, xavfsiz bo'lsa o'zini qaytaradi (SSRF himoyasi).

    AI (yoki uni boshqarayotgan foydalanuvchi) `url` sifatida ichki tarmoq
    manzilini yuborishi mumkin — masalan "http://169.254.169.254/latest/..."
    (cloud metadata endpoint) yoki "http://localhost:6379" (ichki servis).
    Bu tekshirilmasa, toolkit server nomidan foydalanib ichki tarmoqqa
    so'rov yuborishi mumkin.

    Faqat http/https sxemalariga ruxsat beriladi; DNS orqali IP manzilga
    aylantirilib, natija private/loopback/link-local (masalan 127.0.0.1,
    10.x.x.x, 169.254.x.x) bo'lsa rad etiladi. allow_private=True bilan bu
    tekshiruv o'chiriladi (masalan ichki test muhitida ataylab kerak bo'lsa).
    """
    if not isinstance(url, str) or not url:
        raise UnsafeUrlError("url bo'sh yoki noto'g'ri turda")

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise UnsafeUrlError(f"Faqat http/https sxemalariga ruxsat beriladi, berilgan: {parsed.scheme or '(yo`q)'}")

    host = parsed.hostname
    if not host:
        raise UnsafeUrlError("url tarkibida host topilmadi")

    if allow_private:
        return url

    try:
        addr_info = socket.getaddrinfo(host, None)
    except socket.gaierror as e:
        raise UnsafeUrlError(f"Host manzili aniqlanmadi: {host} ({e})")

    for info in addr_info:
        ip_str = info[4][0]
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            continue
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            raise UnsafeUrlError(
                f"url ichki/xavfli tarmoq manziliga ishora qiladi va bloklandi: {host} -> {ip_str}"
            )

    return url
