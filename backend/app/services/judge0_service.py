"""
Інтеграція з Judge0 API для виконання Python-коду у босс-файті.
Якщо JUDGE0_API_KEY не вказаний — використовується локальний fallback через subprocess (для розробки).
"""
import re
import subprocess
import sys
import tempfile
import os
from typing import Optional

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

from app.core.config import settings

JUDGE0_URL = "https://judge0-ce.p.rapidapi.com"
LANGUAGE_ID_PYTHON = 71  # Python 3.8.1

FORBIDDEN_IMPORTS = [
    "os", "sys", "subprocess", "socket", "requests", "http",
    "urllib", "shutil", "pathlib", "glob", "tempfile",
    "multiprocessing", "threading", "ctypes", "importlib",
]
FORBIDDEN_PATTERNS = [
    r"__import__",
    r"getattr\s*\(",
    r"setattr\s*\(",
    r"globals\s*\(",
    r"locals\s*\(",
    r"vars\s*\(",
]


def sanitize_code(code: str) -> tuple[bool, str]:
    """Повертає (is_safe, reason). Перша лінія захисту — основний захист у Judge0 sandbox."""
    for forbidden in FORBIDDEN_IMPORTS:
        pattern = rf'\bimport\s+{forbidden}\b|\bfrom\s+{forbidden}\b'
        if re.search(pattern, code):
            return False, f"Заборонений імпорт: {forbidden}"

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, code):
            return False, "Заборонена операція"

    if len(code) > 10_000:
        return False, "Код занадто довгий (максимум 10 000 символів)"

    return True, ""


def _run_code_local(full_code: str, time_limit: int) -> dict:
    """Локальний fallback для розробки без Judge0 API."""
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(full_code)
            tmppath = f.name

        result = subprocess.run(
            [sys.executable, tmppath],
            capture_output=True,
            text=True,
            timeout=time_limit,
        )
        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "status": "Accepted" if result.returncode == 0 else "Runtime Error",
            "time": None,
            "memory": None,
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Time limit exceeded", "status": "Time Limit Exceeded", "time": None, "memory": None}
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "status": "Internal Error", "time": None, "memory": None}
    finally:
        try:
            os.unlink(tmppath)
        except Exception:
            pass


async def _run_code_judge0(full_code: str, time_limit: int, memory_limit_mb: int) -> dict:
    """Виконання коду через Judge0 API."""
    payload = {
        "source_code": full_code,
        "language_id": LANGUAGE_ID_PYTHON,
        "time_limit": time_limit,
        "memory_limit": memory_limit_mb * 1024,
        "wall_time_limit": time_limit + 2,
    }
    headers = {
        "X-RapidAPI-Key": settings.JUDGE0_API_KEY,
        "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{JUDGE0_URL}/submissions?base64_encoded=false&wait=true",
            json=payload,
            headers=headers,
            timeout=30.0,
        )
    r = resp.json()
    return {
        "stdout": (r.get("stdout") or "").strip(),
        "stderr": (r.get("stderr") or "").strip(),
        "status": r.get("status", {}).get("description", "Unknown"),
        "time": r.get("time"),
        "memory": r.get("memory"),
    }


async def run_test_case(
    user_code: str,
    function_call: str,
    expected_output: str,
    is_hidden: bool,
    time_limit: int,
    memory_limit_mb: int,
    description: str = "",
) -> dict:
    """
    Виконує один тест-кейс.
    function_call — рядок із вже підставленими аргументами, наприклад: find_max([3, 1, 4])
    """
    full_code = f"""{user_code}

# === Test Runner ===
try:
    result = {function_call}
    print(result)
except Exception as e:
    print(f"ERROR: {{type(e).__name__}}: {{e}}")
"""

    use_judge0 = bool(getattr(settings, "JUDGE0_API_KEY", "")) and HTTPX_AVAILABLE

    if use_judge0:
        raw = await _run_code_judge0(full_code, time_limit, memory_limit_mb)
    else:
        import asyncio
        raw = await asyncio.get_event_loop().run_in_executor(
            None, _run_code_local, full_code, time_limit
        )

    actual = raw["stdout"].strip()
    expected = expected_output.strip()
    passed = actual == expected

    return {
        "passed": passed,
        "actual_output": actual if not is_hidden else None,
        "expected_output": expected if not is_hidden else None,
        "is_hidden": is_hidden,
        "error": raw["stderr"] or (actual if actual.startswith("ERROR:") else None),
        "status": raw["status"],
        "description": description,
    }


async def run_all_tests(
    user_code: str,
    challenge,  # BossChallenge
) -> list[dict]:
    """Виконує всі тест-кейси для задачі боса."""
    is_safe, reason = sanitize_code(user_code)
    if not is_safe:
        return [{
            "passed": False,
            "actual_output": None,
            "expected_output": None,
            "is_hidden": tc.get("is_hidden", False),
            "error": reason,
            "status": "Security Error",
            "description": tc.get("description", ""),
        } for tc in challenge.test_cases]

    results = []
    for tc in challenge.test_cases:
        function_call = challenge.function_call_template.format(input=tc["input"])
        result = await run_test_case(
            user_code=user_code,
            function_call=function_call,
            expected_output=tc["expected_output"],
            is_hidden=tc.get("is_hidden", False),
            time_limit=challenge.time_limit_sec,
            memory_limit_mb=challenge.memory_limit_mb,
            description=tc.get("description", ""),
        )
        results.append(result)

    return results
