from celery import Celery

app = Celery("aviata")

app.config_from_object("aviata.settings:Settings", namespace="CELERY")
