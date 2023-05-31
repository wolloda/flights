from datetime import datetime, timedelta
import requests
from typing import Dict
from dataclasses import dataclass
from tabulate import tabulate
from ryanair import Ryanair
import pickle
import csv

@dataclass
class Airport:
    country_name: str
    iata_code: str
    name: str
    seo_name: str
    city: Dict[str, str]

@dataclass
class Flight:
    departure_airport: Airport
    arrival_airport: Airport
    departure_date: datetime
    arrival_date: datetime
    price: float
    currency_code: str
    flight_number: str
    flight_key: str

def main():
    airports = []
    with open('neo4j-community-4.4.21/import/destinations.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        airports = list(map(lambda x: x['iata'], reader))

    start_date =  datetime(2023, 6, 9)

    flights = []
    for airport in airports:
        limit = 32
        dates = [start_date + timedelta(days=x) for x in range(0, 8)]
        for date in dates:
            offset = 0
            while True:
                URL = f"https://services-api.ryanair.com/farfnd/3/oneWayFares?departureAirportIataCode={airport}&limit={limit}&offset={offset}&outboundDepartureDateFrom={date.strftime('%Y-%m-%d')}&outboundDepartureDateTo={date.strftime('%Y-%m-%d')}"

                response = requests.get(URL)
                try:
                    response.raise_for_status()
                except requests.HTTPError as ex:
                    raise ex
                except requests.Timeout:
                    pass

                response = response.json()
                if response["size"] == 0:
                    break

                for fare in response["fares"]:
                    outbound = fare["outbound"]
                    dep_airport = outbound["departureAirport"]
                    arr_airport = outbound["arrivalAirport"]

                    departure_airport = Airport(dep_airport["countryName"], dep_airport["iataCode"], dep_airport["name"], dep_airport["seoName"], dep_airport["city"])
                    arrival_airport = Airport(arr_airport["countryName"], arr_airport["iataCode"], arr_airport["name"], arr_airport["seoName"], arr_airport["city"])
                    departure_date = datetime.strptime(outbound["departureDate"], "%Y-%m-%dT%H:%M:%S")
                    arrival_date = datetime.strptime(outbound["arrivalDate"], "%Y-%m-%dT%H:%M:%S")
                    price = outbound["price"]["value"]
                    currency_code = outbound["price"]["currencyCode"]
                    flight_key = outbound["flightKey"]
                    flight_number = outbound["flightNumber"]

                    flights.append(Flight(departure_airport=departure_airport, arrival_airport=arrival_airport,
                                          departure_date=departure_date, arrival_date=arrival_date, price=price,
                                          currency_code=currency_code, flight_key=flight_key,
                                          flight_number=flight_number))


                offset += limit

    flights = list(filter(lambda x: x.arrival_airport.iata_code in airports, flights))

    with open("flights.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["departure_iata", "arrival_iata", "departure_date", "arrival_date", "price", "currency_code", "flight_number", "flight_key"])
        for flight in flights:
            writer.writerow([flight.departure_airport.iata_code, flight.arrival_airport.iata_code,
                             flight.departure_date.strftime("%Y-%m-%dT%H:%M:%S"), flight.arrival_date.strftime("%Y-%m-%dT%H:%M:%S"), flight.price, flight.currency_code,
                             flight.flight_number, flight.flight_key])

    print(flights)

    with open("flights.pickle", "wb") as outfile:
        pickle.dump(flights, outfile)


if __name__ == "__main__":
    main()
