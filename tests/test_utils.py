import pytest
import requests
from aviata.exceptions import FlightAPIUnavailable, NoFlightsFound
from aviata.utils import get_flights, select_cheapest_flight


class MockFailedResponse:
    status_code = 500

    @property
    def text():
        return "API is unavailable. Sorry for inconvinience"


class MockSuccessfulResponse:
    status_code = 200
    test_data = [
        {"price": 20, "booking_token": "first"},
        {"price": 30, "booking_token": "second"},
        {"price": 11, "booking_token": "third"},
    ]

    @classmethod
    def json(cls):
        return {"data": cls.test_data}


class MockSuccessfulBlankResponse(MockSuccessfulResponse):
    test_data = []


def test_get_flights_success(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockSuccessfulResponse

    monkeypatch.setattr(requests, "get", mock_get)

    flights = get_flights("ALA", "TSE", "14/09/2020")

    assert isinstance(flights, list)
    assert len(flights) == 3


def test_get_flights_fail(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockFailedResponse

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(FlightAPIUnavailable):
        flights = get_flights("ALA", "TSE", "14/09/2020")


def test_get_flights_blank(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockSuccessfulBlankResponse

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(NoFlightsFound):
        flights = get_flights("ALA", "TSE", "14/09/2020")


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ([{"price": 20, "booking_token": "A"},], "A",),
        (
            [
                {"price": 20, "booking_token": "A"},
                {"price": 30, "booking_token": "B"},
                {"price": 15, "booking_token": "C"},
            ],
            "C",
        ),
        (
            [
                {"price": 20.5, "booking_token": "A"},
                {"price": 20.44, "booking_token": "B"},
                {"price": 20.98, "booking_token": "C"},
            ],
            "B",
        ),
    ],
)
def test_select_cheapest_flight(test_input, expected):
    min_price, token = select_cheapest_flight(test_input)
    assert token == expected
