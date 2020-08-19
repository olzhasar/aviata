from celery import Celery
from celery.schedules import crontab

app = Celery(
    "aviata", broker="amqp://aviata:aviata@rabbitmq:5672//", include="aviata.tasks"
)

app.conf.beat_schedule = {
    "update-flights": {
        "task": "aviata.tasks.update_all_flights",
        "schedule": crontab(minute=0, hour=0),
    },
    "check-flights": {
        "task": "aviata.tasks.check_all_flights",
        "schedule": crontab(minute=0, hour="1-23"),
    },
}
