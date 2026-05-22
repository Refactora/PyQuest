# ТЗ — PyQuest: Повна Специфікація
### Платформа для вивчення Python у стилі піксель-арт RPG
**Версія:** 2.0 FULL  
**Статус:** Основний документ розробки

---

# ЗМІСТ

1. [Загальний опис](#1-загальний-опис)
2. [Архітектура системи](#2-архітектура-системи)
3. [База даних — повна схема](#3-база-даних)
4. [Авторизація та профіль](#4-авторизація-та-профіль)
5. [Карта світу та локації](#5-карта-світу-та-локації)
6. [Ігровий процес — Quiz Mode](#6-quiz-mode--бій-з-крипами)
7. [Ігровий процес — Boss Fight](#7-boss-fight--бій-з-босом)
8. [Система прогресії](#8-система-прогресії)
9. [Соціальні механіки](#9-соціальні-механіки)
10. [Повний контент (питання + задачі)](#10-контент)
11. [API — всі ендпоінти](#11-api)
12. [Фронтенд — компоненти](#12-фронтенд)
13. [Графіка та дизайн](#13-графіка-та-дизайн)
14. [Перевірка коду](#14-перевірка-коду)
15. [AI-інтеграція](#15-ai-інтеграція)
16. [Безпека](#16-безпека)
17. [Поетапний план розробки](#17-поетапний-план-розробки)
18. [Деплой та інфраструктура](#18-деплой)
19. [Тестування](#19-тестування)

---

# 1. ЗАГАЛЬНИЙ ОПИС

## 1.1 Продукт

**PyQuest** — браузерна RPG-гра для вивчення Python. Гравець керує піксель-арт героєм, який подорожує картою світу, де кожна локація = тема Python. У кожній локації два типи боїв:

- **Quiz Fight (Крипи)** — відповідаєш на питання теорії → правильна відповідь = герой атакує крипа → неправильна = крип б'є героя
- **Boss Fight** — пишеш Python-код для вирішення задачі → код виконується в пісочниці → правильний output = бос отримує шкоду

## 1.2 Ключові принципи

| Принцип | Опис |
|---|---|
| Гра понад усе | Навчання відбувається через геймплей, а не лекції |
| Негайний фідбек | Кожна дія має візуальну і текстову відповідь |
| Прогресія видима | Гравець завжди бачить свій прогрес |
| Помилка — не кінець | Death → restart, але не втрата прогресу назавжди |
| Простота UI | Піксель-арт, без перевантаження |

## 1.3 Платформи

- **MVP**: Web (Desktop-first, адаптив для планшета)
- **v2**: Mobile Web (PWA)
- **v3**: React Native app

---

# 2. АРХІТЕКТУРА СИСТЕМИ

## 2.1 Загальна схема

```
┌─────────────────────────────────────────────┐
│                  КЛІЄНТ                      │
│         React + TypeScript + Vite            │
│  Tailwind CSS / Pixi.js (анімації спрайтів)  │
└────────────────────┬────────────────────────┘
                     │ HTTPS / REST API
┌────────────────────▼────────────────────────┐
│               БЕКЕНД (API)                   │
│            FastAPI (Python)                  │
│         JWT Auth / Rate Limiting             │
└──────┬─────────────┬──────────────┬─────────┘
       │             │              │
┌──────▼──────┐ ┌────▼────┐ ┌──────▼──────┐
│ PostgreSQL  │ │  Redis  │ │ Judge0 API  │
│  (основна   │ │ (сесії, │ │ (виконання  │
│    БД)      │ │ кеш)    │ │   коду)     │
└─────────────┘ └─────────┘ └──────┬──────┘
                                    │
                            ┌───────▼──────┐
                            │ Claude API   │
                            │ (підказки,   │
                            │  пояснення)  │
                            └──────────────┘
```

## 2.2 Вибір технологій — обґрунтування

### Бекенд: FastAPI (Python)
- Вивчаємо Python → пишемо на Python (синергія)
- Автогенерація Swagger документації
- Async з коробки
- Pydantic для валідації

### Фронтенд: React + TypeScript
- Компонентна архітектура = легко підтримувати
- TypeScript = менше багів з AI-генерацією
- Vite = швидка розробка

### Піксель-арт анімації: Pixi.js
- Рендер спрайтів через WebGL
- Підтримка spritesheets
- Висока продуктивність для анімацій

### БД: PostgreSQL
- JSON поля для test cases та hints
- Повнотекстовий пошук (для v2)
- Надійність і масштабованість

### Кеш: Redis
- Зберігання сесій квізу (поточні питання, стан HP)
- Кеш лідерборду
- Rate limiting лічильники

## 2.3 Структура репозиторію

```
pyquest/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── locations.py
│   │   │   ├── quiz.py
│   │   │   ├── boss.py
│   │   │   ├── profile.py
│   │   │   └── leaderboard.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── location.py
│   │   │   ├── question.py
│   │   │   ├── boss_challenge.py
│   │   │   └── progress.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── quiz_service.py
│   │   │   ├── judge0_service.py
│   │   │   ├── claude_service.py
│   │   │   └── xp_service.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── redis.py
│   │   │   └── security.py
│   │   └── main.py
│   ├── migrations/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/          ← базові UI компоненти
│   │   │   ├── game/        ← ігрові компоненти
│   │   │   └── layout/      ← лейаут компоненти
│   │   ├── pages/
│   │   ├── store/           ← Zustand state management
│   │   ├── hooks/
│   │   ├── services/        ← API calls
│   │   ├── assets/
│   │   │   ├── sprites/
│   │   │   ├── backgrounds/
│   │   │   └── sounds/
│   │   └── types/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# 3. БАЗА ДАНИХ

## 3.1 Повна схема (PostgreSQL)

```sql
-- ============================================
-- КОРИСТУВАЧІ
-- ============================================

CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username        VARCHAR(30) UNIQUE NOT NULL,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    avatar_id       INTEGER NOT NULL DEFAULT 1,      -- 1=Маг, 2=Воїн, 3=Лучник, 4=Хакер
    level           INTEGER NOT NULL DEFAULT 1,
    xp              INTEGER NOT NULL DEFAULT 0,
    xp_to_next      INTEGER NOT NULL DEFAULT 100,
    total_xp        INTEGER NOT NULL DEFAULT 0,      -- за все час (для лідерборду)
    hp_max          INTEGER NOT NULL DEFAULT 5,
    streak_days     INTEGER NOT NULL DEFAULT 0,
    last_active     TIMESTAMP,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- ЛОКАЦІЇ (ТЕМИ)
-- ============================================

CREATE TABLE locations (
    id              SERIAL PRIMARY KEY,
    slug            VARCHAR(50) UNIQUE NOT NULL,
    name            VARCHAR(100) NOT NULL,
    description     TEXT NOT NULL,
    topic           VARCHAR(100) NOT NULL,
    order_index     INTEGER UNIQUE NOT NULL,
    boss_name       VARCHAR(100) NOT NULL,
    boss_sprite_id  VARCHAR(50) NOT NULL,
    background_id   VARCHAR(50) NOT NULL,
    enemy_sprite_id VARCHAR(50) NOT NULL,
    color_theme     VARCHAR(7) NOT NULL,            -- hex колір для UI
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- ПИТАННЯ (КВІЗ)
-- ============================================

CREATE TABLE questions (
    id              SERIAL PRIMARY KEY,
    location_id     INTEGER REFERENCES locations(id),
    question_text   TEXT NOT NULL,
    code_snippet    TEXT,                           -- NULL якщо немає коду у питанні
    option_a        TEXT NOT NULL,
    option_b        TEXT NOT NULL,
    option_c        TEXT NOT NULL,
    option_d        TEXT NOT NULL,
    correct_option  CHAR(1) NOT NULL CHECK (correct_option IN ('a','b','c','d')),
    explanation     TEXT NOT NULL,                  -- пояснення правильної відповіді
    difficulty      INTEGER DEFAULT 1 CHECK (difficulty BETWEEN 1 AND 3),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- ЗАДАЧІ ДЛЯ БОСА
-- ============================================

CREATE TABLE boss_challenges (
    id              SERIAL PRIMARY KEY,
    location_id     INTEGER UNIQUE REFERENCES locations(id),
    title           VARCHAR(200) NOT NULL,
    story_text      TEXT NOT NULL,                  -- сюжетна підводка
    task_text       TEXT NOT NULL,                  -- умова задачі
    function_signature VARCHAR(100) NOT NULL,       -- наприклад: "def find_max(lst):"
    starter_code    TEXT NOT NULL,                  -- початковий код у редакторі
    test_cases      JSONB NOT NULL,
    hints           JSONB NOT NULL,                 -- масив з 3 підказок
    boss_hp         INTEGER NOT NULL DEFAULT 100,
    time_limit_sec  INTEGER NOT NULL DEFAULT 10,
    memory_limit_mb INTEGER NOT NULL DEFAULT 128,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- ПРОГРЕС ГРАВЦЯ ПО ЛОКАЦІЯХ
-- ============================================

CREATE TABLE user_location_progress (
    id                  SERIAL PRIMARY KEY,
    user_id             UUID REFERENCES users(id) ON DELETE CASCADE,
    location_id         INTEGER REFERENCES locations(id),
    status              VARCHAR(20) DEFAULT 'locked'
                            CHECK (status IN ('locked','available','in_progress','completed')),
    quiz_completed      BOOLEAN DEFAULT FALSE,
    boss_defeated       BOOLEAN DEFAULT FALSE,
    best_quiz_score     INTEGER DEFAULT 0,          -- макс правильних без смертей
    quiz_attempts       INTEGER DEFAULT 0,
    boss_attempts       INTEGER DEFAULT 0,
    hints_used          INTEGER DEFAULT 0,
    first_try_boss      BOOLEAN DEFAULT FALSE,      -- перемога над босом з першої спроби
    no_death_run        BOOLEAN DEFAULT FALSE,      -- без жодної смерті
    completed_at        TIMESTAMP,
    UNIQUE(user_id, location_id)
);

-- ============================================
-- СЕСІЇ КВІЗУ (активні бої)
-- ============================================

CREATE TABLE quiz_sessions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID REFERENCES users(id) ON DELETE CASCADE,
    location_id         INTEGER REFERENCES locations(id),
    questions_order     INTEGER[] NOT NULL,         -- перемішаний порядок питань
    current_index       INTEGER DEFAULT 0,          -- поточне питання (0-9)
    hero_hp             INTEGER NOT NULL,
    correct_answers     INTEGER DEFAULT 0,
    wrong_answers       INTEGER DEFAULT 0,
    started_at          TIMESTAMP DEFAULT NOW(),
    completed_at        TIMESTAMP,
    is_active           BOOLEAN DEFAULT TRUE
);

-- ============================================
-- СЕСІЇ БОЯ З БОСОМ
-- ============================================

CREATE TABLE boss_sessions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID REFERENCES users(id) ON DELETE CASCADE,
    challenge_id        INTEGER REFERENCES boss_challenges(id),
    hero_hp             INTEGER NOT NULL,
    boss_hp             INTEGER NOT NULL,
    hints_used          INTEGER DEFAULT 0,
    submissions         JSONB DEFAULT '[]',         -- масив спроб [{code, output, passed, timestamp}]
    started_at          TIMESTAMP DEFAULT NOW(),
    completed_at        TIMESTAMP,
    is_won              BOOLEAN,
    is_active           BOOLEAN DEFAULT TRUE
);

-- ============================================
-- ЩОДЕННІ КВЕСТИ
-- ============================================

CREATE TABLE daily_quests (
    id              SERIAL PRIMARY KEY,
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    quest_date      DATE NOT NULL DEFAULT CURRENT_DATE,
    quest_type      VARCHAR(50) NOT NULL,
    description     TEXT NOT NULL,
    target_value    INTEGER NOT NULL,
    current_value   INTEGER DEFAULT 0,
    xp_reward       INTEGER NOT NULL,
    is_completed    BOOLEAN DEFAULT FALSE,
    completed_at    TIMESTAMP,
    UNIQUE(user_id, quest_date, quest_type)
);

-- ============================================
-- АЧІВМЕНТИ
-- ============================================

CREATE TABLE achievements (
    id              SERIAL PRIMARY KEY,
    slug            VARCHAR(50) UNIQUE NOT NULL,
    name            VARCHAR(100) NOT NULL,
    description     TEXT NOT NULL,
    icon_id         VARCHAR(50) NOT NULL,
    xp_reward       INTEGER DEFAULT 0
);

CREATE TABLE user_achievements (
    id              SERIAL PRIMARY KEY,
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    achievement_id  INTEGER REFERENCES achievements(id),
    unlocked_at     TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, achievement_id)
);

-- ============================================
-- ІНДЕКСИ
-- ============================================

CREATE INDEX idx_questions_location ON questions(location_id) WHERE is_active = TRUE;
CREATE INDEX idx_user_progress_user ON user_location_progress(user_id);
CREATE INDEX idx_quiz_sessions_user ON quiz_sessions(user_id) WHERE is_active = TRUE;
CREATE INDEX idx_boss_sessions_user ON boss_sessions(user_id) WHERE is_active = TRUE;
CREATE INDEX idx_users_xp ON users(total_xp DESC);
CREATE INDEX idx_daily_quests_user_date ON daily_quests(user_id, quest_date);
```

## 3.2 JSONB структури

### test_cases (boss_challenges):
```json
[
  {
    "input": "[3, 1, 4, 1, 5]",
    "expected_output": "5",
    "is_hidden": false,
    "description": "Базовий тест"
  },
  {
    "input": "[-1, -5, -3]",
    "expected_output": "-1",
    "is_hidden": false,
    "description": "Негативні числа"
  },
  {
    "input": "[42]",
    "expected_output": "42",
    "is_hidden": true,
    "description": "Один елемент (прихований)"
  }
]
```

### hints (boss_challenges):
```json
[
  {
    "order": 1,
    "text": "Подумай про те, як перебрати всі елементи списку і знайти найбільший",
    "hp_cost": 10
  },
  {
    "order": 2,
    "text": "Спробуй почати з першого елементу як 'поточний максимум' і оновлювати його у циклі",
    "hp_cost": 10
  },
  {
    "order": 3,
    "text": "for item in lst: if item > current_max: ...",
    "hp_cost": 15
  }
]
```

### submissions (boss_sessions):
```json
[
  {
    "attempt": 1,
    "code": "def find_max(lst):\n    return lst[0]",
    "test_results": [
      {"input": "[3,1,4]", "expected": "4", "got": "3", "passed": false}
    ],
    "passed_count": 0,
    "total_count": 3,
    "timestamp": "2026-05-21T10:30:00Z"
  }
]
```

---

# 4. АВТОРИЗАЦІЯ ТА ПРОФІЛЬ

## 4.1 Реєстрація

**Поля:**
- `username` — 3-30 символів, тільки латиниця/цифри/підкреслення, унікальний
- `email` — валідний email, унікальний
- `password` — мінімум 8 символів
- `avatar_id` — вибір персонажа (1-4)

**Процес:**
1. Валідація на фронті (React Hook Form + Zod)
2. POST `/api/auth/register`
3. Бекенд: валідація → хеш паролю (bcrypt, rounds=12) → створення user → створення progress для всіх локацій (перша = `available`, решта = `locked`) → генерація JWT → відповідь з токеном
4. Фронт зберігає JWT у `httpOnly cookie`
5. Редірект на карту світу

**Початковий стан після реєстрації:**
```python
# Автоматично створюється для кожного нового юзера:
for i, location in enumerate(all_locations):
    UserLocationProgress(
        user_id=user.id,
        location_id=location.id,
        status='available' if i == 0 else 'locked'
    )

# 3 щоденні квести
generate_daily_quests(user.id)
```

## 4.2 Авторизація

- JWT токен: access (24 год) + refresh (30 днів)
- Access token у `Authorization: Bearer` header
- Refresh token у `httpOnly cookie`
- При 401 → автоматичний refresh → якщо не вдалося → логаут

## 4.3 Персонажі (Аватари)

| ID | Клас | Опис |
|---|---|---|
| 1 | Маг Коду | Фіолетовий мантія, посох зі знаком `{}` |
| 2 | Воїн Синтаксису | Синій обладунок, меч у формі `>_` |
| 3 | Лучниця Дебагер | Зелений колір, лук зі стрілами-курсорами |
| 4 | Хакер-Тінь | Чорний плащ, маска, ноутбук |

## 4.4 Профіль гравця (сторінка)

**Відображає:**
- Аватар + ім'я + рівень + звання
- XP прогрес-бар до наступного рівня
- Статистика: пройдено локацій / вбито крипів / вбито босів / загальний XP
- Streak (дні підряд)
- Пройдені локації з датами
- Розблоковані ачівменти

---

# 5. КАРТА СВІТУ ТА ЛОКАЦІЇ

## 5.1 Локації — повний список

| # | Slug | Назва | Тема | Бос | Крипи |
|---|---|---|---|---|---|
| 1 | variables | Рівнина Початку | Змінні та типи даних | Змінний Хаос | Іменовані Примари |
| 2 | conditions | Ліс Умов | if/elif/else | Вилка Долі | Розгалужені Тіні |
| 3 | loops | Печера Циклів | for/while/break/continue | Нескінченний Голем | Циклічні Духи |
| 4 | functions | Вежа Функцій | def, return, args, kwargs | Рекурсивний Дракон | Аргументні Елементалі |
| 5 | lists | Болото Списків | list, методи, зрізи | Список-Пожирач | Індексні Слімі |
| 6 | dicts | Замок Словників | dict, set, frozenset | Ключ-Майстер | Хеш-Привиди |
| 7 | strings | Хмарний Острів | str, методи рядків, f-strings | Форматований Ліч | Символьні Феї |
| 8 | errors | Темний Ліс | try/except/finally, raise | Баг-Лорд | Виняткові Монстри |
| 9 | oop | Цитадель Класів | class, __init__, наслідування | Об'єктний Колос | Інстанс-Зомбі |
| 10 | modules | Фінальна Вежа | import, os, datetime, json | Темний Компілятор | Модульні Варти |

## 5.2 Детальні дані кожної локації

### Локація 1: Рівнина Початку
```
slug: variables
name: Рівнина Початку
description: Безкраї поля, де все починається. Тут ти вперше дізнаєшся,
             як зберігати і використовувати дані.
topic: Змінні та типи даних (int, float, str, bool, None)
boss_name: Змінний Хаос
color_theme: #7BC67E (зелений)
background: green_plains
enemy_sprite: named_ghost
boss_sprite: chaos_boss
```

### Локація 2: Ліс Умов
```
slug: conditions
name: Ліс Умов
description: Густий ліс, де кожна стежка розгалужується. Тільки правильна
             умова приведе тебе до виходу.
topic: Умовні оператори (if, elif, else, and, or, not, порівняння)
boss_name: Вилка Долі
color_theme: #5B9BD5 (синій)
background: dark_forest
enemy_sprite: branch_shadow
boss_sprite: fork_boss
```

*(аналогічно для 3-10)*

## 5.3 Поведінка карти

```
Логіка відображення локацій:

locked     → сіра іконка + анімований замок зверху
available  → кольорова іконка + пульсуючий ефект + "Розпочати"
in_progress→ кольорова іконка + анімований індикатор прогресу
completed  → кольорова іконка + золота зірка + число спроб

При кліку на completed → показати статистику проходження
При кліку на available/in_progress → перейти до локації
При кліку на locked → показати: "Спочатку пройди [попередня локація]"
```

## 5.4 Вхід у локацію (Lobby Screen)

Перед початком бою показується екран лобі:
- Назва локації та опис
- Тема Python (короткий огляд, 3-4 речення)
- Що на тебе чекає: "10 питань + фінальний бос [ім'я боса]"
- Статистика попередніх спроб (якщо є)
- Кнопка "Почати бій!"

---

# 6. QUIZ MODE — БІЙ З КРИПАМИ

## 6.1 Ініціалізація квізу

```python
# backend/services/quiz_service.py

def start_quiz_session(user_id: UUID, location_id: int) -> QuizSession:
    # 1. Перевірити що локація доступна для юзера
    # 2. Закрити попередню активну сесію (якщо є)
    # 3. Отримати всі активні питання для локації
    # 4. Перемішати і взяти 10
    # 5. Отримати hp_max юзера
    # 6. Створити сесію в БД
    # 7. Зберегти сесію в Redis (ключ: quiz:{user_id}, TTL: 2 год)
    # 8. Повернути першу питання
    
    questions = get_questions_for_location(location_id)  # 20-30 питань
    shuffled_ids = shuffle(questions.ids)[:10]
    
    session = QuizSession(
        user_id=user_id,
        location_id=location_id,
        questions_order=shuffled_ids,
        hero_hp=user.hp_max,  # 5
        current_index=0
    )
    return session
```

## 6.2 Структура відповіді на питання

```python
# POST /api/quiz/answer
# Запит:
{
    "session_id": "uuid",
    "question_id": 42,
    "selected_option": "b"
}

# Відповідь (правильна):
{
    "is_correct": true,
    "correct_option": "b",
    "explanation": "...",
    "xp_gained": 10,
    "hero_hp": 5,
    "creep_killed": true,
    "questions_left": 7,
    "is_quiz_done": false
}

# Відповідь (неправильна):
{
    "is_correct": false,
    "correct_option": "b",
    "explanation": "...",
    "xp_gained": 0,
    "hero_hp": 4,        # -1 HP
    "hero_died": false,
    "questions_left": 7,
    "is_quiz_done": false
}

# Відповідь (смерть героя):
{
    "is_correct": false,
    "correct_option": "b",
    "explanation": "...",
    "hero_hp": 0,
    "hero_died": true,
    "is_quiz_done": false,
    "restart_message": "Герой загинув! Починаємо заново..."
}

# Відповідь (квіз завершено):
{
    "is_quiz_done": true,
    "final_score": 8,        # правильних з 10
    "xp_gained": 80,
    "bonus_xp": 0,           # 0 або 25 (no_death_run)
    "next_step": "boss_fight"
}
```

## 6.3 Балансування

```
HP героя: 5 (збільшується при level up: +1 кожні 5 рівнів)
Шкода від крипа: 1 HP за неправильну відповідь
XP за правильну відповідь: 10
XP за завершення квізу: 50
Бонус XP "Без смертей": +25
Бонус XP "10/10 правильних": +30
```

## 6.4 Restart механіка

При смерті (HP = 0):
1. Сесія закривається (completed_at ставиться)
2. `quiz_attempts` збільшується на 1
3. Рахунок не зберігається
4. Нова сесія починається з нових перемішаних питань
5. Показується екран "Герой загинув!" з анімацією та кнопкою "Спробувати знову"

## 6.5 UI стан бою (Quiz)

```
┌──────────────────────────────────────────┐
│ Тема: Змінні            Питання: 3/10    │
│ ████████░░  HP: 4/5                      │
├──────────────────────────────────────────┤
│                                          │
│  [Герой]    ⚔️          [Крип]          │
│   idle                   idle            │
│                                          │
├──────────────────────────────────────────┤
│  Що виведе print(type(42))?              │
│                                          │
│  A) <class 'str'>                        │
│  B) <class 'int'>     ← правильна        │
│  C) <class 'float'>                      │
│  D) int                                  │
└──────────────────────────────────────────┘
```

**Анімаційні стани:**
- `idle` — персонаж легко коливається (looped)
- `attack` — герой рухається вперед, удар, відходить (1.5s)
- `hit` — крип трусить + червоніє (0.5s)
- `die` — крип розсипається на пікселі (1s)
- `enemy_attack` — крип рухається до героя, удар (1.5s)
- `player_hit` — герой трусить + мигтить (0.5s)
- `player_die` — герой падає (2s) → fade out

**Послідовність при правильній відповіді:**
1. Кнопка відповіді підсвічується зеленим (0.3s)
2. Герой → анімація `attack` (1.5s)
3. Крип → анімація `hit` → якщо останній → `die` (1s)
4. +10 XP спливає зверху (float up animation)
5. Якщо не останній крип: наступний крип з'являється
6. Завантажується наступне питання

**Послідовність при неправильній відповіді:**
1. Вибрана кнопка → червона; правильна → зелена (0.3s)
2. Блок пояснення з'являється знизу (slide up)
3. Крип → анімація `enemy_attack` (1.5s)
4. Герой → анімація `player_hit`
5. HP-бар оновлюється
6. Кнопка "Продовжити" → наступне питання

---

# 7. BOSS FIGHT — БІЙ З БОСОМ

## 7.1 Перехід до боса

Після успішного завершення квізу (10 питань, герой живий):
1. Анімація перемоги над крипами
2. Екран переходу: "Ти наближаєшся до боса..." (3s анімація)
3. Бос-арена завантажується зі своїм фоном
4. Boss intro: бос з'являється з анімацією + текст сюжетної підводки
5. Кнопка "Прийняти виклик!"

## 7.2 Арена боса — UI

```
┌──────────────────────────────────────────────────────┐
│  БОС: Змінний Хаос       [HP: ████████░░░  80/100]   │
│  ТИ:  [HP: ████░  4/5]                               │
├─────────────────────┬────────────────────────────────┤
│                     │ 📋 Задача:                      │
│   [БОС - велика     │                                │
│    піксель-арт      │ Напиши функцію swap_values()   │
│    ілюстрація]      │ яка приймає два числа a і b,   │
│                     │ і повертає їх у зміненому      │
│   [анімація idle]   │ порядку як tuple (b, a)        │
│                     │                                │
│   💥 Атака!         │ Приклад:                        │
│   (флеш при ударі)  │ swap_values(3, 7) → (7, 3)    │
│                     │                                │
│  [Підказка 1] [💡2] │ def swap_values(a, b):         │
│  [Підказка 3]       │     # твій код тут            │
│  (залишилось: 2)    │     pass                       │
│                     │                                │
│                     │ [Monaco Editor - Python]       │
│                     │                                │
│                     │     [⚔️ АТАКУВАТИ!]            │
└─────────────────────┴────────────────────────────────┘
```

## 7.3 Механіка бою з босом

```
Boss HP: 100 (завжди, незалежно від локації)

Структура test cases для кожної задачі: 5 тестів
  - 3 відкриті (гравець бачить input/output)
  - 2 приховані (тільки "прихований тест")

Шкода при відправці:
  - Кожен пройдений тест: -20 HP боса
  - Якщо всі 5 пройшли → бос помирає (0 HP)
  - Якщо 0 пройшли → бос атакує героя (-1 HP)
  - Якщо частково пройшли → бос відштовхується, 
    але не атакує (нічия раунду)

Тобто:
  1/5 тестів → -20 HP бос, герой не отримує шкоди
  3/5 тестів → -60 HP бос
  5/5 тестів → бос мертвий, перемога!
  0/5 тестів → бос атакує, герой -1 HP
```

## 7.4 Система підказок у бос-файті

```
Підказки: 3 штуки (фіксовано)

Підказка 1: загальний напрямок (-10 HP героя)
Підказка 2: конкретна порада (-10 HP героя)  
Підказка 3: майже-відповідь (-15 HP героя)

Якщо герой HP = 0 під час бос-файту:
  → Бос переміг!
  → boss_attempts + 1
  → Гравець може:
     a) Спробувати знову (герой HP відновлюється до max)
     b) Повернутися до квізу (якщо хоче перекачатись через XP)
```

## 7.5 Перевірка коду

```python
# backend/services/judge0_service.py

async def submit_code(
    code: str, 
    challenge: BossChallenge,
    session_id: UUID
) -> SubmissionResult:
    
    results = []
    for test_case in challenge.test_cases:
        # Обгортаємо код викликом функції
        full_code = f"""
{code}

# Test runner
result = {challenge.function_call_template.format(input=test_case['input'])}
print(result)
"""
        response = await judge0_api.submit(
            source_code=full_code,
            language_id=71,  # Python 3.8
            time_limit=challenge.time_limit_sec,
            memory_limit=challenge.memory_limit_mb * 1024
        )
        
        actual_output = response.stdout.strip()
        expected_output = test_case['expected_output'].strip()
        
        results.append({
            "test_case": test_case,
            "actual": actual_output,
            "passed": actual_output == expected_output,
            "is_hidden": test_case['is_hidden'],
            "error": response.stderr if response.stderr else None
        })
    
    return SubmissionResult(results=results)
```

## 7.6 Перемога над босом

1. Анімація смерті боса (pixel explosion, 3s)
2. Екран перемоги:
   - "ПЕРЕМОЖЕНО!" великим піксельним текстом
   - XP earned: +150 (базово) + бонуси
   - Бонус "З першої спроби": +50 XP
   - Бонус "Без підказок": +30 XP
3. Якщо новий рівень → level up анімація
4. Якщо нове ачівмент → показати картку
5. Наступна локація розблоковується (анімація на карті)
6. Кнопка "На карту"

---

# 8. СИСТЕМА ПРОГРЕСІЇ

## 8.1 XP та Рівні

```python
def xp_for_level(level: int) -> int:
    """XP потрібно для досягнення рівня level"""
    return int(100 * (level ** 1.5))

# Рівні:
# 1: 0 XP       (старт)
# 2: 100 XP
# 3: 260 XP
# 4: 490 XP
# 5: 790 XP
# 10: 3162 XP
# 15: 8697 XP
# 20: 17889 XP
```

## 8.2 Таблиця XP-нагород

| Дія | XP |
|---|---|
| Правильна відповідь у квізі | +10 |
| Завершення квізу | +50 |
| Квіз без смертей | +25 бонус |
| Квіз 10/10 правильних | +30 бонус |
| Перший пройдений тест боса | +20 |
| Перемога над босом | +150 |
| Бос з першої спроби | +50 бонус |
| Бос без підказок | +30 бонус |
| Щоденний квест | +20-50 |
| Ачівмент | +0-100 |
| Стрік 7 днів | +100 |

## 8.3 Звання

| Рівень | Звання | Іконка |
|---|---|---|
| 1-2 | Новачок-Кодер | 🌱 |
| 3-5 | Юний Маг Коду | ✨ |
| 6-9 | Мисливець на Баги | 🐛 |
| 10-14 | Лицар Синтаксису | ⚔️ |
| 15-19 | Архімаг Функцій | 🔮 |
| 20-24 | Лорд Алгоритмів | 👑 |
| 25+ | Легенда PyQuest | 🏆 |

## 8.4 HP Heroя зі зростанням рівня

```
Рівень 1-4:   HP max = 5
Рівень 5-9:   HP max = 6
Рівень 10-14: HP max = 7
Рівень 15-19: HP max = 8
Рівень 20+:   HP max = 10
```

## 8.5 Ачівменти — повний список

| Slug | Назва | Умова | XP |
|---|---|---|---|
| first_blood | Перший Крип | Правильна відповідь №1 | 10 |
| no_death_1 | Безсмертний | Пройти локацію без смертей | 25 |
| boss_slayer | Переможець Босів | Вбити першого боса | 50 |
| all_bosses | Кілер Босів | Вбити всіх 10 босів | 200 |
| perfectionist | Перфекціоніст | 10/10 у квізі без помилок | 30 |
| first_try | З Першої Спроби | Вбити боса з першої спроби | 50 |
| no_hints | Без Підказок | Вбити боса без підказок | 30 |
| streak_3 | 3 Дні Підряд | Стрік 3 дні | 30 |
| streak_7 | Тижневий Герой | Стрік 7 днів | 100 |
| speed_run | Спідранер | Завершити локацію за < 5 хв | 50 |
| completionist | Завершувач | Пройти всі 10 локацій | 300 |
| level_10 | Досвідчений | Досягти 10 рівня | 50 |
| level_20 | Ветеран | Досягти 20 рівня | 100 |

---

# 9. СОЦІАЛЬНІ МЕХАНІКИ

## 9.1 Лідерборд

**Типи:**
- Всі часи (за total_xp)
- Цей тиждень (за xp, набраним з понеділка)
- Друзі (тільки юзери, яких додав)

**Відображення:**
- Топ 100 гравців
- Твоя позиція завжди видна (навіть якщо >100)
- Аватар + юзернейм + рівень + звання + XP

## 9.2 Щоденні квести

Генеруються о 00:00 UTC щодня, 3 квести:

```python
QUEST_TYPES = [
    {
        "type": "answer_questions",
        "description": "Дай правильні відповіді на {target} питань",
        "targets": [5, 10, 15],
        "xp_rewards": [20, 35, 50]
    },
    {
        "type": "complete_quiz",
        "description": "Пройди {target} локацію(й) без смертей",
        "targets": [1, 2],
        "xp_rewards": [30, 60]
    },
    {
        "type": "defeat_boss",
        "description": "Переможи боса",
        "targets": [1],
        "xp_rewards": [50]
    },
    {
        "type": "login_streak",
        "description": "Увійди в гру сьогодні",
        "targets": [1],
        "xp_rewards": [10]
    }
]
```

## 9.3 Стрік (Streak)

- Інкрементується при вході в гру кожного дня
- Якщо пропустив день → стрік = 0
- Нагороди: 3 дні (+30 XP), 7 днів (+100 XP + ачівмент), 30 днів (+500 XP + ачівмент)
- На головному екрані відображається поточний стрік з вогником 🔥

---

# 10. КОНТЕНТ

## 10.1 Повний банк питань — Локація 1: Змінні

*(По 20 питань на локацію, для квізу беруться 10 рандомних)*

```
ПИТАННЯ 1
Текст: Яке значення матиме x після виконання: x = 5; x = x + 3 ?
A) 5
B) 3
C) 8   ← правильна
D) 15
Пояснення: x спочатку дорівнює 5, потім ми додаємо 3, тому x = 8.

ПИТАННЯ 2
Текст: Який тип даних має значення True?
A) str
B) int
C) float
D) bool  ← правильна
Пояснення: True і False — це літерали типу bool (булевий тип).

ПИТАННЯ 3 (з кодом)
Текст: Що виведе цей код?
[код]: x = "5"
       print(type(x))
A) <class 'int'>
B) <class 'float'>
C) <class 'str'>   ← правильна
D) <class 'char'>
Пояснення: Лапки роблять значення рядком (str), навіть якщо всередині число.

ПИТАННЯ 4
Текст: Як правильно оголосити змінну з ім'ям "my variable"?
A) my variable = 10
B) my-variable = 10
C) my_variable = 10   ← правильна
D) myVariable! = 10
Пояснення: В Python імена змінних не можуть містити пробіли або дефіси.
           Конвенція — snake_case (підкреслення замість пробілів).

