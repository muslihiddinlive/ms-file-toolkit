"""Internetdan ma'lumot olish: URL'dan fayl yuklab olish va oddiy web scraping.

`requests` + `BeautifulSoup` asosida ishlaydi. Xavfsizlik: har bir chaqiruvda
URL avval security.resolve_safe_url() orqali tekshiriladi (SSRF himoyasi —
ichki tarmoq/localhost/cloud-metadata manzillariga so'rov yuborilishining
oldini oladi). Bundan tashqari:

- Har bir so'rovda timeout bor (osilib qolmaslik uchun).
- Fayl yuklashda hajm chegarasi bor (diskni to'ldirib yubormaslik uchun).
- Redirect'lar kuzatiladi, lekin har bir yakuniy manzil ham xavfsizlik
  tekshiruvidan o'tishi kerak (requests buni avtomatik tekshirmaydi, shuning
  uchun redirect'larni o'chirib, o'zimiz qadam-baqadam tekshiramiz).
"""

import os
import requests
from bs4 import BeautifulSoup

from .security import resolve_safe_url, UnsafeUrlError

_DEFAULT_TIMEOUT = 15
_DEFAULT_MAX_BYTES = 50 * 1024 * 1024  # 50 MB
_DEFAULT_MAX_REDIRECTS = 5
_USER_AGENT = "ms-file-toolkit/0.6 (+https://github.com/muslihiddinlive/ms-file-toolkit)"


def search_web(query: str, max_results: int = 8, timeout: int = _DEFAULT_TIMEOUT) -> dict:
    """Internetda oddiy matn qidiruvi (kalit talab qilmaydi, DuckDuckGo HTML natijalari orqali).

    "Telegram Bot API'ning so'nggi versiyasi qaysi?" kabi savollarga aniq
    javob bermaydi — o'rniga qaysi sahifalarda javob bo'lishi mumkinligini
    (sarlavha, manzil, qisqa tavsif) topib beradi. Aniq javobni olish uchun
    natijadagi manzillardan birini scrape_page_text() yoki fetch_url_text()
    bilan o'qish kerak. Kalit yoki obuna talab qilinmaydi, lekin natijalar
    rasmiy Google/Bing API'lariga qaraganda cheklangan bo'lishi mumkin.
    """
    try:
        resolve_safe_url("https://html.duckduckgo.com/html/")
    except UnsafeUrlError as e:
        return {"error": f"Xavfsizlik xatosi: {e}"}

    headers = {"User-Agent": _USER_AGENT}
    try:
        resp = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers=headers,
            timeout=timeout,
        )
    except requests.RequestException as e:
        return {"error": f"So'rov xatosi: {e}"}

    if resp.status_code >= 400:
        resp.close()
        return {"error": f"Qidiruv xizmati xatosi: HTTP {resp.status_code}"}

    soup = BeautifulSoup(resp.text, "html.parser")
    resp.close()

    results = []
    for result in soup.select(".result")[:max_results]:
        link_tag = result.select_one(".result__a")
        snippet_tag = result.select_one(".result__snippet")
        if not link_tag or not link_tag.get("href"):
            continue
        results.append({
            "title": link_tag.get_text(strip=True),
            "url": link_tag["href"],
            "snippet": snippet_tag.get_text(strip=True) if snippet_tag else "",
        })

    return {"query": query, "result_count": len(results), "results": results}


# Ko'p ishlatiladigan servislarning rasmiy changelog/hujjat manzillari.
# search_web() umumiy qidiruv bo'lib, ba'zan aniq natija bermasligi mumkin —
# bu lug'at esa tez-tez so'raladigan mavzular uchun to'g'ridan-to'g'ri, ishonchli
# manzilni beradi (masalan "Telegram Bot API" -> rasmiy changelog sahifasi).
KNOWN_CHANGELOG_URLS = {
    "telegram bot api": "https://core.telegram.org/bots/api-changelog",
    "telegram bot api docs": "https://core.telegram.org/bots/api",
    "discord api": "https://discord.com/developers/docs/change-log",
    "discord.py": "https://github.com/Rapptz/discord.py/blob/master/CHANGELOG.rst",
    "aiogram": "https://github.com/aiogram/aiogram/releases",
    "python": "https://docs.python.org/3/whatsnew/index.html",
    "node.js": "https://github.com/nodejs/node/blob/main/doc/changelogs/CHANGELOG_V22.md",
    "openai api": "https://platform.openai.com/docs/changelog",
    "anthropic claude api": "https://docs.claude.com/en/release-notes/api",
    "github api": "https://docs.github.com/en/rest/overview/whats-new",
    "render.com": "https://render.com/changelog",
    "cloudflare workers": "https://developers.cloudflare.com/workers/platform/changelog/",
}


