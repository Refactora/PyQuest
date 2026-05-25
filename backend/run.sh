#!/bin/bash
# Запуск PyQuest backend локально

set -e

echo "🐍 PyQuest Backend — локальний запуск"
echo "======================================"

# 1. Встановити залежності (якщо треба)
if [ ! -d "venv" ]; then
  echo "📦 Створення venv..."
  python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt -q

# 2. Seed БД
echo "🌱 Наповнення бази даних..."
python -m app.seeds.seed_db

# 3. Запуск сервера
echo ""
echo "🚀 Запуск сервера на http://localhost:8000"
echo "📖 Документація: http://localhost:8000/docs"
echo ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
