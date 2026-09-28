"""QR kod yaratish va o'qish — to'liq LOKAL (tashqi API'ga bog'liq emas).

Yaratish: `segno` (sof Python, qo'shimcha tizim kutubxonalarisiz).
O'qish:   `zxing-cpp` (tayyor wheel, tizimda zbar/OpenCV o'rnatish shart emas).

Yaratishda LaborantRobot'dagi QR formatlari qo'llab-quvvatlanadi: matn, havola,
telefon, email, WiFi, SMS, vCard (kontakt) va Telegram username.
"""

import os
from urllib.parse import quote

MAX_QR_DATA_LENGTH = 2000  # QR sig'imi (~2953 bayt) va o'qish ishonchliligi uchun
QR_TYPES = ("text", "url", "phone", "email", "wifi", "sms", "vcard", "telegram")


def _escape_wifi(value: str) -> str:
    """WIFI: formatida \\ ; , : " belgilari escape qilinishi shart (aks holda
    nomida/parolida shu belgilar bo'lgan tarmoqqa ulanish buziladi)."""
    for ch in ("\\", ";", ",", ":", '"'):
        value = value.replace(ch, "\\" + ch)
    return value


def _one_line(value: str) -> str:
    return " ".join(str(value).split())


def _clean_phone(phone: str) -> str:
    phone = phone.strip().replace(" ", "").replace("-", "")
    return phone if phone.startswith("+") else "+" + phone


def build_qr_payload(
    data: str,
    qr_type: str = "text",
    subject: str = "",
    body: str = "",
    password: str = "",
    security: str = "WPA",
    hidden: bool = False,
    message: str = "",
    name: str = "",
    phone: str = "",
    email: str = "",
    url: str = "",
    org: str = "",
    note: str = "",
) -> str:
    """`qr_type`ga qarab QR ichiga yoziladigan standart matnni yasaydi."""
    if qr_type not in QR_TYPES:
        raise ValueError(f"Noma'lum qr_type: {qr_type!r}. Mumkin: {', '.join(QR_TYPES)}")

    if qr_type == "text":
        return data

    if qr_type == "url":
        return data if data.startswith(("http://", "https://", "tg://")) else "https://" + data

    if qr_type == "phone":
        return f"tel:{_clean_phone(data)}"

    if qr_type == "email":
        params = []
        if subject:
            params.append(f"subject={quote(subject)}")
        if body:
            params.append(f"body={quote(body)}")
        return f"mailto:{data}" + ("?" + "&".join(params) if params else "")

    if qr_type == "wifi":
        if security not in ("WPA", "WEP", "nopass"):
            raise ValueError("security: 'WPA', 'WEP' yoki 'nopass' bo'lishi kerak")
        pwd = "" if security == "nopass" else _escape_wifi(password)
        return f"WIFI:S:{_escape_wifi(data)};T:{security};P:{pwd};H:{'true' if hidden else 'false'};;"

    if qr_type == "sms":
        return f"SMSTO:{_clean_phone(data)}:{message}"

    if qr_type == "telegram":
        return f"https://t.me/{data.lstrip('@').strip()}"

    # vcard — `data` maydoni to'liq ism sifatida ishlatiladi
    lines = ["BEGIN:VCARD", "VERSION:3.0", f"FN:{_one_line(name or data)}"]
    if phone:
        lines.append(f"TEL;TYPE=CELL:{_clean_phone(phone)}")
    if email:
        lines.append(f"EMAIL:{_one_line(email)}")
    if url:
        lines.append(f"URL:{_one_line(url)}")
    if org:
        lines.append(f"ORG:{_one_line(org)}")
    if note:
        lines.append(f"NOTE:{_one_line(note)}")
    lines.append("END:VCARD")
    return "\n".join(lines)


