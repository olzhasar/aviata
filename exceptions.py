class FlightAPIUnavailable(Exception):
    """
    Raised when remote flight search API is unavailable
    """

    pass


class NoFlightsFound(Exception):
    """
    Raised when no flights can be found with specified params
    """

    pass
