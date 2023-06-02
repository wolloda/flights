import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

class Neo4j:
    def __init__(self, URI, AUTH):
        self.URI = URI
        self.AUTH = AUTH

    def delete_airports(self):
        with GraphDatabase.driver(self.URI, auth=self.AUTH) as driver:
            driver.verify_connectivity()

            records, summary, keys = driver.execute_query(
                "MATCH (a:Airport) DELETE a;",
                database_="neo4j"
            )

    def delete_flights(self):
        with GraphDatabase.driver(self.URI, auth=self.AUTH) as driver:
            driver.verify_connectivity()

            records, summary, keys = driver.execute_query(
                "MATCH ()-[f:Flight]->() DELETE f;",
                database_="neo4j"
            )


    def import_destinations(self, filename):
        with GraphDatabase.driver(self.URI, auth=self.AUTH) as driver:
            driver.verify_connectivity()

            records, summary, keys = driver.execute_query(
                """
                LOAD CSV WITH HEADERS FROM 'file:///$filename' AS row
                WITH row WHERE row.id IS NOT NULL
                MERGE (a:Airport {
                    id: row.id,
                    iata: row.iata,
                    country: row.country,
                    city: row.city,
                    airport_to_city_price: row.airport_to_city_price,
                    airport_to_city_duration: row.airport_to_city_duration
                })
                RETURN *;
                """,
                filename=filename,
                database_="neo4j"
            )

    def import_flights(self, filename):
        with GraphDatabase.driver(self.URI, auth=self.AUTH) as driver:
            driver.verify_connectivity()

            records, summary, keys = driver.execute_query(
                """
                LOAD CSV WITH HEADERS FROM "file:///$filename" AS row
                WITH row WHERE row.id IS NOT NULL
                MATCH (departure_airport: Airport {iata: row.departure_iata})
                MATCH (arrival_airport: Airport {iata: row.arrival_iata})
                MERGE (departure_airport)-[:FLIGHT {
                    id: row.id,
                    departure_date: datetime(row.departure_date),
                    arrival_date: datetime(row.arrival_date),
                    duration: duration.inSeconds(datetime(row.departure_date), datetime(row.arrival_date)) / 60,
                    price: toFloat(row.price),
                    flight_search_url: row.flight_search_url,
                    currency_code: row.currency_code,
                    flight_number: row.flight_number,
                    flight_key: row.flight_key
                    }]->(arrival_airport)
                RETURN *;
                """,
                filename=filename,
                database_="neo4j"
            )

    def find_routes2(self):
        with GraphDatabase.driver(self.URI, auth=self.AUTH) as driver:
            driver.verify_connectivity()

            records, summary, keys = driver.execute_query(
                """
                MATCH (a0:Airport {iata: "PRG"})-[f1:FLIGHT]->(a1:Airport)-[f2:FLIGHT]->(a2:Airport)-[f3:FLIGHT]->(a3:Airport)-[f4:FLIGHT]->(a4:Airport)
                WITH
                    *,
                    f1.price + f2.price + f3.price + f4.price AS price
                RETURN
                       f1{dest: a0.city + " -> " + a1.city, time_in_city: duration.inSeconds(f2.departure_date, f1.arrival_date), .flight_number, .price, .departure_date, .arrival_date, .flight_search_url},
                       f2{dest: a1.city + " -> " + a2.city, time_in_city: duration.inSeconds(f3.departure_date, f2.arrival_date), .flight_number, .price, .departure_date, .arrival_date, .flight_search_url},
                       f3{dest: a2.city + " -> " + a3.city, time_in_city: duration.inSeconds(f4.departure_date, f3.arrival_date), .flight_number, .price, .departure_date, .arrival_date, .flight_search_url},
                       f4{dest: a3.city + " -> " + a4.city, .flight_number, .price, .departure_date, .flight_search_url},
                       f4.arrival_date AS arrival_at,
                       price
                ORDER BY price ASC
                LIMIT 10;
                """,
                database_="neo4j"
            )

            return records


    def find_routes(self):
        with GraphDatabase.driver(self.URI, auth=self.AUTH) as driver:
            driver.verify_connectivity()

            records, summary, keys = driver.execute_query(
                """
                MATCH (a0:Airport {iata: "PRG"})-[f1:FLIGHT]->(a1:Airport)-[f2:FLIGHT]->(a2:Airport)-[f3:FLIGHT]->(a3:Airport)-[f4:FLIGHT]->(a4:Airport)
                WITH
                    *,
                    f1.price + f2.price + f3.price + f4.price AS price,
                    ["BRQ", "PRG", "VIE", "BTS"] as last_airports,
                    [a0, a1, a2, a3, a4] AS cities
                CALL {
                    WITH a0, a1, a2, a3, a4
                    UNWIND [a0, a1, a2, a3, a4] as cities
                    RETURN collect(DISTINCT cities.city) as unique_cities
                }
                WITH *
                WHERE
                    datetime("2023-06-09") <= f1.departure_date < datetime("2023-06-10")
                    AND datetime("2023-06-16") <= f4.departure_date < datetime("2023-06-17T13:00:00Z")
                    AND f1.departure_date < f2.departure_date < f3.departure_date < f4.departure_date

                    AND (datetime() + duration.inSeconds(f2.departure_date, f1.arrival_date)) <= (datetime() + duration("PT-14H"))
                    AND (datetime() + duration.inSeconds(f3.departure_date, f2.arrival_date)) <= (datetime() + duration("PT-14H"))
                    AND (datetime() + duration.inSeconds(f4.departure_date, f3.arrival_date)) <= (datetime() + duration("PT-14H"))

                    AND (size(unique_cities) = size(cities) OR (size(unique_cities) = size(cities) - 1 AND cities[0] = cities[-1]))

                    AND NOT a1.iata IN last_airports
                    AND NOT a2.iata IN last_airports
                    AND NOT a3.iata IN last_airports
                    AND a4.iata IN last_airports
                RETURN
                       f1{dest: a0.city + " -> " + a1.city, time_in_city: duration.inSeconds(f2.departure_date, f1.arrival_date), .flight_number, .price, .departure_date, .arrival_date, .flight_search_url},
                       f2{dest: a1.city + " -> " + a2.city, time_in_city: duration.inSeconds(f3.departure_date, f2.arrival_date), .flight_number, .price, .departure_date, .arrival_date, .flight_search_url},
                       f3{dest: a2.city + " -> " + a3.city, time_in_city: duration.inSeconds(f4.departure_date, f3.arrival_date), .flight_number, .price, .departure_date, .arrival_date, .flight_search_url},
                       f4{dest: a3.city + " -> " + a4.city, .flight_number, .price, .departure_date, .flight_search_url},
                       f4.arrival_date AS arrival_at,
                       price
                ORDER BY price asc;
                """,
                database_="neo4j"
            )

            return records


if __name__  == "__main__":
    URI = "neo4j://localhost"
    load_dotenv()

    AUTH = (os.getenv("neo4j_username"), os.getenv("neo4j_password"))
    neo4j = Neo4j(URI, AUTH)

    routes = neo4j.find_routes2()
    for route in routes:
        print(route["f1"]["flight_search_url"])

    routes = neo4j.find_routes()
    for route in routes:
        print(route["f1"]["flight_search_url"])

