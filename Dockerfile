FROM python:3.8

COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r /requirements.txt

WORKDIR /app

COPY aviata/* /app/

CMD ["celery", "-A", "celery_app", "worker"]
