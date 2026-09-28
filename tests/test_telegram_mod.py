"""Telegram moderatsiya adapteri testlari (haqiqiy Telegram'siz, mock bot bilan)."""
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

pytest.importorskip("tg_mod_functions")

from ms_toolkit import dispatch, configure_telegram, telegram_tool_schemas
from ms_toolkit import telegram_mod


@pytest.fixture(autouse=True)
def reset_toolkit():
    telegram_mod._toolkit = None
    yield
    telegram_mod._toolkit = None


def make_bot():
    bot = AsyncMock()
    bot.get_chat_member.return_value = SimpleNamespace(status="member")
    return bot


def test_unconfigured_returns_clear_error():
    result = dispatch("ban_user", {"chat_id": -1, "user_id": 1})
    assert "error" in result  # sozlanmagan: oddiy "noma'lum tool"


def test_configure_exposes_all_moderation_schemas():
    configure_telegram(make_bot())
    names = {s["name"] for s in telegram_tool_schemas()}
    assert {"ban_user", "mute_user", "warn_user", "lockdown_chat"} <= names
    assert len(names) == 25
    # schema formati TOOLS bilan bir xil
    assert all({"name", "description", "input_schema"} <= set(s) for s in telegram_tool_schemas())


def test_dispatch_routes_to_bot():
    bot = make_bot()
    configure_telegram(bot)
    result = dispatch("ban_user", {"chat_id": -100, "user_id": 42})
    assert result["ok"] is True
    bot.ban_chat_member.assert_awaited_once()


def test_protected_user_is_refused_through_dispatch():
    bot = make_bot()
    configure_telegram(bot, protected_user_ids={999})
    result = dispatch("ban_user", {"chat_id": -100, "user_id": 999})
    assert result["ok"] is False
    assert "protected" in result["message"]
    bot.ban_chat_member.assert_not_awaited()


def test_group_creator_is_refused_through_dispatch():
    bot = make_bot()
    bot.get_chat_member.return_value = SimpleNamespace(status="creator")
    configure_telegram(bot)
    result = dispatch("mute_user", {"chat_id": -100, "user_id": 7, "minutes": 5})
    assert result["ok"] is False
    bot.restrict_chat_member.assert_not_awaited()


def test_warns_persist_with_warns_path(tmp_path):
    path = tmp_path / "warns.json"
    configure_telegram(make_bot(), warns_path=str(path))
    dispatch("warn_user", {"chat_id": -1, "user_id": 5, "reason": "spam"})
    # "restart": yangi konfiguratsiya, bir xil fayl
    configure_telegram(make_bot(), warns_path=str(path))
    info = dispatch("get_member_info", {"chat_id": -1, "user_id": 5})
    assert info["warns"] == 1


def test_file_tools_still_work_and_stay_path_protected(tmp_path):
    configure_telegram(make_bot())
    # fayl tool'lari o'zgarmagan: path-himoya hamon ishlaydi
    result = dispatch("read_code_file", {"file_path": "/etc/passwd"})
    assert "error" in result