def get_known_changelog_url(service_name: str) -> dict:
    """Ma'lum bir servis uchun oldindan tayyorlangan rasmiy changelog/hujjat manzilini qaytaradi.

    Aniq mos kelish bo'lmasa, service_name qismiy mos keladigan kalitlarni
    (bor bo'lsa) tavsiya sifatida qaytaradi. Hech narsa topilmasa, buning
    o'rniga search_web() bilan qidirish kerakligini ko'rsatadi.
    """
    key = service_name.strip().lower()
    if key in KNOWN_CHANGELOG_URLS:
        return {"service": service_name, "url": KNOWN_CHANGELOG_URLS[key], "match": "exact"}

    suggestions = [name for name in KNOWN_CHANGELOG_URLS if key in name or name in key]
    if suggestions:
        return {
            "service": service_name,
            "match": "partial",
            "suggestions": [{"service": name, "url": KNOWN_CHANGELOG_URLS[name]} for name in suggestions],
        }

    return {
        "service": service_name,
        "match": "none",
        "hint": "Ro'yxatda yo'q — search_web() bilan qidiring yoki manzilni qo'lda toping.",
    }


def _safe_get(url: str, timeout: int, stream: bool = False, max_redirects: int = _DEFAULT_MAX_REDIRECTS):
    """requests.get() ni SSRF himoyasi bilan chaqiradi, har bir redirectni ham tekshiradi."""
    headers = {"User-Agent": _USER_AGENT}
    current_url = url

    for _ in range(max_redirects + 1):
        resolve_safe_url(current_url)
        resp = requests.get(current_url, headers=headers, timeout=timeout, stream=stream, allow_redirects=False)
        if resp.is_redirect or resp.is_permanent_redirect:
            next_url = resp.headers.get("Location")
            resp.close()
            if not next_url:
                raise UnsafeUrlError("Redirect javobida Location sarlavhasi yo'q")
            current_url = requests.compat.urljoin(current_url, next_url)
            continue
        return resp, current_url

    raise UnsafeUrlError(f"Juda ko'p redirect ({max_redirects} dan oshdi)")


def download_file(url: str, output_path: str, max_bytes: int = _DEFAULT_MAX_BYTES, timeout: int = _DEFAULT_TIMEOUT) -> dict:
    """URL'dan faylni yuklab, diskka saqlaydi.

    max_bytes chegarasidan katta fayl yuklanmaydi (xato qaytariladi, yarim
    yuklangan fayl o'chiriladi).
    """
    try:
        resp, final_url = _safe_get(url, timeout=timeout, stream=True)
    except UnsafeUrlError as e:
        return {"error": f"Xavfsizlik xatosi: {e}"}
    except requests.RequestException as e:
        return {"error": f"So'rov xatosi: {e}"}

    if resp.status_code >= 400:
        resp.close()
        return {"error": f"HTTP xatosi: {resp.status_code} ({url})"}

    content_length = resp.headers.get("Content-Length")
    if content_length and int(content_length) > max_bytes:
        resp.close()
        return {"error": f"Fayl juda katta: {content_length} bayt (chegara: {max_bytes})"}

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    written = 0
    try:
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=65536):
                written += len(chunk)
                if written > max_bytes:
                    f.close()
                    os.remove(output_path)
                    return {"error": f"Fayl hajmi chegaradan oshdi ({max_bytes} bayt), yuklab olish to'xtatildi"}
                f.write(chunk)
    finally:
        resp.close()

    return {
        "file_path": output_path,
        "status": "downloaded",
        "final_url": final_url,
        "size_bytes": written,
        "content_type": resp.headers.get("Content-Type"),
    }