ПИТАННЯ 5
Текст: Що таке None в Python?
A) 0
B) False
C) Порожній рядок ""
D) Спеціальне значення "нічого"  ← правильна
Пояснення: None — це окремий тип NoneType, що означає відсутність значення.

ПИТАННЯ 6 (з кодом)
Текст: Що виведе print(10 / 3)?
A) 3
B) 3.333...   ← правильна
C) 3.0
D) Error
Пояснення: / завжди повертає float в Python 3. Для цілочисельного ділення
           використовуй //.

ПИТАННЯ 7 (з кодом)
Текст: Що виведе print(10 // 3)?
A) 3.333...
B) 3.0
C) 3   ← правильна
D) 4
Пояснення: // — цілочисельне ділення, повертає тільки цілу частину.

ПИТАННЯ 8
Текст: Яка з цих назв змінних є правильною в Python?
A) 2myvar
B) my-var
C) my var
D) my_var2   ← правильна
Пояснення: Змінна не може починатися з цифри, містити дефіс або пробіл.

ПИТАННЯ 9 (з кодом)
Текст: Що виведе: a, b = 5, 10; print(a, b)?
A) 5 10   ← правильна
B) (5, 10)
C) [5, 10]
D) Error
Пояснення: Python підтримує множинне присвоєння. a = 5, b = 10.

