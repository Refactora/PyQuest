# PyQuest 🐍⚔️
RPG-гра для вивчення Python. Піксель-арт + бої + код.

## Вимоги
- Python 3.11
- Node.js 18+

## Запуск бекенду

### 1. Перейди в папку
```bash
cd backend
```

### 2. Створи віртуальне середовище
```bash
py -3.11 -m venv venv
```

### 3. Активуй його
```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 4. Встанови залежності
```bash
pip install -r requirements.txt
```

### 5. Запусти сервер
```bash
uvicorn app.main:app --reload
```

### 6. Відкрий в браузері
http://localhost:8000/docs

## Структура бекенду
backend/
├── app/
│   ├── api/          ← ендпоінти
│   ├── models/       ← таблиці БД
│   ├── schemas/      ← Pydantic схеми
│   ├── services/     ← бізнес-логіка
│   ├── core/         ← config, database, security
│   └── main.py
├── requirements.txt
└── venv/

## Що готово
- ✅ POST /api/auth/register
- ✅ POST /api/auth/login
- ✅ GET /api/auth/me
- ⏳ Локації, квіз, бос — в розробці