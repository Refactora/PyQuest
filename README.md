# 🐍 PyQuest — Python RPG

> Вивчай Python через RPG-пригоду: б'єшся з крипами через квіз, перемагаєш босів розв'язуючи задачі.

---

## 🗂️ Структура

```
PyQuest/
├── backend/
│   ├── app/
│   │   ├── api/           auth · locations · quiz · boss · profile · leaderboard · daily_quests
│   │   ├── core/          config · database · security · redis
│   │   ├── models/        User · Location · Question · BossChallenge · Progress · DailyQuest
│   │   ├── schemas/       auth (з валідацією паролю та username regex)
│   │   ├── services/      xp_service · quiz_service · judge0_service · claude_service · daily_quest_service
│   │   └── seeds/         seed_db · questions (200 шт.) · boss_challenges (10 шт. по ТЗ)
│   ├── alembic/           міграції PostgreSQL
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/    ui · game · layout (з DailyQuestsPanel)
│   │   ├── pages/         Login · Register · Map · Location · Profile · Leaderboard · Achievements
│   │   ├── services/      api.ts (axios + авто-refresh)
│   │   ├── store/         authStore · gameStore (quiz + boss)
│   │   └── types/         повні TypeScript типи
│   └── .env.example
└── docker-compose.yml
```

---

## 🚀 Запуск через Docker (рекомендовано)

```bash
# 1. Скопіюй .env файли
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 2. Запустити все
docker-compose up --build

# Фронтенд: http://localhost:5173
# Бекенд:   http://localhost:8000
# API docs: http://localhost:8000/docs
```

---

## 🛠️ Запуск локально

### Backend

```bash
cd backend

# Встановити залежності
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Запустити PostgreSQL і Redis (або через Docker окремо):
docker run -d -p 5432:5432 -e POSTGRES_DB=pyquest -e POSTGRES_USER=pyquest -e POSTGRES_PASSWORD=devpassword postgres:16
docker run -d -p 6379:6379 redis:7

# Налаштувати .env
cp .env.example .env

# Міграції + seed
alembic upgrade head
python -m app.seeds.seed_db

# Запуск
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

---

## 🔑 .env змінні

| Змінна | Опис | Обов'язково |
|--------|------|-------------|
| `SECRET_KEY` | JWT секрет (≥32 символи) | ✅ |
| `DATABASE_URL` | PostgreSQL URL | ✅ |
| `REDIS_URL` | Redis URL | ✅ |
| `JUDGE0_API_KEY` | [RapidAPI Judge0](https://rapidapi.com/judge0-official/api/judge0-ce) — виконання коду | ❌* |
| `CLAUDE_API_KEY` | [Anthropic API](https://console.anthropic.com/) — AI підказки | ❌* |

> *Без ключів: Judge0 → локальний subprocess; Claude → статичні підказки.

---

## 🎮 Ігровий процес

1. **Реєстрація** — ім'я (`^[a-zA-Z0-9_]+$`), email, пароль (≥8 символів, літера+цифра), аватар
2. **Карта** — 10 локацій, відкриваються послідовно
3. **Квіз** (10 питань):
   - Правильно → вбиваєш крипа, +10 XP
   - Неправильно → крип атакує (−1 HP)
   - HP=0 → смерть, рестарт
4. **Бос** (задача на код, Monaco Editor):
   - Тести → шкода босу пропорційна до пройдених тестів
   - 0 тестів → бос атакує
   - 3 підказки: статичні (−HP) + AI (після 2 спроб, без HP)
5. **Щоденні квести** — 3 квести/день у navbar dropdown
6. **XP → рівні → ачівменти → лідерборд**

---

## 🏆 10 Локацій та задачі босів (по ТЗ)

| # | Локація | Тема квізу | Задача боса |
|---|---------|-----------|-------------|
| 1 | Рівнина Початку | Змінні та типи | `celsius_to_fahrenheit(c)` |
| 2 | Ліс Умов | if/elif/else | `classify_number(n)` |
| 3 | Печера Циклів | for/while | `sum_digits(n)` |
| 4 | Вежа Функцій | def/lambda | `is_palindrome(s)` |
| 5 | Болото Списків | list/comprehension | `find_max(lst)` без max() |
| 6 | Замок Словників | dict/set | `word_count(text)` |
| 7 | Хмарний Острів | Рядки/f-strings | `format_name(first, last)` |
| 8 | Ліс Помилок | try/except | `safe_divide(a, b)` |
| 9 | Цитадель Класів | OOP | клас `Rectangle` |
| 10 | Фінальна Вежа | Модулі | `days_until(date_str)` |

---

## 🔌 API ендпоінти

```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/refresh
POST   /api/auth/logout
GET    /api/auth/me

GET    /api/locations
GET    /api/locations/{slug}
POST   /api/locations/{slug}/enter

POST   /api/quiz/start
POST   /api/quiz/answer
POST   /api/quiz/abandon
GET    /api/quiz/session/{id}

POST   /api/boss/start
POST   /api/boss/submit
POST   /api/boss/hint
POST   /api/boss/ai-hint

GET    /api/profile
PATCH  /api/profile/avatar

GET    /api/leaderboard?period=all|weekly

GET    /api/daily-quests
```

---

## 🏅 Ачівменти (14 шт.)

`first_blood` · `no_death_1` · `boss_slayer` · `all_bosses` · `perfectionist` · `first_try` · `no_hints` · `streak_3` · `streak_7` · `streak_30` · `speed_run` · `completionist` · `level_10` · `level_20`
