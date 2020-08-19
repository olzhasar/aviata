import time
from typing import List, Optional

import requests

from .exceptions import FlightAPIUnavailable, NoFlightsFound
from .settings import Settings


def get_flights(
    fly_from: str, fly_to: str, date_from: str, date_to: Optional[str] = None
):
    params = {
        "partner": Settings.PARTNER,
        "fly_from": fly_from,
        "fly_to": fly_to,
        "date_from": date_from,
        "date_to": date_to,
    }

    res = requests.get(Settings.FLIGHT_SEARCH_URL, params=params)

    if res.status_code != 200:
        raise FlightAPIUnavailable(res.text)

    data = res.json()["data"]

    if len(data) == 0:
        raise NoFlightsFound

    return data


def select_cheapest_flight(flights: List[dict]):
    cheapest = min(flights, key=lambda x: x["price"])

    return cheapest["price"], cheapest["booking_token"]


def get_cheapest_flight(
    fly_from: str, fly_to: str, date_from: str, date_to: Optional[str] = None
):
    flights = get_flights(fly_from, fly_to, date_from, date_to)

    return select_cheapest_flight(flights)


def check_flight(booking_token: str, pnum: int = 1, bnum: int = 1):
    params = {
        "affily": settings.AFFILY,
        "booking_token": booking_token,
        "pnum": pnum,
        "bnum": bnum,
    }

    while True:
        res = requests.get(settings.FLIGHT_CHECK_URL, params=params)

        data = res.json()

        if data["flights_checked"]:
            break

        print(
            "Flight checking has not finished yet. Retrying in"
            f" {settings.FLIGHT_CHECK_DELAY} secs"
        )

        time.sleep(settings.FLIGHT_CHECK_DELAY)

    return res.json()
