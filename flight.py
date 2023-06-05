from dataclasses import dataclass
from airport import Airport
from datetime import datetime

@dataclass
class Flight:
    departure_airport: Airport
    arrival_airport: Airport
    departure_date: datetime
    arrival_date: datetime
    company: str
    price: float
    flight_search_url: str
    currency_code: str
    flight_number: str
    flight_key: str
