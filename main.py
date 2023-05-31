from datetime import datetime, timedelta
from tabulate import tabulate
from ryanair import Ryanair
import pickle
import csv

def main():
    airports = []
    with open('neo4j-community-4.4.21/import/destinations.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        airports = list(map(lambda x: x['iata'], reader))

    api = Ryanair(currency="EUR")

    start_date =  datetime(2023, 6, 9)
    end_date = datetime(2023, 6, 16)

    flights = api.get_cheapest_flights("PRG", start_date, start_date)
    flights = list(filter(lambda x: x.destination in airports, flights))

    with open("flights.pickle", "wb") as outfile:
        pickle.dump(flights, outfile)


    with open("flights.pickle", "rb") as infile:
        flights_reconstructed = pickle.load(infile)

    print(flights == flights_reconstructed)


    # print("\nflight #1")
    # print(tabulate(flights, headers="keys", tablefmt="github"))

    # flights_1 = []
    # for flight in flights:
    #     f = api.get_cheapest_flights(flight.destination, start + timedelta(days=2), start + timedelta(days=3))
    #     flights_1 += list(filter(lambda x: flight_valid(x, airports, 60), f))

    # print("\nflight #2")
    # print(tabulate(flights_1, headers="keys", tablefmt="github"))

    # flights_2 = []
    # for flight in flights_1:
    #     f = api.get_cheapest_flights(flight.destination, start + timedelta(days=4), start + timedelta(days=5))
    #     flights_2 += list(filter(lambda x: flight_valid(x, airports, 60), f))

    # print("\nflight #3")
    # print(tabulate(flights_2, headers="keys", tablefmt="github"))

    # flights_3 = []
    # for flight in flights_2:
    #     f = api.get_cheapest_flights(flight.destination, start + timedelta(days=6), start + timedelta(days=7))
    #     flights_3 += list(filter(lambda x: x.destination in [prague, brno], f))


    # print("\nflight #4")
    # print(tabulate(flights_3, headers="keys", tablefmt="github"))

if __name__ == "__main__":
    main()
