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
    min_price = flights[0]["price"]
    booking_token = flights[0]["booking_token"]

    for flight in flights[1:]:
        if flight["price"] < min_price:
            min_price = flight["price"]
            booking_token = flight["booking_token"]

    return min_price, booking_token


def get_cheapest_flight(
    fly_from: str, fly_to: str, date_from: str, date_to: Optional[str] = None
):
    flights = get_flights(fly_from, fly_to, date_from, date_to)

    return select_cheapest_flight(flights)
