class Airline:
    def __init__(self, adults: int, teens: int, children: int, infants: int):
        self.flights = []
        self.adults = adults
        self.teens = teens
        self.children = children
        self.infants = infants

    def download_flights(self, airport_iatas: List, start_date: datetime, trip_length: int):
        self.flights = self.transform_flights(self.flights, self.adults, self.teens, self.children, self.infants)
        return self.flights

    def transform_flights(self, flights: List, adults: int, teens: int, children: int, infants: int) -> List[Flight]:
        return flights

