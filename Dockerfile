FROM python:3.8-slim

# Установка зависимостей
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копирование исходного кода
COPY src /app/src
COPY data /app/data
COPY tests /app/tests

# Установка рабочей директории
WORKDIR /app/src

# Установка точки входа
CMD ["python", "main.py"]
