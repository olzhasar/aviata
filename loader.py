from typing import List, Optional

import requests

from exceptions import FlightAPIUnavailable, NoFlightsFound

API_URL = "https://api.skypicker.com/flights"
PARTNER = "picky"


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

    res = requests.get(API_URL, params=params)

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
