"""
ms_toolkit uchun komandalar qatori (CLI) interfeysi.

Ishlatish:
    ms-toolkit list
    ms-toolkit run create_docx '{"file_path": "test.docx", "title": "Salom"}'
    ms-toolkit run read_docx_text '{"file_path": "test.docx"}'
    ms-toolkit run read_any_file '{"file_path": "hujjat.xlsx"}'

MS_TOOLKIT_BASE_DIR muhit o'zgaruvchisi bilan fayl amallarini bitta papkaga
cheklash mumkin (xavfsizlik uchun tavsiya etiladi).
"""

import sys
import json
import argparse

from .registry import REGISTRY, dispatch
from .schemas import TOOLS


def cmd_list(args):
    for t in TOOLS:
        print(f"{t['name']:<28} {t['description'][:80]}")


def cmd_run(args):
    if args.tool_name not in REGISTRY:
        print(f"Xato: noma'lum tool '{args.tool_name}'. Ro'yxat uchun: ms-toolkit list", file=sys.stderr)
        sys.exit(1)

    try:
        tool_input = json.loads(args.json_input)
    except json.JSONDecodeError as e:
        print(f"Xato: JSON noto'g'ri formatda: {e}", file=sys.stderr)
        sys.exit(1)

    result = dispatch(args.tool_name, tool_input)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    if "error" in result:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(prog="ms-toolkit", description="MS fayllar (DOCX/XLSX/PPTX/PDF) uchun CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="Barcha mavjud tool'larni ro'yxatini chiqaradi").set_defaults(func=cmd_list)

    run_parser = sub.add_parser("run", help="Bitta tool'ni ishga tushiradi")
    run_parser.add_argument("tool_name", help="Ishga tushiriladigan tool nomi (masalan: create_docx)")
    run_parser.add_argument("json_input", help="Tool uchun JSON formatidagi kirish, masalan '{\"file_path\": \"a.docx\"}'")
    run_parser.set_defaults(func=cmd_run)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
