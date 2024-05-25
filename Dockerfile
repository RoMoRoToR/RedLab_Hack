FROM python:3.8-slim

# Установка зависимостей для сборки h5py и других пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    pkg-config \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Установка pytest для тестирования
RUN pip install pytest

# Копирование исходного кода
COPY src /app/src
COPY data /app/data
COPY tests /app/tests

# Установка рабочей директории
WORKDIR /app/src

# Установка точки входа
CMD ["python", "main.py"]