def create_qr_code(
    output_path: str,
    data: str,
    qr_type: str = "text",
    size: int = 512,
    error_correction: str = "m",
    overwrite: bool = False,
    **options,
) -> dict:
    """Matn/havola/WiFi/kontakt va h.k. dan QR kod rasmi (.png yoki .svg) yaratadi."""
    import segno

    if os.path.exists(output_path) and not overwrite:
        return {"error": f"Fayl allaqachon mavjud: {output_path} (overwrite=True qiling)"}
    if not isinstance(data, str) or not data.strip():
        return {"error": "data bo'sh bo'lmasligi kerak"}
    if error_correction.lower() not in ("l", "m", "q", "h"):
        return {"error": "error_correction: 'l', 'm', 'q' yoki 'h' bo'lishi kerak"}
    ext = os.path.splitext(output_path)[1].lower()
    if ext not in (".png", ".svg"):
        return {"error": "output_path .png yoki .svg bilan tugashi kerak"}

    try:
        payload = build_qr_payload(data, qr_type, **options)
    except (ValueError, TypeError) as e:
        return {"error": str(e)}

    if len(payload) > MAX_QR_DATA_LENGTH:
        return {"error": f"Ma'lumot juda uzun ({len(payload)} belgi, ruxsat: {MAX_QR_DATA_LENGTH})"}

    try:
        qr = segno.make(payload, error=error_correction.lower(), micro=False)
    except segno.DataOverflowError:
        return {"error": "Ma'lumot QR'ga sig'madi — qisqartiring yoki error_correction='l' qiling"}

    border = 4  # QR standarti tavsiya qilgan "quiet zone" — skaner ishonchliligi uchun
    modules = qr.symbol_size(scale=1, border=border)[0]
    scale = max(1, int(size) // modules)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    qr.save(output_path, scale=scale, border=border)

    return {
        "file_path": output_path,
        "status": "created",
        "qr_type": qr_type,
        "content": payload,
        "pixel_size": modules * scale,
    }


def _classify(text: str) -> str:
    low = text.lower()
    if low.startswith(("http://", "https://")):
        return "url"
    if low.startswith("wifi:"):
        return "wifi"
    if low.startswith("tel:"):
        return "phone"
    if low.startswith("mailto:"):
        return "email"
    if low.startswith("smsto:") or low.startswith("sms:"):
        return "sms"
    if low.startswith("begin:vcard"):
        return "vcard"
    return "text"


def read_qr_code(image_path: str, only_qr: bool = True) -> dict:
    """Rasmdagi QR kod(lar)ni o'qib, ichidagi matnni qaytaradi (lokal, internetsiz)."""
    import zxingcpp
    from PIL import Image, ImageOps

    if not os.path.exists(image_path):
        return {"error": f"Fayl topilmadi: {image_path}"}

    try:
        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img).convert("RGB")
    except Exception as e:  # noqa: BLE001 — buzilgan/rasm bo'lmagan fayl
        return {"error": f"Rasmni ochib bo'lmadi: {type(e).__name__}: {e}"}

    formats = []
    if only_qr:
        formats = [zxingcpp.BarcodeFormat.QRCode, zxingcpp.BarcodeFormat.MicroQRCode]

    def _scan(image):
        return zxingcpp.read_barcodes(image, formats=formats) if formats else zxingcpp.read_barcodes(image)

    results = _scan(img)
    if not results and max(img.size) < 1200:
        # Kichik/past sifatli rasm — 2x kattalashtirib qayta urinamiz
        results = _scan(img.resize((img.width * 2, img.height * 2), Image.LANCZOS))
    if not results:
        # Past kontrast/inversiya — kulrang + avtokontrast bilan urinamiz
        results = _scan(ImageOps.autocontrast(ImageOps.grayscale(img)))

    codes = [
        {"text": r.text, "format": str(r.format).split(".")[-1], "kind": _classify(r.text)}
        for r in results
        if r.valid or r.text
    ]
    return {
        "file_path": image_path,
        "found": bool(codes),
        "count": len(codes),
        "codes": codes,
    }
