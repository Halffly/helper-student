FROM python:3.10.2

WORKDIR /app

COPY req.txt .
COPY ./ .

RUN pip install -r req.txt

# Запускаем Python скрипт
CMD ["python", "main.py"]