"""
Seed: 10 локацій, 200 питань, 10 задач босів, ачівменти.
"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
import app.models  # noqa
from app.models.location import Location, Question
from app.models.boss_challenge import BossChallenge
from app.models.progress import Achievement
from app.seeds.boss_challenges import BOSS_CHALLENGES
from app.seeds.questions import QUESTIONS

LOCATIONS = [
    {"slug": "variables",   "name": "Рівнина Початку",    "order_index": 1,
     "description": "Безкраї поля, де все починається. Тут ти вперше дізнаєшся, як зберігати дані.",
     "topic": "Змінні та типи даних (int, float, str, bool, None)",
     "boss_name": "Змінний Хаос",    "boss_sprite_id": "chaos_boss",    "background_id": "green_plains",
     "enemy_sprite_id": "named_ghost",    "color_theme": "#7BC67E"},
    {"slug": "conditions",  "name": "Ліс Умов",           "order_index": 2,
     "description": "Густий ліс, де кожна стежка розгалужується. Правильна умова веде до виходу.",
     "topic": "Умовні оператори (if, elif, else, and, or, not)",
     "boss_name": "Вилка Долі",       "boss_sprite_id": "fork_boss",     "background_id": "dark_forest",
     "enemy_sprite_id": "branch_shadow",  "color_theme": "#5B9BD5"},
    {"slug": "loops",       "name": "Печера Циклів",      "order_index": 3,
     "description": "Темна печера, де час іде по колу. Лише той, хто знає вихід, вибереться.",
     "topic": "for, while, break, continue, range",
     "boss_name": "Нескінченний Голем","boss_sprite_id": "golem_boss",   "background_id": "dark_cave",
     "enemy_sprite_id": "cycle_spirit",   "color_theme": "#C0784E"},
    {"slug": "functions",   "name": "Вежа Функцій",       "order_index": 4,
     "description": "Стародавня вежа, де кожен поверх — окрема функція. Піднімись на вершину!",
     "topic": "def, return, аргументи, *args, **kwargs, lambda",
     "boss_name": "Рекурсивний Дракон","boss_sprite_id": "dragon_boss",  "background_id": "magic_tower",
     "enemy_sprite_id": "arg_elemental",  "color_theme": "#9B59B6"},
    {"slug": "lists",       "name": "Болото Списків",     "order_index": 5,
     "description": "Болото, де в кожній калюжі ховається елемент. Знайди правильний індекс!",
     "topic": "list, методи списків, зрізи, list comprehension",
     "boss_name": "Список-Пожирач",   "boss_sprite_id": "list_boss",    "background_id": "swamp",
     "enemy_sprite_id": "index_slime",    "color_theme": "#27AE60"},
    {"slug": "dicts",       "name": "Замок Словників",    "order_index": 6,
     "description": "Величний замок, де за кожними дверима — ключ і значення.",
     "topic": "dict, set, frozenset, методи словників",
     "boss_name": "Ключ-Майстер",     "boss_sprite_id": "key_boss",     "background_id": "castle",
     "enemy_sprite_id": "hash_ghost",     "color_theme": "#E67E22"},
    {"slug": "strings",     "name": "Хмарний Острів",    "order_index": 7,
     "description": "Острів у хмарах, де кожне слово має магічну силу.",
     "topic": "str, методи рядків, f-strings, форматування",
     "boss_name": "Форматований Ліч", "boss_sprite_id": "lich_boss",    "background_id": "cloud_island",
     "enemy_sprite_id": "char_fairy",     "color_theme": "#3498DB"},
    {"slug": "errors",      "name": "Ліс Помилок",        "order_index": 8,
     "description": "Ліс, де кожен крок може викликати виняток. Навчись їх ловити!",
     "topic": "try/except/finally/else, raise, Exception, типи помилок",
     "boss_name": "Баг-Лорд",         "boss_sprite_id": "bug_boss",     "background_id": "error_forest",
     "enemy_sprite_id": "exception_monster","color_theme": "#E74C3C"},
    {"slug": "oop",         "name": "Цитадель Класів",   "order_index": 9,
     "description": "Могутня цитадель, де об'єкти та класи правлять усім.",
     "topic": "class, __init__, self, наслідування, поліморфізм",
     "boss_name": "Об'єктний Колос",  "boss_sprite_id": "colossus_boss","background_id": "citadel",
     "enemy_sprite_id": "instance_zombie","color_theme": "#8E44AD"},
    {"slug": "modules",     "name": "Фінальна Вежа",     "order_index": 10,
     "description": "Фінальне випробування. Тут зібрані знання всього Python-світу.",
     "topic": "import, os, datetime, json, random, math",
     "boss_name": "Темний Компілятор","boss_sprite_id": "compiler_boss","background_id": "final_tower",
     "enemy_sprite_id": "module_guard",   "color_theme": "#2C3E50"},
]

ACHIEVEMENTS = [
    {"slug": "first_blood",    "name": "Перший Крип",         "description": "Дай першу правильну відповідь",       "icon_id": "sword",   "xp_reward": 10},
    {"slug": "no_death_1",     "name": "Безсмертний",          "description": "Пройди квіз без жодної смерті",       "icon_id": "shield",  "xp_reward": 25},
    {"slug": "boss_slayer",    "name": "Переможець Босів",     "description": "Вбий першого боса",                   "icon_id": "skull",   "xp_reward": 50},
    {"slug": "all_bosses",     "name": "Кілер Босів",          "description": "Вбий всіх 10 босів",                  "icon_id": "crown",   "xp_reward": 200},
    {"slug": "perfectionist",  "name": "Перфекціоніст",        "description": "10/10 у квізі без помилок",           "icon_id": "star",    "xp_reward": 30},
    {"slug": "first_try",      "name": "З Першої Спроби",      "description": "Вбий боса з першої спроби",           "icon_id": "lightning","xp_reward": 50},
    {"slug": "no_hints",       "name": "Без Підказок",         "description": "Вбий боса без підказок",              "icon_id": "brain",   "xp_reward": 30},
    {"slug": "streak_3",       "name": "На Роботі",            "description": "3 дні стріку поспіль",                "icon_id": "fire",    "xp_reward": 30},
    {"slug": "streak_7",       "name": "Тижневий Герой",       "description": "Стрік 7 днів",                        "icon_id": "fire",    "xp_reward": 100},
    {"slug": "streak_30",      "name": "Місячний Герой",       "description": "Стрік 30 днів",                       "icon_id": "fire",    "xp_reward": 500},
    {"slug": "speed_run",      "name": "Спідранер",            "description": "Пройди локацію менш ніж за 5 хвилин", "icon_id": "clock",   "xp_reward": 75},
    {"slug": "completionist",  "name": "Завершувач",           "description": "Пройди всі 10 локацій",               "icon_id": "trophy",  "xp_reward": 300},
    {"slug": "level_10",       "name": "Досвідчений",          "description": "Досягни 10 рівня",                    "icon_id": "gem",     "xp_reward": 50},
    {"slug": "level_20",       "name": "Ветеран",              "description": "Досягни 20 рівня",                    "icon_id": "diamond", "xp_reward": 100},
]


def seed(db: Session):
    print("🌱 Починаємо seed...")

    for ach in ACHIEVEMENTS:
        if not db.query(Achievement).filter(Achievement.slug == ach["slug"]).first():
            db.add(Achievement(**ach))
    db.commit()
    print(f"  ✅ {len(ACHIEVEMENTS)} ачівментів")

    for loc_data in LOCATIONS:
        loc = db.query(Location).filter(Location.slug == loc_data["slug"]).first()
        if not loc:
            loc = Location(**loc_data)
            db.add(loc)
            db.commit()
            db.refresh(loc)
            print(f"  📍 {loc.name}")

        if db.query(Question).filter(Question.location_id == loc.id).count() == 0:
            for q in QUESTIONS.get(loc.slug, []):
                db.add(Question(
                    location_id=loc.id,
                    question_text=q["q"], code_snippet=q.get("code"),
                    option_a=q["a"], option_b=q["b"],
                    option_c=q["c"], option_d=q["d"],
                    correct_option=q["ans"], explanation=q["exp"],
                ))
            db.commit()
            print(f"    ❓ {len(QUESTIONS.get(loc.slug, []))} питань")

        if not db.query(BossChallenge).filter(BossChallenge.location_id == loc.id).first():
            if loc.slug in BOSS_CHALLENGES:
                bd = BOSS_CHALLENGES[loc.slug]
                db.add(BossChallenge(
                    location_id=loc.id,
                    title=bd["title"], story_text=bd["story_text"],
                    task_text=bd["task_text"], function_signature=bd["function_signature"],
                    function_call_template=bd["function_call_template"],
                    starter_code=bd["starter_code"],
                    test_cases=bd["test_cases"], hints=bd["hints"],
                ))
                db.commit()
                print(f"    👹 Бос: {bd['title'][:50]}")

    print("✅ Seed завершено!")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
