from celery import Celery

app = Celery("aviata")

app.config_from_object("settings:Settings", namespace="CELERY")