ПИТАННЯ 10 (з кодом)
Текст: Що виведе print(type(3.14))?
A) <class 'int'>
B) <class 'str'>
C) <class 'float'>   ← правильна
D) <class 'double'>
Пояснення: 3.14 — це число з плаваючою комою, тип float.

ПИТАННЯ 11
Текст: Що означає оператор ** в Python?
A) Множення
B) Ділення
C) Степінь   ← правильна
D) Коментар
Пояснення: 2 ** 3 = 8 (2 у степені 3).

ПИТАННЯ 12 (з кодом)
Текст: Що виведе print(7 % 3)?
A) 2.333...
B) 2   ← правильна
C) 1
D) 4
Пояснення: % — оператор остачі від ділення. 7 = 3*2 + 1. Тобто 7 % 3 = 1.
(виправлення: 7 % 3 = 1, правильна відповідь C)

ПИТАННЯ 13
Текст: Як у Python перевірити тип змінної x?
A) x.type()
B) typeof(x)
C) type(x)   ← правильна
D) x::type

ПИТАННЯ 14 (з кодом)
Текст: x = 5; y = "5". Чи рівні вони? (x == y)
A) True
B) False   ← правильна
C) Error
D) None
Пояснення: int 5 і str "5" — різні типи, тому == повертає False.

