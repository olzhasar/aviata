import os


class Settings:
    AIRPORTS = {
        "ALA": "Almaty",
        "TSE": "Astana",
        "MOW": "Moscow",
        "LED": "Saint Petersburg",
        "CIT": "Shymkent",
    }

    FLIGHTS = (
        ("ALA", "TSE"),
        ("TSE", "ALA"),
        ("ALA", "MOW"),
        ("MOW", "ALA"),
        ("ALA", "CIT"),
        ("CIT", "ALA"),
        ("TSE", "MOW"),
        ("MOW", "TSE"),
        ("TSE", "LED"),
        ("LED", "TSE"),
    )

    FLIGHT_SEARCH_URL = "https://api.skypicker.com/flights"
    FLIGHT_CHECK_URL = "https://booking-api.skypicker.com/api/v0.1/check_flights"
    FLIGHT_CHECK_DELAY = 5
    PARTNER = "picky"
    AFFILY = "picky_kz"

    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = 6379
    REDIS_DB = 0
