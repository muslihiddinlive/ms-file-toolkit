"""
Misol: Claude API'ga ms_toolkit'ni 'tools' sifatida ulash.

O'rnatish:
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=...

Ishga tushirish:
    python example.py "test.docx faylida nima yozilgan?"
    python example.py "/tmp/hisobot.docx nomli hujjat yarat, sarlavhasi 'Hisobot' bo'lsin"
"""

import sys
import os
import json
import anthropic

from ms_toolkit import TOOLS, dispatch

MODEL = "claude-sonnet-5"

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = (
    "Siz Microsoft fayllar (Word, Excel, PowerPoint) bilan ishlaydigan yordamchisiz. "
    "Fayllarni o'qish yoki yaratish/tahrirlash kerak bo'lsa, mos tool'ni chaqiring. "
    "Fayl yo'llarini aniq va to'liq (absolyut) ko'rsating."
)


def run(user_message: str):
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            for block in response.content:
                if block.type == "text":
                    print(block.text)
            break

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"[tool chaqirildi: {block.name}({block.input})]")
                result = dispatch(block.name, block.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False, default=str),
                    }
                )

        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or "Salom!"
    run(prompt)