ПИТАННЯ 15
Текст: Яка з цих операцій поверне тип int?
A) 10 / 2
B) int("10")   ← правильна
C) float(10)
D) str(10)
Пояснення: int("10") конвертує рядок у ціле число.

ПИТАННЯ 16 (з кодом)
Текст: Що виведе: print(bool(0), bool(""), bool(1))?
A) True True True
B) False False True   ← правильна
C) False True False
D) 0 "" 1
Пояснення: 0 і порожній рядок є "falsy" в Python.

ПИТАННЯ 17
Текст: Яке ключове слово не можна використовувати як ім'я змінної?
A) data
B) my_list
C) if   ← правильна
D) number
Пояснення: if — зарезервоване слово Python. Зарезервовані слова не можна
           використовувати як імена змінних.

ПИТАННЯ 18 (з кодом)
Текст: Що виведе: x = 10; x += 5; print(x)?
A) 10
B) 5
C) 15   ← правильна
D) 105

ПИТАННЯ 19
Текст: Чи можна в Python присвоїти різні типи одній змінній?
A) Ні, тип фіксується при оголошенні
B) Так, Python — динамічно типізована мова   ← правильна
C) Тільки якщо використати int()
D) Тільки числові типи

ПИТАННЯ 20 (з кодом)
Текст: Що виведе print(10 == 10.0)?
A) False
B) TypeError
C) True   ← правильна
D) None
Пояснення: Python порівнює значення, а не типи при ==. 10 і 10.0 рівні.
```

## 10.2 Банк питань — Локація 2: Умови

```
ПИТАННЯ 1 (з кодом)
Текст: Що виведе цей код?
x = 10
if x > 5:
    print("Більше")
else:
    print("Менше")
A) Менше
B) Більше   ← правильна
C) Нічого
D) Error

ПИТАННЯ 2 (з кодом)
Текст: Що виведе?
x = 5
if x > 10:
    print("A")
elif x > 3:
    print("B")   ← правильна
else:
    print("C")
A) A
B) B   ← правильна
C) C
D) B і C

ПИТАННЯ 3
Текст: Що означає оператор and?
A) Хоч одна умова True
B) Обидві умови True   ← правильна
C) Жодна умова не True
D) Заперечення

ПИТАННЯ 4 (з кодом)
Текст: Результат: print(5 > 3 and 2 < 4)?
A) False
B) Error
C) 5 > 3
D) True   ← правильна

ПИТАННЯ 5 (з кодом)
Текст: print(5 > 10 or 3 < 7) → ?
A) False
B) True   ← правильна
C) None
D) Error

ПИТАННЯ 6 (з кодом)
Текст: print(not True)?
A) True
B) 1
C) False   ← правильна
D) None

ПИТАННЯ 7
Текст: Скільки гілок elif може бути в одному if-блоці?
A) Тільки 1
B) Максимум 3
C) Необмежено   ← правильна
D) 0

ПИТАННЯ 8 (з кодом)
Текст: Що виведе?
x = 0
if x:
    print("Є")
else:
    print("Нема")   ← правильна
A) Є
B) Нема   ← правильна
C) 0
D) Error
Пояснення: 0 — falsy значення, тому умова if x: → False.

ПИТАННЯ 9 (з кодом)
Текст: Що виведе?
a, b = 3, 5
print("max:", a if a > b else b)
A) max: 3
B) max: 5   ← правильна
C) max: a
D) Error
Пояснення: Тернарний оператор: значення_якщо_true if умова else значення_якщо_false

ПИТАННЯ 10
Текст: Оператор != означає...?
A) Присвоєння
B) Не дорівнює   ← правильна
C) Менше або рівне
D) Приблизно рівне

ПИТАННЯ 11 (з кодом)
Текст: Що виведе?
x = 5
if x == 5: print("П'ять")
A) Нічого
B) П'ять   ← правильна
C) Error (потрібні дужки)
D) if x == 5

ПИТАННЯ 12 (з кодом)
Текст: print(1 < 2 < 3) →?
A) Error
B) False
C) True   ← правильна
D) (True, True)
Пояснення: Python підтримує ланцюгові порівняння.

ПИТАННЯ 13 (з кодом)
Текст: Що виведе?
x = None
if x is None:
    print("None!")   ← правильна
A) Нічого
B) None!   ← правильна
C) Error
D) False

ПИТАННЯ 14
Текст: Різниця між == та is?
A) Немає різниці
B) == порівнює значення, is — об'єкти в пам'яті   ← правильна
C) is порівнює значення, == — об'єкти
D) is тільки для None

ПИТАННЯ 15 (з кодом)
Текст: Що виведе?
if True:
    if False:
        print("A")
    else:
        print("B")   ← правильна
else:
    print("C")
A) A
B) B   ← правильна
C) C
D) B і C

ПИТАННЯ 16
Текст: Як перевірити, чи x належить діапазону 1-10?
A) 1 < x > 10
B) x >= 1 or x <= 10
C) 1 <= x <= 10   ← правильна
D) x in range(1, 10)  (не включає 10)

