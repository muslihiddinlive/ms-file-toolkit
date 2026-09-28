"""
Telegram guruh moderatsiyasi tool'lari (tg-mod-functions ustiga adapter).

Bu modul kodni nusxalamaydi — ``tg-mod-functions`` paketini ishlatadi
(``pip install ms-file-toolkit`` uni avtomatik o'rnatadi), shuning uchun
ikki joyda ikki xil versiya paydo bo'lmaydi.

Farq: ms-file-toolkit tool'lari sinxron va holatsiz, moderatsiya tool'lari
esa async, ``aiogram.Bot`` obyektini talab qiladi va holatli (warn storage).
Shuning uchun avval ``configure_telegram(bot, ...)`` chaqiriladi, so'ng
``dispatch("ban_user", {...})`` oddiy fayl tool'lari kabi ishlaydi.

Xavfsizlik: ``protected_user_ids`` va guruh yaratuvchisi (creator) har doim
himoyalangan — AI adashsa yoki aldansa ham ularga ban/mute/kick/demote
qilib bo'lmaydi.
"""

import asyncio
import concurrent.futures
import threading

try:
    from tg_mod_functions import ModerationToolkit, JSONFileWarnStorage
except ImportError:  # pragma: no cover - faqat buzilgan o'rnatishda
    ModerationToolkit = None
    JSONFileWarnStorage = None

_toolkit = None
_loop = None
_loop_thread = None
_lock = threading.Lock()


def _require():
    if ModerationToolkit is None:
        raise ImportError(
            "Telegram moderatsiya tool'lari uchun 'tg-mod-functions' kerak: "
            "pip install --upgrade tg-mod-functions"
        )


def configure_telegram(bot, warn_storage=None, max_warns=3, protected_user_ids=None,
                       warns_path=None):
    """Moderatsiya tool'larini yoqadi. ``bot`` — ``aiogram.Bot`` obyekti.

    warns_path berilsa, ogohlantirishlar JSON faylda saqlanadi (restart'dan
    keyin ham yo'qolmaydi); aks holda ``warn_storage`` yoki xotira ishlatiladi.
    """
    global _toolkit
    _require()
    if warn_storage is None and warns_path:
        warn_storage = JSONFileWarnStorage(warns_path)
    _toolkit = ModerationToolkit(
        bot,
        warn_storage=warn_storage,
        max_warns=max_warns,
        protected_user_ids=set(protected_user_ids or ()),
    )
    return _toolkit


def telegram_tool_names():
    """Sozlangan moderatsiya tool'lari nomlari (sozlanmagan bo'lsa bo'sh)."""
    return list(_toolkit._tools) if _toolkit else []


def telegram_tool_schemas():
    """Anthropic formatidagi schemalar — ``TOOLS`` bilan bir xil format."""
    return _toolkit.as_anthropic_tools() if _toolkit else []


def _ensure_loop():
    """Sinxron dispatch() ichidan async tool'lar uchun alohida event loop."""
    global _loop, _loop_thread
    with _lock:
        if _loop is None or _loop.is_closed():
            _loop = asyncio.new_event_loop()
            _loop_thread = threading.Thread(target=_loop.run_forever, daemon=True)
            _loop_thread.start()
    return _loop


def call_telegram_tool(tool_name: str, **kwargs) -> dict:
    """Bitta moderatsiya tool'ini bajaradi va {ok, message, ...} qaytaradi."""
    if _toolkit is None:
        return {"error": "Telegram tool'lari sozlanmagan: avval configure_telegram(bot) chaqiring"}
    # aiogram Bot obyekti o'z event loop'ida yaratilgan bo'lishi mumkin;
    # bu yerda alohida loop'da bajaramiz va natijani kutamiz.
    future = asyncio.run_coroutine_threadsafe(_toolkit.call(tool_name, **kwargs), _ensure_loop())
    try:
        result = future.result(timeout=60)
    except concurrent.futures.TimeoutError:
        return {"error": f"{tool_name}: 60 soniyada javob kelmadi"}
    return result.as_dict()
