"""
Правильні задачі для босів — точно по ТЗ.
"""

BOSS_CHALLENGES = {
    "variables": {
        "title": "Переможи Змінного Хаоса: celsius_to_fahrenheit",
        "story_text": "Хаос переплутав всі температури у країні! Напиши конвертер щоб відновити порядок.",
        "task_text": (
            "Напиши функцію celsius_to_fahrenheit(celsius), яка конвертує температуру\n"
            "з Цельсія у Фаренгейт за формулою: F = C * 9/5 + 32\n\n"
            "Повертай результат округлений до 2 знаків після коми (round).\n\n"
            "Приклади:\n"
            "celsius_to_fahrenheit(0)   → 32.0\n"
            "celsius_to_fahrenheit(100) → 212.0\n"
            "celsius_to_fahrenheit(37)  → 98.6"
        ),
        "function_signature": "def celsius_to_fahrenheit(celsius):",
        "function_call_template": "celsius_to_fahrenheit({input})",
        "starter_code": "def celsius_to_fahrenheit(celsius):\n    # твій код тут\n    pass",
        "test_cases": [
            {"input": "0",   "expected_output": "32.0",  "is_hidden": False, "description": "Точка замерзання"},
            {"input": "100", "expected_output": "212.0", "is_hidden": False, "description": "Точка кипіння"},
            {"input": "37",  "expected_output": "98.6",  "is_hidden": False, "description": "Температура тіла"},
            {"input": "-40", "expected_output": "-40.0", "is_hidden": True,  "description": "Унікальна точка"},
            {"input": "20",  "expected_output": "68.0",  "is_hidden": True,  "description": "Кімнатна температура"},
        ],
        "hints": [
            {"order": 1, "text": "Формула: F = C * 9/5 + 32. Не забудь round(результат, 2).", "hp_cost": 10},
            {"order": 2, "text": "return round(celsius * 9 / 5 + 32, 2)", "hp_cost": 10},
            {"order": 3, "text": "def celsius_to_fahrenheit(celsius):\n    return round(celsius * 9 / 5 + 32, 2)", "hp_cost": 15},
        ],
    },

    "conditions": {
        "title": "Перехитри Вилку Долі: classify_number",
        "story_text": "Вилка Долі ставить числові загадки! Вона вимагає класифікувати числа.",
        "task_text": (
            "Напиши функцію classify_number(n), яка повертає рядок:\n"
            "- 'negative' якщо n < 0\n"
            "- 'zero' якщо n == 0\n"
            "- 'small positive' якщо 0 < n <= 10\n"
            "- 'large positive' якщо n > 10\n\n"
            "Приклади:\n"
            "classify_number(-5)  → 'negative'\n"
            "classify_number(0)   → 'zero'\n"
            "classify_number(7)   → 'small positive'\n"
            "classify_number(100) → 'large positive'"
        ),
        "function_signature": "def classify_number(n):",
        "function_call_template": "classify_number({input})",
        "starter_code": "def classify_number(n):\n    # твій код тут\n    pass",
        "test_cases": [
            {"input": "-5",  "expected_output": "negative",       "is_hidden": False, "description": "Від'ємне"},
            {"input": "0",   "expected_output": "zero",           "is_hidden": False, "description": "Нуль"},
            {"input": "7",   "expected_output": "small positive", "is_hidden": False, "description": "Мале позитивне"},
            {"input": "100", "expected_output": "large positive", "is_hidden": True,  "description": "Велике позитивне"},
            {"input": "10",  "expected_output": "small positive", "is_hidden": True,  "description": "Межове значення 10"},
        ],
        "hints": [
            {"order": 1, "text": "Перевіряй умови по черзі: спочатку n < 0, потім n == 0, потім n <= 10, інакше large.", "hp_cost": 10},
            {"order": 2, "text": "Використовуй if/elif/else. Чотири гілки — чотири результати.", "hp_cost": 10},
            {"order": 3, "text": "if n < 0: return 'negative'\nelif n == 0: return 'zero'\nelif n <= 10: return 'small positive'\nelse: return 'large positive'", "hp_cost": 15},
        ],
    },

    "loops": {
        "title": "Зупини Голема: sum_digits",
        "story_text": "Голем живиться сумою цифр! Обрахуй суму цифр числа щоб його знесилити.",
        "task_text": (
            "Напиши функцію sum_digits(n), яка повертає суму всіх цифр числа n.\n"
            "n — невід'ємне ціле число.\n\n"
            "Приклади:\n"
            "sum_digits(123)  → 6  (1+2+3)\n"
            "sum_digits(9999) → 36\n"
            "sum_digits(0)    → 0"
        ),
        "function_signature": "def sum_digits(n):",
        "function_call_template": "sum_digits({input})",
        "starter_code": "def sum_digits(n):\n    # твій код тут\n    pass",
        "test_cases": [
            {"input": "123",  "expected_output": "6",  "is_hidden": False, "description": "Базовий тест"},
            {"input": "9999", "expected_output": "36", "is_hidden": False, "description": "Чотири дев'ятки"},
            {"input": "0",    "expected_output": "0",  "is_hidden": False, "description": "Нуль"},
            {"input": "1000", "expected_output": "1",  "is_hidden": True,  "description": "Нулі не рахуються"},
            {"input": "99",   "expected_output": "18", "is_hidden": True,  "description": "Два числа"},
        ],
        "hints": [
            {"order": 1, "text": "Перетвори число на рядок: str(n). Потім ітеруй по символах, конвертуй int().", "hp_cost": 10},
            {"order": 2, "text": "sum(int(d) for d in str(n)) — компактне рішення через генератор.", "hp_cost": 10},
            {"order": 3, "text": "def sum_digits(n):\n    return sum(int(d) for d in str(n))", "hp_cost": 15},
        ],
    },

    "functions": {
        "title": "Розбери Дракона: is_palindrome",
        "story_text": "Дракон сховався у паліндромі! Знайди його перевіривши слово.",
        "task_text": (
            "Напиши функцію is_palindrome(s), яка повертає True якщо рядок\n"
            "є паліндромом (читається однаково з обох боків), False — інакше.\n"
            "Ігноруй регістр та пробіли.\n\n"
            "Приклади:\n"
            "is_palindrome('racecar')                       → True\n"
            "is_palindrome('A man a plan a canal Panama')   → True\n"
            "is_palindrome('hello')                         → False"
        ),
        "function_signature": "def is_palindrome(s):",
        "function_call_template": "is_palindrome({input})",
        "starter_code": "def is_palindrome(s):\n    # твій код тут\n    pass",
        "test_cases": [
            {"input": "'racecar'",                       "expected_output": "True",  "is_hidden": False, "description": "Простий паліндром"},
            {"input": "'hello'",                         "expected_output": "False", "is_hidden": False, "description": "Не паліндром"},
            {"input": "'A man a plan a canal Panama'",   "expected_output": "True",  "is_hidden": False, "description": "З пробілами"},
            {"input": "'level'",                         "expected_output": "True",  "is_hidden": True,  "description": "Ще один паліндром"},
            {"input": "'Python'",                        "expected_output": "False", "is_hidden": True,  "description": "Не паліндром 2"},
        ],
        "hints": [
            {"order": 1, "text": "Видали пробіли та приведи до нижнього регістру: s.lower().replace(' ', '')", "hp_cost": 10},
            {"order": 2, "text": "Порівняй рядок з його зворотом: cleaned == cleaned[::-1]", "hp_cost": 10},
            {"order": 3, "text": "cleaned = s.lower().replace(' ', '')\nreturn cleaned == cleaned[::-1]", "hp_cost": 15},
        ],
    },

    "lists": {
        "title": "Знищ Список-Пожирача: find_max",
        "story_text": "Пожирач вкрав максимум! Знайди найбільший елемент БЕЗ вбудованої функції max().",
        "task_text": (
            "Напиши функцію find_max(lst), яка повертає найбільший елемент списку.\n"
            "ЗАБОРОНЕНО використовувати вбудовану функцію max()!\n\n"
            "Приклади:\n"
            "find_max([3, 1, 4, 1, 5, 9, 2, 6]) → 9\n"
            "find_max([1])                        → 1\n"
            "find_max([-3, -1, -7])               → -1"
        ),
        "function_signature": "def find_max(lst):",
        "function_call_template": "find_max({input})",
        "starter_code": "def find_max(lst):\n    # Не використовуй max()!\n    pass",
        "test_cases": [
            {"input": "[3, 1, 4, 1, 5, 9, 2, 6]", "expected_output": "9",  "is_hidden": False, "description": "Базовий список"},
            {"input": "[1]",                        "expected_output": "1",  "is_hidden": False, "description": "Один елемент"},
            {"input": "[-3, -1, -7]",               "expected_output": "-1", "is_hidden": False, "description": "Від'ємні числа"},
            {"input": "[10, 10, 10]",               "expected_output": "10", "is_hidden": True,  "description": "Однакові"},
            {"input": "[0, 100, 50, 75]",           "expected_output": "100","is_hidden": True,  "description": "Різні значення"},
        ],
        "hints": [
            {"order": 1, "text": "Почни з того що припустиш: перший елемент — максимум. Потім ітеруй і порівнюй.", "hp_cost": 10},
            {"order": 2, "text": "current_max = lst[0]; for item in lst: if item > current_max: current_max = item", "hp_cost": 10},
            {"order": 3, "text": "def find_max(lst):\n    current_max = lst[0]\n    for item in lst:\n        if item > current_max:\n            current_max = item\n    return current_max", "hp_cost": 15},
        ],
    },

    "dicts": {
        "title": "Розкрий Ключ-Майстра: word_count",
        "story_text": "Майстер заховався у словнику слів! Порахуй кожне слово щоб його знайти.",
        "task_text": (
            "Напиши функцію word_count(text), яка приймає рядок і повертає\n"
            "словник де ключ — слово (в нижньому регістрі), значення — кількість входжень.\n\n"
            "Приклади:\n"
            "word_count('hello world hello') → {'hello': 2, 'world': 1}\n"
            "word_count('Hello hello HELLO') → {'hello': 3}"
        ),
        "function_signature": "def word_count(text):",
        "function_call_template": "word_count({input})",
        "starter_code": "def word_count(text):\n    # твій код тут\n    pass",
        "test_cases": [
            {"input": "'hello world hello'", "expected_output": "{'hello': 2, 'world': 1}", "is_hidden": False, "description": "Базовий тест"},
            {"input": "'Hello hello HELLO'", "expected_output": "{'hello': 3}",             "is_hidden": False, "description": "Різний регістр"},
            {"input": "'a b c a b a'",       "expected_output": "{'a': 3, 'b': 2, 'c': 1}", "is_hidden": False, "description": "Три слова"},
            {"input": "'one'",               "expected_output": "{'one': 1}",                "is_hidden": True,  "description": "Одне слово"},
            {"input": "'go go go go'",       "expected_output": "{'go': 4}",                 "is_hidden": True,  "description": "Одне слово 4 рази"},
        ],
        "hints": [
            {"order": 1, "text": "Розбий на слова через split() та приведи до lower(). Ітеруй по словах.", "hp_cost": 10},
            {"order": 2, "text": "counts[word] = counts.get(word, 0) + 1 — безпечне збільшення лічильника.", "hp_cost": 10},
            {"order": 3, "text": "counts = {}\nfor word in text.lower().split():\n    counts[word] = counts.get(word, 0) + 1\nreturn counts", "hp_cost": 15},
        ],
    },

    "strings": {
        "title": "Зруйнуй Ліча: format_name",
        "story_text": "Ліч знищує імена! Відновлюй їх правильним форматуванням.",
        "task_text": (
            "Напиши функцію format_name(first, last), яка повертає рядок у форматі:\n"
            "'Last, First' (Прізвище, Ім'я) з великої літери кожне слово.\n\n"
            "Приклади:\n"
            "format_name('john', 'doe')       → 'Doe, John'\n"
            "format_name('ALICE', 'SMITH')    → 'Smith, Alice'\n"
            "format_name('bob', 'van dyke')   → 'Van Dyke, Bob'"
        ),
        "function_signature": "def format_name(first, last):",
        "function_call_template": "format_name({input})",
        "starter_code": "def format_name(first, last):\n    # твій код тут\n    pass",
        "test_cases": [
            {"input": "'john', 'doe'",      "expected_output": "Doe, John",      "is_hidden": False, "description": "Базовий тест"},
            {"input": "'ALICE', 'SMITH'",   "expected_output": "Smith, Alice",   "is_hidden": False, "description": "Верхній регістр"},
            {"input": "'bob', 'van dyke'",  "expected_output": "Van Dyke, Bob",  "is_hidden": False, "description": "Складне прізвище"},
            {"input": "'ann', 'o brien'",   "expected_output": "O Brien, Ann",   "is_hidden": True,  "description": "Складне прізвище 2"},
            {"input": "'x', 'y'",           "expected_output": "Y, X",           "is_hidden": True,  "description": "Одна літера"},
        ],
        "hints": [
            {"order": 1, "text": "title() перетворює рядок так що кожне слово починається з великої літери.", "hp_cost": 10},
            {"order": 2, "text": "Формат: f'{last.title()}, {first.title()}'", "hp_cost": 10},
            {"order": 3, "text": "def format_name(first, last):\n    return f'{last.title()}, {first.title()}'", "hp_cost": 15},
        ],
    },

    "errors": {
        "title": "Переможи Баг-Лорда: safe_divide",
        "story_text": "Баг-Лорд кидає винятки на кожному кроці! Захисти ділення.",
        "task_text": (
            "Напиши функцію safe_divide(a, b), яка:\n"
            "- Повертає результат a / b (float)\n"
            "- Повертає None якщо b == 0\n"
            "- Повертає None якщо a або b не є числом (int або float)\n\n"
            "Приклади:\n"
            "safe_divide(10, 2)   → 5.0\n"
            "safe_divide(10, 0)   → None\n"
            "safe_divide('a', 2)  → None"
        ),
        "function_signature": "def safe_divide(a, b):",
        "function_call_template": "safe_divide({input})",
        "starter_code": "def safe_divide(a, b):\n    # твій код тут\n    pass",
        "test_cases": [
            {"input": "10, 2",   "expected_output": "5.0",  "is_hidden": False, "description": "Нормальне ділення"},
            {"input": "10, 0",   "expected_output": "None", "is_hidden": False, "description": "На нуль"},
            {"input": "'a', 2",  "expected_output": "None", "is_hidden": False, "description": "Не число"},
            {"input": "7, 2",    "expected_output": "3.5",  "is_hidden": True,  "description": "Float результат"},
            {"input": "0, 5",    "expected_output": "0.0",  "is_hidden": True,  "description": "Нуль в чисельнику"},
        ],
        "hints": [
            {"order": 1, "text": "isinstance(x, (int, float)) перевіряє тип. Перевір обидва аргументи.", "hp_cost": 10},
            {"order": 2, "text": "if b == 0: return None. Використай try/except для безпеки.", "hp_cost": 10},
            {"order": 3, "text": "if not isinstance(a,(int,float)) or not isinstance(b,(int,float)): return None\nif b == 0: return None\nreturn float(a/b)", "hp_cost": 15},
        ],
    },

    "oop": {
        "title": "Повали Колоса: Rectangle",
        "story_text": "Колос будує непробивні стіни з прямокутників! Створи клас Rectangle щоб розрахувати їх слабкі місця.",
        "task_text": (
            "Напиши клас Rectangle з:\n"
            "- __init__(self, width, height)\n"
            "- area(self) → width * height\n"
            "- perimeter(self) → 2 * (width + height)\n"
            "- is_square(self) → True якщо width == height\n"
            "- __str__(self) → 'Rectangle(width=W, height=H)'\n\n"
            "Тести перевіряють методи окремо через: Rectangle(4, 6).area() тощо"
        ),
        "function_signature": "class Rectangle:",
        "function_call_template": "Rectangle({input})",
        "starter_code": "class Rectangle:\n    def __init__(self, width, height):\n        pass\n\n    def area(self):\n        pass\n\n    def perimeter(self):\n        pass\n\n    def is_square(self):\n        pass\n\n    def __str__(self):\n        pass",
        "test_cases": [
            {"input": "4, 6",   "expected_output": "24",                      "is_hidden": False, "description": "area() для 4x6"},
            {"input": "3, 5",   "expected_output": "16",                      "is_hidden": False, "description": "perimeter() для 3x5"},
            {"input": "5, 5",   "expected_output": "True",                    "is_hidden": False, "description": "is_square() для 5x5"},
            {"input": "4, 6",   "expected_output": "False",                   "is_hidden": True,  "description": "is_square() для 4x6"},
            {"input": "3, 7",   "expected_output": "Rectangle(width=3, height=7)", "is_hidden": True, "description": "__str__"},
        ],
        "hints": [
            {"order": 1, "text": "В __init__ збережи: self.width = width, self.height = height.", "hp_cost": 10},
            {"order": 2, "text": "area: return self.width * self.height\nperimeter: return 2 * (self.width + self.height)\nis_square: return self.width == self.height", "hp_cost": 10},
            {"order": 3, "text": "__str__: return f'Rectangle(width={self.width}, height={self.height})'", "hp_cost": 15},
        ],
    },

    "modules": {
        "title": "Знищ Компілятора: days_until",
        "story_text": "Компілятор рахує дні до кінця світу! Визнач скільки залишилось.",
        "task_text": (
            "Напиши функцію days_until(date_str), яка приймає рядок дати\n"
            "у форматі 'YYYY-MM-DD' і повертає кількість днів від сьогодні до цієї дати.\n"
            "Якщо дата в минулому — від'ємне число.\n\n"
            "Використовуй модуль datetime.\n\n"
            "Приклади (відносно 2026-05-26):\n"
            "days_until('2026-06-26') → 31\n"
            "days_until('2026-05-26') → 0\n"
            "days_until('2026-05-19') → -7"
        ),
        "function_signature": "def days_until(date_str):",
        "function_call_template": "days_until({input})",
        "starter_code": "import datetime\n\ndef days_until(date_str):\n    # твій код тут\n    pass",
        "test_cases": [
            {"input": "'2026-06-26'", "expected_output": "31",  "is_hidden": False, "description": "Через місяць"},
            {"input": "'2026-05-26'", "expected_output": "0",   "is_hidden": False, "description": "Сьогодні"},
            {"input": "'2026-05-19'", "expected_output": "-7",  "is_hidden": False, "description": "Тиждень тому"},
            {"input": "'2026-12-31'", "expected_output": "219", "is_hidden": True,  "description": "Кінець року"},
            {"input": "'2027-05-26'", "expected_output": "365", "is_hidden": True,  "description": "Рік вперед"},
        ],
        "hints": [
            {"order": 1, "text": "target = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()", "hp_cost": 10},
            {"order": 2, "text": "today = datetime.date.today(). Різниця: (target - today).days", "hp_cost": 10},
            {"order": 3, "text": "import datetime\ndef days_until(date_str):\n    target = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()\n    return (target - datetime.date.today()).days", "hp_cost": 15},
        ],
    },
}
