from datetime import datetime, timedelta
import requests
from typing import List
from .airline import Airline
from flight import Flight
from airport import Airport

class Ryanair(Airline):
    def get_flights(self, airport_iatas: List[str], start_date: datetime, end_date: datetime, adults: int = 1, teens: int = 0, children: int = 0, infants: int = 0):
        flights = self.__download_flights(airport_iatas, start_date, end_date)
        print(flights)
        print()
        print()
        flights = self.__parse_raw_data(flights, adults, teens, children, infants)
        print(flights)
        print()
        print()
        flights = list(filter(lambda x: x.arrival_airport.iata_code in airport_iatas, flights))
        print(flights)
        print()
        print()
        return flights

    def __download_flights(self, airport_iatas: List[str], start_date: datetime, end_date: datetime):
        """ Download all outgoing flights for all airports from a list of airport IATAs """
        flights = []
        trip_length = (end_date - start_date).days + 1

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

                    # print(response["size"])
                    # print(response["fares"])
                    # exit()

                    if response["size"] == 0:
                        # offset past results or no flights fulfilling criteria
                        break

                    flights += response["fares"]
                    offset += limit
        return flights

    def __parse_raw_data(self, flights: List, adults: int, teens: int, children: int, infants: int):
        flights_res = []

        for flight_info in flights:
            outbound = flight_info["outbound"]
            price_info = outbound["price"]

            dep_airport = outbound["departureAirport"]
            departure_airport = Airport(dep_airport["countryName"], dep_airport["iataCode"], dep_airport["name"],
                                        dep_airport["seoName"], dep_airport["city"])
            departure_date = datetime.strptime(outbound["departureDate"], "%Y-%m-%dT%H:%M:%S")

            arr_airport = outbound["arrivalAirport"]
            arrival_airport = Airport(arr_airport["countryName"], arr_airport["iataCode"], arr_airport["name"], arr_airport["seoName"], arr_airport["city"])
            arrival_date = datetime.strptime(outbound["arrivalDate"], "%Y-%m-%dT%H:%M:%S")

            price = outbound["price"]["value"]
            currency_code = outbound["price"]["currencyCode"]

            flight_search_url = 'https://www.ryanair.com/cz/cs/trip/flights/select?adults={adults}&teens={teens}&children={children}&infants={infants}&dateOut={date_out}&dateIn=&isConnectedFlight=false&isReturn=false&discount=0&promoCode=&originIata={origin_iata}&destinationIata={destination_iata}&tpAdults={adults}&tpTeens={teens}&tpChildren={children}&tpInfants={infants}&tpStartDate={date_out}&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata={origin_iata}'.format(adults=adults, teens=teens, children=children, infants=infants, date_out=departure_date.strftime('%Y-%m-%d'), origin_iata=departure_airport.iata_code, destination_iata=arrival_airport.iata_code)

            # todo: download conversion rates via API
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

            flights_res.append(Flight(departure_airport=departure_airport, arrival_airport=arrival_airport,
                                  company="Ryanair", departure_date=departure_date, arrival_date=arrival_date, price=price,
                                  flight_search_url=flight_search_url, currency_code=currency_code, flight_key=flight_key,
                                  flight_number=flight_number))

        return flights_res
