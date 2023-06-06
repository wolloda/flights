import os
from db import Neo4j
from datetime import datetime
from airlines.ryanair import Ryanair
from airlines.wizzair import Wizzair
from dotenv import load_dotenv
import get_flights


if __name__  == "__main__":
    load_dotenv()

    start_date = datetime(2023, 9, 1)
    end_date = datetime(2023, 9, 30)

    URI = "neo4j://localhost"
    AUTH = (os.getenv("neo4j_username"), os.getenv("neo4j_password"))
    neo4j = Neo4j(URI, AUTH)

    # neo4j.delete_flights()
    # neo4j.delete_airports()

    airport_iatas = get_flights.read_airports("neo4j-community-4.4.21/import/destinations_2.csv")

    ryanair = Ryanair()
    flights_ryanair = ryanair.get_flights(airport_iatas, start_date, end_date)
    print(flights_ryanair)

    # wizzair = Wizzair()
    # flights_wizzair = wizzair.get_flights(airport_iatas, start_date, end_date, adults=2)
    # print(flights_wizzair)

    get_flights.save_to_csv("neo4j-community-4.4.21/import/flights.csv", flights_ryanair)

    neo4j.import_destinations("destinations_2.csv")
    neo4j.import_flights("flights.csv")

    # routes = neo4j.find_routes2()
    # for route in routes:
    #     print(route["f1"]["flight_search_url"])

    # routes = neo4j.find_routes()
    # for route in routes:
    #     print(route["f1"]["flight_search_url"])

