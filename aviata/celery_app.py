from celery import Celery

app = Celery(
    "aviata", broker="amqp://aviata:aviata@rabbitmq:5672//", include="aviata.tasks"
)