ПИТАННЯ 17 (з кодом)
Текст: print(bool([])) →?
A) True
B) None
C) Error
D) False   ← правильна
Пояснення: Порожні колекції — falsy.

ПИТАННЯ 18
Текст: Falsy значення в Python (вибери всі правильні):
A) 0, "", [], None   ← правильна (вибираємо одне)
B) 0, "0", False
C) None, 0, True
D) "", 0, [0]

ПИТАННЯ 19 (з кодом)
Текст: Що виведе?
x = "python"
if "py" in x:
    print("Є!")   ← правильна
A) Нічого
B) Є!   ← правильна
C) True
D) Error

ПИТАННЯ 20 (з кодом)
Текст: Результат: print(5 != 5)?
A) True
B) None
C) 5 != 5
D) False   ← правильна
```

## 10.3 Банк питань — Локація 3: Цикли

```
ПИТАННЯ 1 (з кодом)
Текст: Скільки разів виведеться "Hi"?
for i in range(3):
    print("Hi")
A) 0
B) 2
C) 3   ← правильна
D) 4

ПИТАННЯ 2 (з кодом)
Текст: Що виведе?
for i in range(2, 6):
    print(i, end=" ")
A) 2 3 4 5   ← правильна
B) 2 3 4 5 6
C) 1 2 3 4 5
D) 0 1 2 3

ПИТАННЯ 3 (з кодом)
Текст: Що виведе?
i = 0
while i < 3:
    print(i)
    i += 1
A) 0 1 2   ← правильна
B) 1 2 3
C) 0 1 2 3
D) Нескінченний цикл

ПИТАННЯ 4
Текст: Що робить оператор break?
A) Пропускає поточну ітерацію
B) Виходить з циклу повністю   ← правильна
C) Перезапускає цикл
D) Зупиняє програму

ПИТАННЯ 5
Текст: Що робить оператор continue?
A) Виходить з циклу
B) Перезапускає цикл з початку
C) Пропускає решту коду в поточній ітерації, переходить до наступної   ← правильна
D) Нічого

ПИТАННЯ 6 (з кодом)
Текст: Що виведе?
for i in range(5):
    if i == 3:
        break
    print(i)
A) 0 1 2 3
B) 0 1 2   ← правильна
C) 0 1 2 3 4
D) 3

ПИТАННЯ 7 (з кодом)
Текст: Що виведе?
for i in range(5):
    if i == 3:
        continue
    print(i)
A) 0 1 2 3 4
B) 0 1 2 4   ← правильна
C) 0 1 2
D) 3

ПИТАННЯ 8 (з кодом)
Текст: range(0, 10, 2) — що це?
A) 0 1 2 3 4 5 6 7 8 9 10
B) 0 2 4 6 8   ← правильна
C) 2 4 6 8 10
D) 0 2 4 6 8 10

ПИТАННЯ 9 (з кодом)
Текст: Що виведе?
for i in range(3):
    for j in range(2):
        print(i, j)
A) 0 0, 1 1, 2 2
B) 0 0, 0 1, 1 0, 1 1, 2 0, 2 1   ← правильна
C) 6 разів "0 0"
D) Error

ПИТАННЯ 10
Текст: Що таке else в циклі for?
A) Помилка синтаксису
B) Виконується після циклу, якщо break не спрацював   ← правильна
C) Виконується при кожній ітерації
D) Виконується тільки якщо break спрацював

ПИТАННЯ 11 (з кодом)
Текст: Що виведе?
s = 0
for i in range(1, 5):
    s += i
print(s)
A) 10   ← правильна (1+2+3+4)
B) 15
C) 6
D) 4

ПИТАННЯ 12 (з кодом)
Текст: for letter in "abc": print(letter) — виведе?
A) abc
B) a b c (в один рядок)
C) a, b, c кожне на новому рядку   ← правильна
D) Error, рядки не ітеруються

ПИТАННЯ 13
Текст: Коли використовувати while замість for?
A) Завжди, while краще
B) Коли кількість ітерацій заздалегідь невідома   ← правильна
C) Тільки для чисел
D) Ніколи, for завжди краще

ПИТАННЯ 14 (з кодом)
Текст: Що не так з цим кодом?
while True:
    print("hi")
A) Синтаксична помилка
B) True не можна у while
C) Нескінченний цикл (немає break/зміни умови)   ← правильна
D) Нічого, код правильний

ПИТАННЯ 15 (з кодом)
Текст: enumerate([10,20,30]) дає?
A) (10, 20, 30)
B) [(0,10), (1,20), (2,30)]   ← правильна
C) [0, 1, 2]
D) [(1,10), (2,20), (3,30)]

ПИТАННЯ 16 (з кодом)
Текст: Що виведе?
for i in range(3):
    pass
print("Done")
A) Нічого
B) Done   ← правильна
C) 0 1 2 Done
D) Error

ПИТАННЯ 17 (з кодом)
Текст: Що виведе?
i = 10
while i > 0:
    i -= 3
print(i)
A) 0
B) 1
C) -2   ← правильна (10→7→4→1→-2)
D) 3

ПИТАННЯ 18
Текст: range(5) → скільки елементів?
A) 4
B) 5   ← правильна
C) 6
D) Залежить від системи

ПИТАННЯ 19 (з кодом)
Текст: Що виведе?
total = 0
for _ in range(5):
    total += 1
print(total)
A) 0
B) 4
C) 5   ← правильна
D) _
Пояснення: _ — конвенція для "не важлива змінна".

ПИТАННЯ 20 (з кодом)
Текст: zip([1,2], ["a","b"]) дає?
A) [1, 2, "a", "b"]
B) [(1,"a"), (2,"b")]   ← правильна
C) {1:"a", 2:"b"}
D) Error
```

## 10.4 Задачі для босів — повний список

### Бос 1: Змінний Хаос (Змінні)
```
Назва: Транспозиція Хаосу
Сюжет: Змінний Хаос заплутав всі значення у Рівнині Початку! 
       Щоб перемогти його, ти маєш довести, що розумієш, 
       як обмінювати місцями змінні.

Задача: Напиши функцію swap_values(a, b), яка приймає два числа 
        і повертає їх у зміненому порядку у вигляді tuple.

Підпис: def swap_values(a, b):

Стартовий код:
def swap_values(a, b):
    # Твій код тут
    pass

Тести:
  swap_values(3, 7) → (7, 3)
  swap_values(0, 5) → (5, 0)
  swap_values(-1, 1) → (1, -1)
  [прихований] swap_values(100, 200) → (200, 100)
  [прихований] swap_values(42, 42) → (42, 42)

Підказки:
  1. Функція має повернути два значення у зміненому порядку
  2. У Python функція може повертати кілька значень через кому: return b, a
  3. return b, a — і Python автоматично зробить з цього tuple (b, a)
```

### Бос 2: Вилка Долі (Умови)
```
Задача: Напиши функцію classify_number(n), яка повертає:
        "positive" якщо n > 0
        "negative" якщо n < 0
        "zero" якщо n == 0

Тести:
  classify_number(5) → "positive"
  classify_number(-3) → "negative"
  classify_number(0) → "zero"
  [прихований] classify_number(1000000) → "positive"
  [прихований] classify_number(-0.5) → "negative"
```

### Бос 3: Нескінченний Голем (Цикли)
```
Задача: Напиши функцію sum_digits(n), яка приймає невід'ємне ціле 
        число і повертає суму його цифр.

Тести:
  sum_digits(123) → 6
  sum_digits(0) → 0
  sum_digits(999) → 27
  [прихований] sum_digits(1000) → 1
  [прихований] sum_digits(12345) → 15
```

### Бос 4: Рекурсивний Дракон (Функції)
```
Задача: Напиши функцію is_palindrome(s), яка перевіряє, 
        чи є рядок паліндромом (однаково читається зліва і справа).
        Регістр не враховується.

Тести:
  is_palindrome("racecar") → True
  is_palindrome("hello") → False
  is_palindrome("A") → True
  [прихований] is_palindrome("Madam") → True
  [прихований] is_palindrome("") → True
```

### Бос 5: Список-Пожирач (Списки)
```
Задача: Напиши функцію find_max(lst), яка повертає найбільший 
        елемент списку БЕЗ використання вбудованої функції max().

Тести:
  find_max([3, 1, 4, 1, 5]) → 5
  find_max([10, 20, 30]) → 30
  find_max([-1, -5, -3]) → -1
  [прихований] find_max([42]) → 42
  [прихований] find_max([0, 0, 0]) → 0
```

### Бос 6: Ключ-Майстер (Словники)
```
Задача: Напиши функцію count_words(text), яка приймає рядок 
        і повертає словник де ключі — слова, значення — кількість 
        їх повторень.

Тести:
  count_words("hello world hello") → {"hello": 2, "world": 1}
  count_words("a a a") → {"a": 3}
  count_words("one") → {"one": 1}
  [прихований] count_words("") → {}
  [прихований] count_words("hi hi ho ho") → {"hi": 2, "ho": 2}
```

### Бос 7: Форматований Ліч (Рядки)
```
Задача: Напиши функцію format_name(first, last), яка повертає 
        рядок у форматі "Last, First" де обидва імені починаються 
        з великої літери.

Тести:
  format_name("john", "doe") → "Doe, John"
  format_name("ALICE", "SMITH") → "Smith, Alice"
  format_name("Bob", "brown") → "Brown, Bob"
  [прихований] format_name("anna", "KOWALSKI") → "Kowalski, Anna"
  [прихований] format_name("X", "Y") → "Y, X"
```

### Бос 8: Баг-Лорд (Помилки)
```
Задача: Напиши функцію safe_divide(a, b), яка ділить a на b. 
        Якщо b == 0, повертає None замість виключення.

Тести:
  safe_divide(10, 2) → 5.0
  safe_divide(10, 0) → None
  safe_divide(7, 2) → 3.5
  [прихований] safe_divide(0, 5) → 0.0
  [прихований] safe_divide(-10, 2) → -5.0
```

### Бос 9: Об'єктний Колос (ООП)
```
Задача: Створи клас Rectangle зі:
        - __init__(self, width, height)
        - метод area(self) → повертає площу
        - метод perimeter(self) → повертає периметр

Тести (через окремі виклики):
  r = Rectangle(4, 5); r.area() → 20
  r = Rectangle(4, 5); r.perimeter() → 18
  r = Rectangle(1, 1); r.area() → 1
  [прихований] r = Rectangle(10, 0); r.area() → 0
  [прихований] r = Rectangle(3, 3); r.perimeter() → 12
