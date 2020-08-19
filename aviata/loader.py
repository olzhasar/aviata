import time
from typing import List, Optional

import requests

from .exceptions import FlightAPIUnavailable, NoFlightsFound

FLIGHT_SEARCH_URL = "https://api.skypicker.com/flights"
FLIGHT_CHECK_URL = "https://booking-api.skypicker.com/api/v0.1/check_flights"
PARTNER = "picky"
AFFILY = "picky_kz"
FLIGHT_CHECK_DELAY = 5


def get_flights(
    fly_from: str, fly_to: str, date_from: str, date_to: Optional[str] = None
):
    params = {
        "partner": PARTNER,
        "fly_from": fly_from,
        "fly_to": fly_to,
        "date_from": date_from,
        "date_to": date_to,
    }

    res = requests.get(FLIGHT_SEARCH_URL, params=params)

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
        "affily": AFFILY,
        "booking_token": booking_token,
        "pnum": pnum,
        "bnum": bnum,
    }

    while True:
        res = requests.get(FLIGHT_CHECK_URL, params=params)

        data = res.json()

        if data["flights_checked"]:
            break

        print(
            f"Flight checking has not finished yet. Retrying in {FLIGHT_CHECK_DELAY}"
            " secs"
        )

        time.sleep(FLIGHT_CHECK_DELAY)

    return res.json()
