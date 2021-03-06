FROM python:3.8

COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r /requirements.txt

WORKDIR /app

COPY aviata/ /app/aviata
COPY main.py /app/
COPY templates/ /app/templates

CMD ["celery", "-A", "aviata.celery_app", "worker", "--loglevel=info"]
