"""
Misol: Claude API'ga ms_toolkit'ni 'tools' sifatida ulash.

Ishga tushirish:
    export ANTHROPIC_API_KEY=...
    python example.py "Bu hujjatda nima yozilgan? /path/to/file.docx"
"""

import sys
import os
import json
import anthropic

from ms_toolkit import TOOLS, dispatch

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def run(user_message: str):
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
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
