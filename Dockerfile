FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /inventario

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY inventario/ .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]