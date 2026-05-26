"""
ClaudeService — AI-підказки для Boss Fight через Anthropic API.
Якщо CLAUDE_API_KEY не вказаний — повертає заглушку.
"""
import httpx
from app.core.config import settings

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-20250514"


async def get_ai_hint(
    task_text: str,
    starter_code: str,
    user_code: str,
    test_results: list[dict],
    hint_level: int = 1,
) -> str:
    """
    hint_level: 1 = загальний напрямок, 2 = конкретніше, 3 = майже відповідь
    """
    if not settings.CLAUDE_API_KEY:
        return _fallback_hint(hint_level)

    failed = [r for r in test_results if not r.get("passed")]
    failed_info = ""
    for r in failed[:2]:
        if not r.get("is_hidden"):
            failed_info += f"\n- Вхід: {r.get('actual_output','?')} (очікувалось: {r.get('expected_output','?')})"

    verbosity = {
        1: "Дай загальний напрямок без коду — яку ідею або підхід використати.",
        2: "Дай конкретну підказку: яку структуру або алгоритм застосувати. Можна показати шаблон без повної відповіді.",
        3: "Дай майже готове рішення — покажи структуру коду з пропущеними деталями.",
    }[hint_level]

    prompt = f"""Ти помічник у Python-грі PyQuest. Студент вирішує задачу.

ЗАДАЧА:
{task_text}

КОД СТУДЕНТА:
```python
{user_code or starter_code}
```

ПРОВАЛЕНІ ТЕСТИ:{failed_info or ' немає даних'}

Твоє завдання: {verbosity}
Відповідь — тільки підказка, коротко (1-4 речення), українською мовою."""

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                ANTHROPIC_URL,
                headers={
                    "x-api-key": settings.CLAUDE_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": MODEL,
                    "max_tokens": 300,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
        data = resp.json()
        return data["content"][0]["text"].strip()
    except Exception as e:
        return _fallback_hint(hint_level)


def _fallback_hint(level: int) -> str:
    hints = {
        1: "💡 Подумай про базовий випадок — що має повернути функція для найпростішого вхідного значення?",
        2: "💡 Спробуй розбити задачу на менші кроки. Яку структуру даних або цикл тут доречно використати?",
        3: "💡 Перевір свій алгоритм на прикладах з умови вручну, крок за кроком.",
    }
    return hints.get(level, hints[1])
