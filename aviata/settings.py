class Settings:
    FLIGHT_SEARCH_URL = "https://api.skypicker.com/flights"
    FLIGHT_CHECK_URL = "https://booking-api.skypicker.com/api/v0.1/check_flights"
    PARTNER = "picky"
    AFFILY = "picky_kz"
    FLIGHT_CHECK_DELAY = 5
    CELERY_BROKER_URL = 'amqp://aviata:aviata@rabbitmq:5672//'
