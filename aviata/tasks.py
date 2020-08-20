from celery.utils.log import get_task_logger

from aviata.celery_app import app
from aviata.exceptions import CheckInProgress, FlightAPIUnavailable
from aviata.settings import Settings
from aviata.utils import (
    get_cheapest_flight,
    get_flights_from_cache,
    get_forward_dates,
    verify_flight_not_changed,
    write_flight_to_cache,
)

logger = get_task_logger(__name__)


@app.task(
    bind=True, autoretry_for=(FlightAPIUnavailable,), retry_kwargs={"max_retries": 5}
)
def update_flight(self, fly_from: str, fly_to: str, date_from: str):
    logger.info(f"Requesting flights for {fly_from}-{fly_to} on {date_from}")
    price, booking_token = get_cheapest_flight(fly_from, fly_to, date_from)
    write_flight_to_cache(fly_from, fly_to, date_from, booking_token, price)
    logger.info("Flight info updated")


@app.task
def update_all_flights():
    for day in get_forward_dates():
        for row in Settings.FLIGHTS:
            update_flight.delay(row[0], row[1], day.strftime("%d/%m/%Y"))


@app.task(
    bind=True, autoretry_for=(FlightAPIUnavailable,), retry_kwargs={"max_retries": 5}
)
def check_flight(self, fly_from: str, fly_to: str, date_from: str, booking_token: str):
    logger.info(f"Verifying flight {fly_from}-{fly_to} on {date_from}")
    try:
        valid = verify_flight_not_changed(booking_token)
    except CheckInProgress as exc:
        logger.info(
            f"Check in progress. Scheduled retry in {Settings.FLIGHT_CHECK_DELAY}"
        )
        self.retry(exc=exc, countdown=Settings.FLIGHT_CHECK_DELAY)
    if not valid:
        logger.warning("Flight info outdated. Scheduled update")
        update_flight.delay(fly_from, fly_to, date_from)
    else:
        logger.info("Flight info is up-to-date")


@app.task
def check_all_flights():
    flights = get_flights_from_cache()
    for flight in flights:
        flight.pop("price")
        check_flight.delay(**flight)
