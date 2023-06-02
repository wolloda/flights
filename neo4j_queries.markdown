# load airports

```cypher
LOAD CSV WITH HEADERS FROM "file:///destinations.csv" AS row
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
```

# load flights

```cypher
LOAD CSV WITH HEADERS FROM "file:///flights.csv" AS row
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
```

# example flight-finding query

```cypher
MATCH (prg:Airport {iata: "PRG"})-[f1:FLIGHT]->(a1:Airport)-[f2:FLIGHT]->(a2:Airport)-[f3:FLIGHT]->(a3:Airport)-[f4:FLIGHT]->(a4:Airport)
WHERE
    datetime("2023-06-10") > f1.departure_date >= datetime("2023-06-09")
    AND datetime("2023-06-17") > f4.departure_date >= datetime("2023-06-16")
    AND f4.departure_date > f3.departure_date > f2.departure_date > f1.departure_date
    AND (datetime() + duration.inSeconds(f2.departure_date, f1.arrival_date)) <= (datetime() + duration("PT-18H")) // 18+ hours at destination
    AND (datetime() + duration.inSeconds(f3.departure_date, f2.arrival_date)) <= (datetime() + duration("PT-18H")) // 18+ hours at destination
    AND (datetime() + duration.inSeconds(f4.departure_date, f3.arrival_date)) <= (datetime() + duration("PT-18H")) // 18+ hours at destination
    AND (a1.iata <> "PRG" AND a1.iata <> "BRQ" AND a1.iata <> "VIE" AND a1.iata <> "BTS")
    AND (a2.iata <> "PRG" AND a2.iata <> "BRQ" AND a2.iata <> "VIE" AND a2.iata <> "BTS")
    AND (a3.iata <> "PRG" AND a3.iata <> "BRQ" AND a3.iata <> "VIE" AND a3.iata <> "BTS")
    AND (a4.iata = "PRG" OR a4.iata = "BRQ" OR a4.iata = "VIE" OR a4.iata = "BTS")
RETURN prg.city,
       f1,
       a1.city,
       duration.inSeconds(f2.departure_date, f1.arrival_date) as time_in_a1,
       f2,
       a2.city,
       duration.inSeconds(f3.departure_date, f2.arrival_date) as time_in_a2,
       f3,
       a3.city,
       duration.inSeconds(f4.departure_date, f3.arrival_date) as time_in_a3,
       f4,
       a4.city,
       f1.price + f2.price + f3.price + f4.price AS price,
       f1.currency_code + " " + f2.currency_code + " " + f3.currency_code + " " + f4.currency_code as currencies
ORDER BY price asc;
```
