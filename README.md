# 🐍 PyQuest — Python RPG

Інтерактивна RPG-гра для вивчення Python. Воюй з крипами через квіз, перемагай босів розв'язуючи задачі.

---

## 🏗️ Структура проєкту

```
PyQuest/
├── backend/              # FastAPI + SQLite
│   ├── app/
│   │   ├── api/         # auth, locations, quiz, boss, profile, leaderboard
│   │   ├── core/        # config, database, security
│   │   ├── models/      # SQLAlchemy моделі
│   │   ├── schemas/     # Pydantic схеми
│   │   ├── services/    # xp_service, quiz_service, judge0_service
│   │   ├── seeds/       # seed_db.py — 10 локацій, 200 питань, 10 задач
│   │   └── main.py
│   ├── requirements.txt
│   └── run.sh
└── frontend/             # React + TypeScript + Tailwind
    ├── src/
    │   ├── components/  # ui/, game/, layout/
    │   ├── pages/       # Login, Register, Map, Location, Profile, Leaderboard
    │   ├── services/    # api.ts (axios)
    │   ├── store/       # authStore, gameStore (Zustand)
    │   └── types/       # TypeScript типи
    └── package.json
```

---

## 🚀 Швидкий старт

### Backend

```bash
cd backend

# 1. Встановити залежності
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Наповнити базу даних (локації, питання, задачі)
python -m app.seeds.seed_db

# 3. Запустити сервер
uvicorn app.main:app --reload

# Або одразу:
bash run.sh
```

Бекенд: http://localhost:8000  
Документація API: http://localhost:8000/docs

### Frontend

```bash
cd frontend

npm install
npm run dev
```

Фронтенд: http://localhost:5173

---

## 🔑 Налаштування (.env)

```env
# backend/.env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./pyquest.db

# Опціонально — для виконання коду у босс-файті
# Без цього ключа використовується локальний subprocess (тільки для розробки)
JUDGE0_API_KEY=your-rapidapi-key
```

**Judge0 API** (безкоштовний план): https://rapidapi.com/judge0-official/api/judge0-ce

---

## 🎮 Ігровий процес

1. **Реєстрація** → вибір аватара
2. **Карта** → 10 локацій, відкриваються послідовно
3. **Квіз** (по 10 питань):
   - Правильна відповідь → вбиваєш крипа, +10 XP
   - Неправильна → крип атакує (−1 HP)
   - HP = 0 → смерть, рестарт квізу
   - Пройшов квіз → відкривається бій з босом
4. **Бій з босом** (задача на код):
   - Пишеш Python функцію в редакторі Monaco
   - Відправляєш → запускаються тест-кейси
   - Кожен пройдений тест → −20 HP босу
   - Жоден не пройшов → бос атакує
   - Бос переможений → локація завершена, відкривається наступна
5. **Підказки**: 3 підказки (−10/−10/−15 HP)
6. **XP система**: рівні, досягнення, лідерборд

---

## 🏆 Локації

| # | Назва | Тема |
|---|-------|------|
| 1 | Рівнина Початку | Змінні та типи |
| 2 | Ліс Умов | if/elif/else |
| 3 | Печера Циклів | for/while |
| 4 | Вежа Функцій | def, lambda |
| 5 | Болото Списків | list, comprehension |
| 6 | Замок Словників | dict, set |
| 7 | Хмарний Острів | Рядки |
| 8 | Темний Ліс Помилок | try/except |
| 9 | Цитадель Класів | OOP |
| 10 | Фінальна Вежа | Модулі |

---

## 🔌 API Ендпоінти

```
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me

GET  /api/locations
GET  /api/locations/{slug}

POST /api/quiz/start
POST /api/quiz/answer
GET  /api/quiz/session/{id}

POST /api/boss/start
POST /api/boss/submit
POST /api/boss/hint

GET  /api/profile
PATCH /api/profile/avatar

GET  /api/leaderboard
```
