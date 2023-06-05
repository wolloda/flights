from datetime import datetime, timedelta
import requests
from typing import List
from airport import Airport
from flight import Flight
import pickle
import csv

def read_airports(filepath: str):
    airports = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        airports = list(map(lambda x: x['iata'], reader))

    return airports

def download_flights(airport_iatas: List, start_date: datetime, trip_length: int):
    flights = []
    for iata in airport_iatas:
        limit = 32
        dates = [start_date + timedelta(days=x) for x in range(0, trip_length)]
        for date in dates:
            offset = 0
            while True:
                URL = f"https://services-api.ryanair.com/farfnd/3/oneWayFares?departureAirportIataCode={iata}&limit={limit}&offset={offset}&outboundDepartureDateFrom={date.strftime('%Y-%m-%d')}&outboundDepartureDateTo={date.strftime('%Y-%m-%d')}"

                response = requests.get(URL)
                try:
                    response.raise_for_status()
                except requests.HTTPError as ex:
                    raise ex
                except requests.Timeout:
                    pass

                response = response.json()
                if response["size"] == 0:
                    # offset past results or no flights fulfilling criteria
                    break

                flights += (response["fares"])
                offset += limit
    return flights

def transform_flights(flights: List, adults: int, teens: int, children: int, infants: int):
    flights_modified = []

    for flight in flights:
        outbound = flight["outbound"]
        price_info = outbound["price"]

        dep_airport = outbound["departureAirport"]
        departure_airport = Airport(dep_airport["countryName"], dep_airport["iataCode"], dep_airport["name"], dep_airport["seoName"], dep_airport["city"])
        departure_date = datetime.strptime(outbound["departureDate"], "%Y-%m-%dT%H:%M:%S")

        arr_airport = outbound["arrivalAirport"]
        arrival_airport = Airport(arr_airport["countryName"], arr_airport["iataCode"], arr_airport["name"], arr_airport["seoName"], arr_airport["city"])
        arrival_date = datetime.strptime(outbound["arrivalDate"], "%Y-%m-%dT%H:%M:%S")

        price = outbound["price"]["value"]
        currency_code = outbound["price"]["currencyCode"]

        flight_search_url = 'https://www.ryanair.com/cz/cs/trip/flights/select?adults={adults}&teens={teens}&children={children}&infants={infants}&dateOut={date_out}&dateIn=&isConnectedFlight=false&isReturn=false&discount=0&promoCode=&originIata={origin_iata}&destinationIata={destination_iata}&tpAdults={adults}&tpTeens={teens}&tpChildren={children}&tpInfants={infants}&tpStartDate={date_out}&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata={origin_iata}'.format(adults=adults, teens=teens, children=children, infants=infants, date_out=departure_date.strftime('%Y-%m-%d'), origin_iata=departure_airport.iata_code, destination_iata=arrival_airport.iata_code)

        currencies = {
            "DKK": 3.3,
            "EUR": 23.7,
            "GBP": 27.4,
            "NOK": 2,
            "SEK": 2.1
        }

        if currency_code in currencies:
            price *= currencies[currency_code]
            currency_code = "CZK"

        flight_key = outbound["flightKey"]
        flight_number = outbound["flightNumber"]

        flights_modified.append(Flight(departure_airport=departure_airport, arrival_airport=arrival_airport,
                              company="Ryanair", departure_date=departure_date, arrival_date=arrival_date, price=price,
                              flight_search_url=flight_search_url, currency_code=currency_code, flight_key=flight_key,
                              flight_number=flight_number))

    return flights_modified

def save_to_csv(filepath: str, flights: List[Flight]):
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["id", "departure_iata", "arrival_iata", "departure_date", "arrival_date", "price", "currency_code", "flight_number", "flight_key", "flight_search_url"])
        for i, flight in enumerate(flights):
            writer.writerow([i, flight.departure_airport.iata_code, flight.arrival_airport.iata_code,
                             flight.departure_date.strftime("%Y-%m-%dT%H:%M:%S"), flight.arrival_date.strftime("%Y-%m-%dT%H:%M:%S"), flight.price, flight.currency_code,
                             flight.flight_number, flight.flight_key, flight.flight_search_url])

def get_flights():
    start_date =  datetime(2023, 6, 9)
    adults = 2
    teens = 0
    children = 0
    infants = 0

    airport_iatas = read_airports('neo4j-community-4.4.21/import/destinations.csv')
    flights = download_flights(airport_iatas, start_date, 8)
    flights = transform_flights(flights, adults, teens, children, infants)
    flights = list(filter(lambda x: x.arrival_airport.iata_code in airport_iatas, flights))
    print(f"{len(flights)} flights exported")

    save_to_csv('neo4j-community-4.4.21/import/flights.csv', flights)

    with open("flights.pickle", "wb") as outfile:
        pickle.dump(flights, outfile)


if __name__ == "__main__":
    get_flights()