def fetch_url_text(url: str, timeout: int = _DEFAULT_TIMEOUT, max_chars: int = 200_000) -> dict:
    """URL'dan sahifa mazmunini xom matn (raw) sifatida oladi (HTML tozalanmaydi)."""
    try:
        resp, final_url = _safe_get(url, timeout=timeout)
    except UnsafeUrlError as e:
        return {"error": f"Xavfsizlik xatosi: {e}"}
    except requests.RequestException as e:
        return {"error": f"So'rov xatosi: {e}"}

    if resp.status_code >= 400:
        resp.close()
        return {"error": f"HTTP xatosi: {resp.status_code} ({url})"}

    text = resp.text
    truncated = False
    if len(text) > max_chars:
        text = text[:max_chars]
        truncated = True
    resp.close()

    return {
        "url": url,
        "final_url": final_url,
        "status_code": resp.status_code,
        "content_type": resp.headers.get("Content-Type"),
        "text": text,
        "truncated": truncated,
    }


def scrape_page_text(url: str, timeout: int = _DEFAULT_TIMEOUT, max_chars: int = 100_000) -> dict:
    """Web-sahifadan o'qiladigan matnni ajratib oladi (skript/stil belgilari olib tashlanadi).

    HTML teglaridan tozalangan, odam o'qiy oladigan matn qaytaradi —
    fetch_url_text'dan farqli o'laroq, bu yerda xom HTML emas, balki
    sahifaning "mazmuni" beriladi.
    """
    try:
        resp, final_url = _safe_get(url, timeout=timeout)
    except UnsafeUrlError as e:
        return {"error": f"Xavfsizlik xatosi: {e}"}
    except requests.RequestException as e:
        return {"error": f"So'rov xatosi: {e}"}

    if resp.status_code >= 400:
        resp.close()
        return {"error": f"HTTP xatosi: {resp.status_code} ({url})"}

    soup = BeautifulSoup(resp.text, "html.parser")
    resp.close()

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else None
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    clean_text = "\n".join(lines)

    truncated = False
    if len(clean_text) > max_chars:
        clean_text = clean_text[:max_chars]
        truncated = True

    return {
        "url": url,
        "final_url": final_url,
        "title": title,
        "text": clean_text,
        "truncated": truncated,
    }


def extract_page_links(url: str, timeout: int = _DEFAULT_TIMEOUT, same_domain_only: bool = False) -> dict:
    """Web-sahifadagi barcha havolalarni (<a href>) ajratib oladi, matni bilan birga.

    Nisbiy (relative) havolalar sahifa manziliga nisbatan to'liq URL'ga
    aylantiriladi. same_domain_only=True bo'lsa, faqat asl sahifa bilan bir
    xil domendagi havolalar qaytariladi.
    """
    try:
        resp, final_url = _safe_get(url, timeout=timeout)
    except UnsafeUrlError as e:
        return {"error": f"Xavfsizlik xatosi: {e}"}
    except requests.RequestException as e:
        return {"error": f"So'rov xatosi: {e}"}

    if resp.status_code >= 400:
        resp.close()
        return {"error": f"HTTP xatosi: {resp.status_code} ({url})"}

    soup = BeautifulSoup(resp.text, "html.parser")
    resp.close()

    from urllib.parse import urljoin, urlparse
    base_domain = urlparse(final_url).netloc

    links = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith("#") or href.startswith("javascript:"):
            continue
        full_url = urljoin(final_url, href)
        if same_domain_only and urlparse(full_url).netloc != base_domain:
            continue
        if full_url in seen:
            continue
        seen.add(full_url)
        links.append({"url": full_url, "text": a.get_text(strip=True)})

    return {"url": url, "final_url": final_url, "link_count": len(links), "links": links}


def extract_page_images(url: str, timeout: int = _DEFAULT_TIMEOUT) -> dict:
    """Web-sahifadagi barcha rasm (<img>) manzillarini ajratib oladi (to'liq URL'ga aylantirilgan)."""
    try:
        resp, final_url = _safe_get(url, timeout=timeout)
    except UnsafeUrlError as e:
        return {"error": f"Xavfsizlik xatosi: {e}"}
    except requests.RequestException as e:
        return {"error": f"So'rov xatosi: {e}"}

    if resp.status_code >= 400:
        resp.close()
        return {"error": f"HTTP xatosi: {resp.status_code} ({url})"}

    soup = BeautifulSoup(resp.text, "html.parser")
    resp.close()

    from urllib.parse import urljoin
    images = []
    for img in soup.find_all("img", src=True):
        src = img["src"].strip()
        if not src:
            continue
        full_url = urljoin(final_url, src)
        images.append({"url": full_url, "alt": img.get("alt", "")})

    return {"url": url, "final_url": final_url, "image_count": len(images), "images": images}