```

### Бос 10: Темний Компілятор (Модулі)
```
Задача: Напиши функцію days_until(date_str), яка приймає 
        дату у форматі "YYYY-MM-DD" і повертає кількість 
        днів від сьогодні до тієї дати (може бути від'ємним).

Підказка: використай модуль datetime.

Тести (відносні, тест запускається з фіксованою "сьогоднішньою" датою 2026-01-01):
  days_until("2026-01-11") → 10
  days_until("2025-12-31") → -1
  days_until("2026-01-01") → 0
  [прихований] days_until("2026-01-31") → 30
  [прихований] days_until("2025-01-01") → -365
```

---

# 11. API

## 11.1 Авторизація

```
POST   /api/auth/register
       Body: {username, email, password, avatar_id}
       Response: {user, access_token}

POST   /api/auth/login
       Body: {email, password}
       Response: {user, access_token}

POST   /api/auth/logout
       Response: {message: "ok"}

POST   /api/auth/refresh
       Response: {access_token}

GET    /api/auth/me
       Response: {user + stats}
```

## 11.2 Локації

```
GET    /api/locations
       Response: [{location + user_progress}]

GET    /api/locations/:slug
       Response: {location + questions_count + user_progress}

POST   /api/locations/:slug/enter
       Response: {location_data, hero_hp, existing_session?}
```

## 11.3 Квіз

```
POST   /api/quiz/start
       Body: {location_slug}
       Response: {session_id, question, hero_hp, question_number: 1}

POST   /api/quiz/answer
       Body: {session_id, question_id, selected_option}
       Response: {is_correct, correct_option, explanation, 
                  hero_hp, xp_gained, questions_left, 
                  next_question?, is_quiz_done, hero_died}

GET    /api/quiz/session/:session_id
       Response: {current state of quiz session}

POST   /api/quiz/abandon
       Body: {session_id}
       Response: {message: "ok"}
```

## 11.4 Бос

```
GET    /api/boss/:location_slug
       Response: {challenge, boss_session_id, hero_hp, boss_hp}

POST   /api/boss/submit
       Body: {session_id, code}
       Response: {
           test_results: [{input, expected, actual, passed, is_hidden}],
           boss_hp_remaining,
           hero_hp_remaining,
           boss_defeated,
           hero_died,
           xp_gained,
           bonuses: [...]
       }

POST   /api/boss/hint
       Body: {session_id, hint_number}
       Response: {hint_text, hero_hp_after, hints_remaining}

GET    /api/boss/session/:session_id
       Response: {full session state}
```

## 11.5 Профіль

```
GET    /api/profile/:username
       Response: {user, stats, completed_locations, achievements}

GET    /api/profile/:username/achievements
       Response: [{achievement + unlocked_at}]

PATCH  /api/profile/avatar
       Body: {avatar_id}
       Response: {user}
```

## 11.6 Лідерборд та квести

```
GET    /api/leaderboard?type=all_time|weekly|friends&page=1
       Response: {rankings: [...], my_position, total}

GET    /api/daily-quests
       Response: {quests: [...], streak_days}

POST   /api/daily-quests/update
       Body: {quest_type, increment}
       (викликається автоматично з інших ендпоінтів)
```

## 11.7 HTTP коди відповідей

```
200 OK             — успіх
201 Created        — створено
400 Bad Request    — невалідні дані
401 Unauthorized   — немає або невалідний токен
403 Forbidden      — немає прав
404 Not Found      — ресурс не знайдено
409 Conflict       — email/username вже існує
422 Unprocessable  — валідація Pydantic
429 Too Many       — rate limiting
500 Server Error   — помилка сервера
```

---

# 12. ФРОНТЕНД

## 12.1 Роутінг (React Router v6)

```
/                       → redirect to /map (якщо авторизований) або /login
/login                  → LoginPage
/register               → RegisterPage
/map                    → WorldMapPage          (protected)
/location/:slug         → LocationLobbyPage     (protected)
/location/:slug/quiz    → QuizBattlePage        (protected)
/location/:slug/boss    → BossFightPage         (protected)
/profile/:username      → ProfilePage           (protected)
/leaderboard            → LeaderboardPage       (protected)
/achievements           → AchievementsPage      (protected)
```

## 12.2 Компоненти

### UI Базові
```
components/ui/
  PixelButton.tsx       — кнопка у піксельному стилі (варіанти: primary, danger, ghost)
  PixelCard.tsx         — картка з піксельним бордером
  HPBar.tsx             — HP-бар з анімацією (fill + shake при ударі)
  XPBar.tsx             — XP прогрес-бар
  PixelBadge.tsx        — бейджик (рівень, звання)
  Modal.tsx             — модальне вікно (game-over, level-up, achievement)
  Tooltip.tsx           — підказка при ховері
  LoadingScreen.tsx     — екран завантаження з піксель-анімацією
  NotificationToast.tsx — сповіщення (XP gained, achievement unlocked)
```

### Ігрові компоненти
```
components/game/
  SpriteAnimation.tsx   — рендер піксель-арт спрайту через Pixi.js
  HeroSprite.tsx        — герой з анімаціями (idle/attack/hit/die)
  EnemySprite.tsx       — крип з анімаціями
  BossSprite.tsx        — бос (великий) з анімаціями
  BattleArena.tsx       — арена бою (фон + позиції героя та ворога)
  QuizQuestion.tsx      — картка питання з варіантами відповіді
  AnswerOption.tsx      — кнопка варіанту відповіді (neutral/correct/wrong)
  ExplanationCard.tsx   — блок пояснення після неправильної відповіді
  CodeEditor.tsx        — Monaco Editor з Python налаштуваннями
  TestResultRow.tsx     — рядок результату тесту (passed/failed)
  HintButton.tsx        — кнопка підказки (з залишком та ціною HP)
  DamageNumber.tsx      — спливаючий числовий індикатор ("-1 HP", "+10 XP")
  BossHealthBar.tsx     — HP-бар боса з анімацією
```

### Лейаут
```
components/layout/
  GameLayout.tsx        — обгортка для ігрових екранів
  Navbar.tsx            — навігаційна панель (аватар, XP, рівень, меню)
  Sidebar.tsx           — бічна панель (карта прогресу, квести)
```

## 12.3 State Management (Zustand)

```typescript
// store/authStore.ts
interface AuthStore {
  user: User | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  updateUser: (data: Partial<User>) => void
}

// store/gameStore.ts
interface GameStore {
  currentLocation: Location | null
  quizSession: QuizSession | null
  bossSession: BossSession | null
  
  startQuiz: (locationSlug: string) => Promise<void>
  submitAnswer: (questionId: number, option: string) => Promise<AnswerResult>
  startBoss: (locationSlug: string) => Promise<void>
  submitCode: (code: string) => Promise<SubmissionResult>
  requestHint: (hintNumber: number) => Promise<HintResult>
}

// store/uiStore.ts
interface UIStore {
  activeModal: ModalType | null
  notifications: Notification[]
  showModal: (type: ModalType, data?: any) => void
  hideModal: () => void
  addNotification: (notif: Notification) => void
}
```

## 12.4 Сервісний шар (API calls)

```typescript
// services/api.ts
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,  // для httpOnly cookies
})

// Автоматичний refresh при 401
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      await refreshToken()
      return api.request(error.config)
    }
    throw error
  }
)

// services/quiz.service.ts
export const startQuiz = (locationSlug: string) =>
  api.post('/quiz/start', { location_slug: locationSlug })

export const submitAnswer = (sessionId: string, questionId: number, option: string) =>
  api.post('/quiz/answer', { session_id: sessionId, question_id: questionId, selected_option: option })
```

## 12.5 Ключові екрани — деталі

### WorldMapPage
- SVG карта з 10 локаціями (позиції фіксовані, з'єднані пунктирними стежками)
- Кожна локація — кліковний SVG елемент зі своєю іконкою та статусом
- Анімація пульсації для доступних локацій (CSS keyframes)
- При кліку на completed → popup з статистикою
- Верхня панель: аватар, рівень, XP-бар, стрік

### QuizBattlePage
- Split layout: ліво — арена (герой + крип), право — питання
- Після вибору відповіді — блокування кнопок на час анімації
- Анімаційний таймінг:
  ```
  Правильна: 300ms підсвічення → 1500ms attack anim → 500ms die anim → 400ms fade in next question
  Неправильна: 300ms підсвічення → 800ms enemy attack → 500ms player hit → 600ms show explanation
  ```

### BossFightPage
- Split layout: ліво — арена (бос + HP бар), право — редактор + задача
- Monaco Editor: тема "vs-dark", python підсвічування, автодоповнення
- Run Tests → спінер → результати по кожному тесту (зелений ✓ / червоний ✗)
- Прихований тест показується як "🔒 Прихований тест: [passed/failed]"
- При перемозі над босом → fullscreen overlay з анімацією

---

# 13. ГРАФІКА ТА ДИЗАЙН

## 13.1 Дизайн-система

```css
/* Кольори */
--color-bg:          #0a0a0f;  /* майже чорний */
--color-bg-card:     #13131a;  /* картки */
--color-bg-elevated: #1c1c26;  /* підняті елементи */
--color-border:      #2a2a3a;  /* бордери */

--color-primary:     #7c5cbf;  /* фіолетовий (основний) */
--color-primary-hover: #9b7fe0;
--color-danger:      #e05252;  /* червоний (HP, помилки) */
--color-success:     #52c97a;  /* зелений (правильно, XP) */
--color-warning:     #e0c052;  /* жовтий (підказки) */
--color-info:        #5288e0;  /* синій */

--color-text:        #e8e8f0;  /* основний текст */
--color-text-muted:  #8888aa;  /* другорядний */
--color-text-dim:    #555570;  /* дімований */

/* Шрифти */
--font-pixel: 'Press Start 2P', monospace;  /* заголовки, UI */
--font-mono:  'JetBrains Mono', monospace;  /* код */
--font-body:  'Inter', sans-serif;           /* основний текст */

