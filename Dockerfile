FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
COPY wheelhouse /wheelhouse

RUN pip install --no-cache-dir --no-index --find-links=/wheelhouse -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]