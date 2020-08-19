import time
from datetime import date, timedelta
from typing import List, Optional, Union

import requests

from .exceptions import CheckInProgress, FlightAPIUnavailable, NoFlightsFound
from .redis import cache
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


def verify_flight_not_changed(booking_token: str, pnum: int = 1, bnum: int = 1):
    params = {
        "affily": Settings.AFFILY,
        "booking_token": booking_token,
        "pnum": pnum,
        "bnum": bnum,
    }

    res = requests.get(Settings.FLIGHT_CHECK_URL, params=params)

    data = res.json()

    if not data.get("flights_checked"):
        raise CheckInProgress

    if data["flights_invalid"] or data["price_change"]:
        return False

    return True


def write_flight_to_cache(
    fly_from: str,
    fly_to: str,
    date_from: str,
    booking_token: str,
    price: Union[int, float],
):
    key = f"{date_from}_{fly_from}_{fly_to}_"
    token_key = key + "token"
    price_key = key + "price"

    ex = 3600 * 24  # Cache record expires in 24 hours to avoid deleting manually
    cache.set(token_key, booking_token, ex=ex)
    cache.set(price_key, price, ex=ex)


def get_flights_from_cache(date: str = ""):
    flights = []

    for _key in cache.keys(f"{date}*_token"):
        key = _key.decode("utf-8")
        price_key = key.replace("token", "price")

        token = cache.get(key).decode("utf-8")
        price = float(cache.get(price_key))

        flights.append(
            {
                "date_from": key[:10],
                "fly_from": key[11:14],
                "fly_to": key[15:18],
                "booking_token": token,
                "price": price,
            }
        )

    return flights


def get_forward_dates(n: int = 30):
    today = date.today()
    for i in range(n):
        yield today + timedelta(days=i)