/* Розміри піксель-арт елементів */
--sprite-size-sm: 32px;   /* крипи */
--sprite-size-md: 64px;   /* герой */
--sprite-size-lg: 128px;  /* бос */
```

## 13.2 Список спрайтів для генерації

**Промпт-шаблон (Midjourney/DALL-E 3):**
```
pixel art, 32x32 pixels, RPG game sprite, [ОБ'ЄКТ], 
dark fantasy style, vibrant neon colors, black background, 
transparent background, crisp pixels, no anti-aliasing, 
game asset style
```

**Що генерувати:**

| Категорія | Спрайти | К-сть |
|---|---|---|
| Герої (idle) | Маг, Воїн, Лучниця, Хакер | 4 |
| Герої (attack) | Те ж саме + анімація атаки | 4 |
| Крипи (idle) | 6 видів (по 1-2 на локацію) | 6 |
| Крипи (attack) | Те ж + анімація атаки | 6 |
| Боси (idle, 128x128) | 10 унікальних | 10 |
| Боси (attack) | 10 унікальних | 10 |
| Фони арени | 10 (per локація) | 10 |
| Карта світу | 1 загальна карта | 1 |
| Іконки локацій | 10 іконок для карти | 10 |
| UI елементи | Рамки, кнопки, HP-бар | ~15 |
| Аватари персонажів | 4 класи | 4 |
| Іконки ачівментів | ~13 штук | 13 |
| **Разом** | | **~93** |

## 13.3 Анімації (CSS/Pixi.js)

```typescript
// Всі анімації героя/ворогів через Pixi.js Spritesheet

// CSS анімації для UI:
@keyframes pulse-available {
  0%, 100% { filter: brightness(1) drop-shadow(0 0 4px var(--color-primary)); }
  50%       { filter: brightness(1.3) drop-shadow(0 0 12px var(--color-primary)); }
}

@keyframes float-up {
  0%   { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-60px); }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25%       { transform: translateX(-8px); }
  75%       { transform: translateX(8px); }
}

@keyframes level-up {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.5); filter: brightness(2); }
  100% { transform: scale(1); }
}
```

## 13.4 Звуки (опціональні)

- `correct_answer.mp3` — позитивний звук (хрум/дзвін)
- `wrong_answer.mp3` — негативний (бум/хрипіння)
- `boss_defeated.mp3` — переможний fanfare
- `level_up.mp3` — мелодія level up
- `hero_attack.mp3` — звук удару
- `boss_attack.mp3` — звук удару боса
- `bg_quiz.mp3` — фонова музика для квізу (looped)
- `bg_boss.mp3` — фонова музика для бос-файту (looped)

Генерати через: ElevenLabs Sound Effects або Suno

---

# 14. ПЕРЕВІРКА КОДУ

## 14.1 Judge0 API інтеграція

```python
# backend/services/judge0_service.py
import httpx
from typing import Optional

JUDGE0_URL = "https://judge0-ce.p.rapidapi.com"
LANGUAGE_ID_PYTHON = 71  # Python 3.8.1

class Judge0Service:
    
    async def run_code(
        self, 
        source_code: str,
        time_limit: int = 5,
        memory_limit: int = 131072  # 128MB в KB
    ) -> dict:
        
        payload = {
            "source_code": source_code,
            "language_id": LANGUAGE_ID_PYTHON,
            "time_limit": time_limit,
            "memory_limit": memory_limit,
            "wall_time_limit": time_limit + 2,
        }
        
        # Submit
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{JUDGE0_URL}/submissions?base64_encoded=false&wait=true",
                json=payload,
                headers={
                    "X-RapidAPI-Key": settings.JUDGE0_API_KEY,
                    "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
                },
                timeout=30.0
            )
        
        result = response.json()
        
        return {
            "stdout": result.get("stdout", "").strip(),
            "stderr": result.get("stderr", ""),
            "status": result.get("status", {}).get("description"),
            "time": result.get("time"),
            "memory": result.get("memory"),
            "exit_code": result.get("exit_code"),
        }
    
    async def run_test_case(
        self,
        user_code: str,
        function_call: str,
        expected_output: str,
        time_limit: int,
        memory_limit: int
    ) -> dict:
        
        # Обгортаємо код гравця тестовим викликом
        full_code = f"""{user_code}

# === Test Runner ===
try:
    result = {function_call}
    print(result)
except Exception as e:
    print(f"ERROR: {{type(e).__name__}}: {{e}}")
"""
        
        result = await self.run_code(full_code, time_limit, memory_limit)
        
        actual = result["stdout"].strip()
        
        return {
            "actual_output": actual,
            "expected_output": expected_output.strip(),
            "passed": actual == expected_output.strip(),
            "error": result["stderr"] or (actual if actual.startswith("ERROR:") else None),
            "status": result["status"],
            "time_ms": result["time"],
        }
```

## 14.2 Захист від шкідливого коду

```python
# backend/services/code_sanitizer.py

FORBIDDEN_IMPORTS = [
    "os", "sys", "subprocess", "socket", "requests", "http",
    "urllib", "shutil", "pathlib", "glob", "tempfile",
    "multiprocessing", "threading", "ctypes", "importlib",
    "__builtins__", "eval", "exec", "compile", "open"
]

FORBIDDEN_PATTERNS = [
    r"__import__",
    r"getattr\s*\(",
    r"setattr\s*\(",
    r"globals\s*\(",
    r"locals\s*\(",
    r"vars\s*\(",
    r"dir\s*\(",
]

def sanitize_code(code: str) -> tuple[bool, str]:
    """
    Повертає (is_safe, reason)
    УВАГА: це перша лінія захисту.
    Основний захист — Judge0 sandbox.
    """
    import re
    
    for forbidden in FORBIDDEN_IMPORTS:
        pattern = rf'\bimport\s+{forbidden}\b|\bfrom\s+{forbidden}\b'
        if re.search(pattern, code):
            return False, f"Заборонений імпорт: {forbidden}"
    
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, code):
            return False, "Заборонена операція"
    
    if len(code) > 10000:
        return False, "Код занадто довгий (максимум 10000 символів)"
    
    return True, ""
```

## 14.3 Порівняння виводу

```python
def compare_output(actual: str, expected: str) -> bool:
    """
    Порівнює вивід з очікуваним результатом.
    Нормалізує пробіли та регістр де потрібно.
    """
    actual = actual.strip()
    expected = expected.strip()
    
    # Точне порівняння
    if actual == expected:
        return True
    
    # Числа: порівняти як float (5.0 == 5)
    try:
        if float(actual) == float(expected):
            return True
    except (ValueError, TypeError):
        pass
    
    # Tuple/list нормалізація: (7, 3) vs (7, 3) з різними пробілами
    actual_normalized = actual.replace(" ", "")
    expected_normalized = expected.replace(" ", "")
    if actual_normalized == expected_normalized:
        return True
    
    return False
```

---

# 15. AI-ІНТЕГРАЦІЯ

## 15.1 Claude API для підказок у бос-файті

```python
# backend/services/claude_service.py
import anthropic

client = anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY)

async def get_hint(
    challenge: BossChallenge,
    user_code: str,
    hint_number: int  # 1, 2, або 3
) -> str:
    
    hint_instructions = {
        1: "Дай загальний натяк у напрямку рішення. НЕ давай конкретний код.",
        2: "Дай конкретну пораду про алгоритм. Можна згадати один метод Python.",
        3: "Дай майже-відповідь: покажи структуру коду без заповнення деталей."
    }
    
    prompt = f"""Ти помічник у навчальній грі PyQuest для початківців Python.

Задача гравця:
{challenge.task_text}

Поточний код гравця:
```python
{user_code if user_code.strip() else "# (порожньо)"}
```

Дай підказку #{hint_number}.
{hint_instructions[hint_number]}

Вимоги:
- Мова: українська
- Довжина: 1-3 речення максимум
- НЕ давай повне рішення
- Будь підбадьорливим та дружнім
- Не кажи "Підказка:" на початку
"""
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text
```

## 15.2 Генерація пояснень для питань

```python
async def generate_explanation(
    question: Question,
    selected_option: str
) -> str:
    """
    Для питань без пояснення — генеруємо через Claude.
    Зберігаємо в БД щоб не генерувати повторно.
    """
    
    prompt = f"""Поясни, чому відповідь на це питання Python правильна/неправильна.

Питання: {question.question_text}
Правильна відповідь: {question.correct_option}) {getattr(question, f'option_{question.correct_option}')}
Вибрана відповідь: {selected_option}) {getattr(question, f'option_{selected_option}')}

Поясни в 2-3 реченнях, чому правильна відповідь є правильною.
Мова: українська. Тон: дружній, для початківця.
"""
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text
```

## 15.3 Rate Limiting для AI

```python
# Щоб не перевитрачати API бюджет:
AI_RATE_LIMITS = {
    "hints_per_boss": 3,        # максимум 3 підказки на бос-сесію
    "hints_per_day": 20,        # максимум 20 підказок на день (глобально)
    "explanations_cached": True  # пояснення кешуються в БД назавжди
}
```

---

# 16. БЕЗПЕКА

## 16.1 Аутентифікація

```python
# JWT налаштування
ACCESS_TOKEN_EXPIRE = 24 * 60  # 24 години (хвилини)
REFRESH_TOKEN_EXPIRE = 30      # 30 днів

# bcrypt
BCRYPT_ROUNDS = 12

# httpOnly cookie для refresh token (захист від XSS)
# Authorization header для access token
```

## 16.2 Rate Limiting

```python
# backend/core/rate_limit.py
# Використовуємо slowapi (FastAPI обгортка для limits)

RATE_LIMITS = {
    "auth:register":     "5/hour",
    "auth:login":        "10/minute",
    "quiz:answer":       "60/minute",    # 1 відповідь/секунду макс
    "boss:submit":       "10/minute",    # не більше 10 сабмітів/хв
    "boss:hint":         "5/minute",
    "api:global":        "300/minute",   # загальний ліміт
}
```

## 16.3 Валідація

```python
# Pydantic схеми для всіх запитів
class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern=r'^[a-zA-Z0-9_]+$')
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    avatar_id: int = Field(ge=1, le=4)

class AnswerRequest(BaseModel):
    session_id: UUID
    question_id: int = Field(gt=0)
    selected_option: str = Field(pattern=r'^[abcd]$')

class CodeSubmissionRequest(BaseModel):
    session_id: UUID
    code: str = Field(min_length=1, max_length=10000)
