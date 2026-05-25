FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Seed the database on first run
CMD ["sh", "-c", "python -m app.seeds.seed_db && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
