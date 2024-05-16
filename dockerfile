# Используйте официальный образ Python в качестве базового образа
FROM python:3.9-slim

# Установите переменную среды PYTHONUNBUFFERED для предотвращения буферизации вывода
ENV PYTHONUNBUFFERED=1

# Установите рабочую директорию внутри контейнера
WORKDIR /app

# Скопируйте файл зависимостей и установите их с помощью pip
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте файлы вашего FastAPI-проекта внутрь контейнера
COPY . .

# Команда для запуска вашего FastAPI-приложения с помощью uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Используйте официальный образ Python в качестве базового образа

FROM python:3.9-slim

# Установите переменную среды PYTHONUNBUFFERED для предотвращения буферизации вывода
ENV PYTHONUNBUFFERED=1

# Установите рабочую директорию внутри контейнера
WORKDIR /app

# Скопируйте файл зависимостей и установите их с помощью pip
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте файлы вашего FastAPI-проекта внутрь контейнера
COPY . .

# Команда для запуска вашего FastAPI-приложения с помощью uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]