```

## 16.4 CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # тільки наш фронт
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## 16.5 SQL Injection захист

- Використовуємо SQLAlchemy ORM — параметризовані запити автоматично
- Ніяких raw SQL рядків з user input

---

# 17. ПОЕТАПНИЙ ПЛАН РОЗРОБКИ

## Фаза 0: Підготовка (1-2 дні)

- [ ] Створити репозиторій (GitHub, monorepo)
- [ ] Налаштувати docker-compose (postgres, redis)
- [ ] Ініціалізувати FastAPI проект + базова структура
- [ ] Ініціалізувати React + Vite + TypeScript + Tailwind
- [ ] Налаштувати ESLint, Prettier, pre-commit hooks
- [ ] Отримати API ключі: Judge0, Claude API
- [ ] Зареєструватися на Railway/Render для деплою

## Фаза 1: Авторизація (2-3 дні)

**Бекенд:**
- [ ] Модель User (SQLAlchemy)
- [ ] Alembic міграції
- [ ] `POST /auth/register` + `POST /auth/login`
- [ ] JWT генерація та валідація
- [ ] `GET /auth/me`

**Фронтенд:**
- [ ] Сторінки Login і Register
- [ ] Форми з валідацією (React Hook Form + Zod)
- [ ] Вибір аватара (4 персонажі)
- [ ] Zustand authStore
- [ ] Protected routes
- [ ] Автоматичний refresh token

**Тест:** Можна зареєструватися, залогінитися, побачити profil

## Фаза 2: БД та Контент (2-3 дні)

**Бекенд:**
- [ ] Всі міграції (locations, questions, boss_challenges, progress)
- [ ] Seed script: заповнити всі 10 локацій
- [ ] Seed script: заповнити питання (20 на локацію = 200 питань)
- [ ] Seed script: заповнити boss_challenges (10 задач)
- [ ] `GET /locations` API

**Фронтенд:**
- [ ] WorldMapPage: статична карта з іконками локацій
- [ ] Логіка locked/available/completed відображення

**Тест:** Карта відображається, локації заблоковані/доступні правильно

## Фаза 3: Quiz System (3-4 дні)

**Бекенд:**
- [ ] Модель QuizSession
- [ ] `POST /quiz/start` — створення сесії
- [ ] `POST /quiz/answer` — перевірка відповіді, логіка HP
- [ ] Redis для кешування сесії
- [ ] Логіка death → restart
- [ ] XP нарахування
- [ ] Оновлення user_location_progress після завершення

**Фронтенд:**
- [ ] LocationLobbyPage
- [ ] QuizBattlePage — базовий лейаут
- [ ] Компоненти: HPBar, QuizQuestion, AnswerOption
- [ ] Стани кнопок: neutral → correct/wrong → blocked during animation
- [ ] ExplanationCard після неправильної відповіді
- [ ] Перехід на Boss Fight після 10 питань
- [ ] Game Over екран при смерті

**Спрайти (тимчасово):** Прості CSS-прямокутники замість спрайтів

**Тест:** Повний квіз від початку до кінця, смерть і рестарт

## Фаза 4: Boss Fight (4-5 днів)

**Бекенд:**
- [ ] Модель BossSession
- [ ] `GET /boss/:slug` — отримати задачу боса
- [ ] `POST /boss/submit` — прийняти код, запустити тести
- [ ] Judge0Service інтеграція
- [ ] CodeSanitizer
- [ ] Логіка HP боса (кожен тест = -20 HP)
- [ ] `POST /boss/hint`
- [ ] XP нарахування за боса + бонуси
- [ ] Розблокування наступної локації

**Фронтенд:**
- [ ] BossFightPage — лейаут
- [ ] Monaco Editor інтеграція (pip: @monaco-editor/react)
- [ ] Кнопка "Атакувати" → лоадер → результати
- [ ] TestResultRow компоненти
- [ ] HintButton (3 підказки, ціна HP)
- [ ] Victory екран з XP анімацією
- [ ] Defeat екран

**Тест:** Повний бос-файт, перемога, розблокування наступної локації

## Фаза 5: Прогресія та Профіль (2-3 дні)

**Бекенд:**
- [ ] XP service: level up логіка
- [ ] Achievements service: перевірка умов після кожної дії
- [ ] Seed: всі ачівменти в БД
- [ ] `GET /profile/:username`
- [ ] `GET /leaderboard`
- [ ] Щоденні квести генерація (cron job)

**Фронтенд:**
- [ ] ProfilePage
- [ ] LeaderboardPage
- [ ] AchievementsPage
- [ ] Level Up модал (з анімацією)
- [ ] Achievement Unlocked toast
- [ ] Оновлення Navbar (XP-бар + рівень в реальному часі)

## Фаза 6: Графіка та Анімації (3-5 днів)

- [ ] Генерація всіх спрайтів через AI (по шаблону)
- [ ] Pixi.js інтеграція для спрайтів
- [ ] Spritesheet для героїв (idle/attack/hit/die)
- [ ] Spritesheet для крипів
- [ ] Spritesheet для босів
- [ ] CSS анімації для UI (float-up XP, pulse для карти)
- [ ] Фонові зображення для арен
- [ ] Карта світу (повноцінна SVG/PNG версія)
- [ ] Звуки (опціонально)

## Фаза 7: Claude AI підказки (1-2 дні)

- [ ] Claude API інтеграція
- [ ] `POST /boss/hint` → Claude генерує підказку
- [ ] Rate limiting для підказок
- [ ] Кешування підказок (зберігати в БД якщо задача повторюється)
- [ ] Фронт: показ підказки в модалі

## Фаза 8: QA та Полірування (3-4 дні)

- [ ] Ручне тестування всіх 10 локацій
- [ ] Перевірка всіх test cases для кожного боса
- [ ] Перевірка edge cases (смерть при бос-файті, disconnect, etc.)
- [ ] UX polish: loading states, error states, empty states
- [ ] Responsive (планшет мінімум)
- [ ] Performance: lazy loading зображень, code splitting

## Фаза 9: Деплой (1-2 дні)

- [ ] Production env variables
- [ ] Docker images для бека
- [ ] Деплой бекенду на Railway
- [ ] Деплой фронту на Vercel
- [ ] Налаштування PostgreSQL на Railway
- [ ] Налаштування Redis на Railway
- [ ] Домен + HTTPS
- [ ] Фінальне тестування на production

**Загальний час MVP: ~25-35 днів** (з AI-допомогою значно менше)

---

# 18. ДЕПЛОЙ

## 18.1 Оточення

```bash
# backend/.env
DATABASE_URL=postgresql://user:pass@host:5432/pyquest
REDIS_URL=redis://host:6379
SECRET_KEY=<random-256-bit-key>
ALGORITHM=HS256
JUDGE0_API_KEY=<key>
CLAUDE_API_KEY=<key>
FRONTEND_URL=https://pyquest.vercel.app

# frontend/.env
VITE_API_URL=https://api.pyquest.railway.app
```

## 18.2 Docker Compose (розробка)

```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: pyquest
      POSTGRES_USER: pyquest
      POSTGRES_PASSWORD: devpassword
    ports: ["5432:5432"]
    volumes: [postgres_data:/var/lib/postgresql/data]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: postgresql://pyquest:devpassword@db:5432/pyquest
      REDIS_URL: redis://redis:6379
    depends_on: [db, redis]
    volumes: [./backend:/app]
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

  frontend:
    build: ./frontend
    ports: ["5173:5173"]
    volumes: [./frontend:/app]
    command: npm run dev -- --host

volumes:
  postgres_data:
```

## 18.3 Production деплой

**Бекенд → Railway:**
- Підключити GitHub repo
- Вибрати папку `/backend`
- Dockerfile автоматично
- Додати PostgreSQL plugin
- Додати Redis plugin
- Встановити ENV змінні

**Фронтенд → Vercel:**
- Підключити GitHub repo
- Root directory: `frontend`
- Build command: `npm run build`
- Output: `dist`
- Встановити `VITE_API_URL`

---

# 19. ТЕСТУВАННЯ

## 19.1 Бекенд тести (pytest)

```python
# tests/test_auth.py
def test_register_success(client):
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "password123",
        "avatar_id": 1
    })
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_register_duplicate_email(client):
    # Створити юзера
    # Спробувати ще раз з тим же email
    assert response.status_code == 409

# tests/test_quiz.py
def test_start_quiz(authenticated_client, seeded_db):
    response = authenticated_client.post("/api/quiz/start", 
        json={"location_slug": "variables"})
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "question" in data
    assert data["hero_hp"] == 5

def test_correct_answer(authenticated_client, active_session):
    response = authenticated_client.post("/api/quiz/answer", json={
        "session_id": str(active_session.id),
        "question_id": active_session.current_question_id,
        "selected_option": correct_option  # отримати з БД
    })
    assert response.json()["is_correct"] == True
    assert response.json()["xp_gained"] == 10

# tests/test_boss.py
def test_boss_correct_submission(authenticated_client, completed_quiz_session):
    response = authenticated_client.post("/api/boss/submit", json={
        "session_id": str(boss_session.id),
        "code": "def swap_values(a, b):\n    return b, a"
    })
    data = response.json()
    assert all(t["passed"] for t in data["test_results"])
    assert data["boss_defeated"] == True
```

## 19.2 Фронтенд тести (Vitest + Testing Library)

```typescript
// src/components/game/QuizQuestion.test.tsx
describe('QuizQuestion', () => {
  it('renders question text', () => {
    render(<QuizQuestion question={mockQuestion} onAnswer={vi.fn()} />)
    expect(screen.getByText(mockQuestion.question_text)).toBeInTheDocument()
  })

  it('highlights correct answer after selection', async () => {
    const onAnswer = vi.fn()
    render(<QuizQuestion question={mockQuestion} onAnswer={onAnswer} />)
    
    fireEvent.click(screen.getByText('option A text'))
    
    await waitFor(() => {
      expect(screen.getByTestId('option-a')).toHaveClass('correct')
    })
  })
})
```

## 19.3 Мануальний QA чекліст

```
АВТОРИЗАЦІЯ:
[ ] Реєстрація з валідними даними
[ ] Реєстрація з існуючим email → помилка
[ ] Логін з правильними даними
[ ] Логін з неправильним паролем → помилка
[ ] Refresh token при 401

КВІЗ:
[ ] Старт квізу для першої локації
[ ] Правильна відповідь → крип гине, +XP
[ ] Неправильна відповідь → HP -1, пояснення
[ ] 5 неправильних → game over
[ ] 10 питань → перехід до боса
[ ] Питання перемішуються при рестарті

БОС:
[ ] Відображення задачі
[ ] Правильний код → тести проходять → бос HP -20 за кожен
[ ] Всі тести → бос помирає, перемога
[ ] Неправильний код → 0 тестів → бос атакує
[ ] Прихований тест не показує input/expected
[ ] Підказка 1 → -10 HP
[ ] Підказка 3 → -15 HP
[ ] Після перемоги → наступна локація розблокована

ПРОГРЕСІЯ:
[ ] XP нараховується правильно
[ ] Level up після набору порогу
[ ] Ачівмент після першого правильного
[ ] Лідерборд оновлюється
```

---

*Документ PyQuest TZ v2.0 FULL — готовий до розробки*  
*Всі розділи є обов'язковими для MVP за виключенням позначених (v2)*
