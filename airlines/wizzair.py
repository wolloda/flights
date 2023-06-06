from .airline import Airline
from typing import List
import requests
from datetime import datetime, timedelta

class Wizzair(Airline):
    def get_flights(self, airport_iatas: List[str], start_date: datetime, end_date: datetime, adults: int = 1, children: int = 0, infants: int = 0):
        flights = self.__download_flights(airport_iatas, start_date, end_date, adults, children, infants, False)
        # flights = self.__parse_raw_data(flights, adults, teens, children, infants)
        # flights = list(filter(lambda x: x.arrival_airport.iata_code in airport_iatas, flights))
        return flights

    def __download_flights(self, airport_iatas: List[str], start_date: datetime, end_date: datetime, adults: int, children: int, infants: int, wdc: bool):
        """ Download all outgoing flights for all airports from a list of airport IATAs """
        flights = []
        trip_length = (end_date - start_date).days + 1

        headers = {
            "Host": "be.wizzair.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://wizzair.com/",
            "Content-Type": "application/json;charset=utf-8",
            "X-RequestVerificationToken": "bc24aba43c564b28afa836ca1d427aa6",
            "Content-Length": "175",
            "Origin": "https://wizzair.com",
            "Connection": "keep-alive",
            "Cookie": "_abck=2DB5A93249BBCC7AD1B49113140BC064~-1~YAAQr27UF4Y0bYiIAQAA6HahjQq4cYgBlkwuqS6QJw5lryK7AjGAK/0qQJYl4EH3Gk1DJEzvgp1n9shDJjTqklP7i0XpLciT5AKjvm3tPpNA8BGQ53S2vd3NKsx69NKXja3iTeCKO8JGktzdhyvVm06tk0/5r1drSpGQPk0PRsvjx+AF9H8eL16K3EBxgmPIKOyPXLSIO2YKPyFneEhzn+IlrlcCe23b1X6BjEjAd2O5tgLXv1wBLDH8QMVOl2Ji3DUDJZQxDcRm8mfeX4J+lK66fbH/X8GeemjO5N5hvUjsws50C19bE/7tBbUid+siBwyO80AtgOSvftU9Nwb6QQQLpz65gsL66+ENwS9jWwZKcX823ka//A9/NTR0W92KGJjWKZ6wPubIPtqflKNfEo8Zns35cT76no1Pw25EISs/MbVMicB5sKxtpNZ4KXSksQLN4xtvO7eiGy9c5ww=~-1~-1~-1; ak_bmsc=21AEA5ADFF2285314EA14C2ECE24993D~000000000000000000000000000000~YAAQr27UF3QxbYiIAQAAQwGhjRSF486P9Xa2TTh3avWgsF5lyu0dUsw1RlSecE+qHWuTBaoQyEBfDGfHiuuLfonTtqZXY6Tf4APrK/iUY1Loqn7os5QLVElYj2nGHxWEepdIoP4+qSEqWQcEzl8NREJie7Tn1Bax6+7xSw138VRn9LrmfzUh4iBiFyTsPPdecICIRZqzs2BYdRUYmxlsgsPRF7f8imyvNgNbNJpyfbxvh1m1/GTlIfXqeTbeJXZPDPuSTvxrpeumQenILiacKvyXQaI+Mydqn+t4pvsz/fo5cwYD0QZjaFGlsoNAnL6VPMQkABhRToSUQvc5dq9p0XnuyvzsW0QlkV+FaQaVopev1m4mg0hp5HdR31BF+Zw1vIBw3aPZpfSGYZVXK/AHM3GVg5BGc7hIqRJyOFSOeu0BYkvl0wfB/5goiP6LZ96yfntgtzZOnL9Xv/6Z; bm_sz=F828F25F4CC26687845E90405947D310~YAAQr27UF17sa4iIAQAAnYhwjRSNcRdk0tI+z2HJTlnwZC5z3rL34ohsDx5W11/qtVnSPEjQRPWNDoJaJVOuogQrSuplhYnPgGnQ7bt2vcbiYnNv/POvrstFPt4L9UoNEzA0DSavH9bPOPkwgkN+76Pe+dcl2yFxzhMBTBY3PV1VAnnUcyWCEk/FV52YWoK8JpoI5zXrnKpoZlS0GSRZJR3OmuF29wrax+inOBp8UQ1admeqVbfkUu9fjPzczDzVuJRfsx+kxX6WsYOCsbmAaNJB4ZKfZaJFBIDR3NGohnRb1XR6ZNgbKdNRti+m89uHS40W7Nuzwrgq1taz5mFqcXE4uOCn62JKXdBU16ipyab1fHhfx51irNgstNbWzR76R//+ew7LnrVMtUuKV1L7Jl5RRFSWu2v9BG/iJgU8slkk+Eu2KVNfw32+Ew==~3553593~3616837; bm_sv=D70B886A35622B01F0E8CDDB08A770C8~YAAQr27UF38xbYiIAQAApQKhjRTjHVjlwzsKwhMZKhoYcoueK9Y9CUmKsgvyxLaRXATUVaFilnZxXB25SwMzkNneJGwC+YLNl3DY3LYFErXtIS+3tDCdIFyEpod05IXF/K9CG16pObwlj3XjzyhPVxJ3rFJuA6M70QMEDyS2w/u7TtPoFu5YTOgZnHximSKaOweCB+BQyQRw2CTPwNAJVQkvEkUsw32knPs8yhjheRfAvj+sVINdsBZlQI6/5wLiFeU=~1; bm_mi=906B3EBA99C6AD505748A3F12EDAE95E~YAAQr27UF2Pta4iIAQAAdadwjRTSqKf4K3t1JMM9ATb+srTTteKwZYzOHGOasLvIcnXzT+Ic2LE1EixwBbTzNOXqcg2d7ZTNsR7PjUOuKlA75QRVqIxrOH06+pz6D0lzvrcp4eagY2pEP0stiHeTviMTviK3a35apBH+asEFRy/1oS+OT7CQ6y3+pYA4s2ehvi5I4LFkvc3UC12X5DUG3vK6nFj8ayiovcyxNWxQIf3fJSehFaPZoneCDtUYuPUWXJeipwn4JZ8xR408V/g4oekCYK5Ws1VM515pCxqNK07ONNj3wOXtVMqIIPfNmDE=~1; ASP.NET_SessionId=gx2rzawyz1vsvmi5nehl3tlv; RequestVerificationToken=bc24aba43c564b28afa836ca1d427aa6; _gcl_au=1.1.548654846.1686000158; _ga_G2EKSJBE0J=GS1.1.1686000158.1.1.1686003348.0.0.0; _ga=GA1.2.354202600.1686000158; _gid=GA1.2.1168952256.1686000162; _pin_unauth=dWlkPU1HWm1abVk1WlRNdE1qUmlNeTAwWlRJM0xUZzBNMkl0T0dJd1pHWXdaams0TTJKaw; _tt_enable_cookie=1; _ttp=hJNkqI7NHLnxUrL2yrcGUbO9L3S; _gat_gtag_UA_2629375_25=1; sec_cpt=6DE36A38BD3DA25D90A5B29A3ECB4A6E~3~YAAQr27UF8gzbYiIAQAA2GGhjQk2VUDAQ+klom5zoNet5A4vkaxi+bBUlS9ocWwjZNXfwabZD79oZlA2gU1zuYMPirAkOYxHbLFANDKnujpKb/U/Qg7EGLMyOToHpmHUFzzpL6TUmBH3YIjh9OBZwEtgrJSaPCZL3+mOUE31dc1RGJ5QbBIHsHKbU6mBnrNj4RtFl9LMqbXQt9mL1KGV0mQ6yx5ulmmazWCiC9CGQITOLzmh7m1WthCMGT9r0xVAoda9YgS8SoHCDqYxEY5Eb20GyzZQk2TGKUBqOQVcCJq0jUId+bEClBEFIf6dMKYM//BwxqRd78M6jAQRlAIHT7IK8abPcrePydMte2sXOTb1cMAztI/BRSSYc1lm8Qqy9Y9A8Nusmds7HKi7nxEU+cP1snY3wIscibOakl8F/HjRmlIP67L+LDmTjf1YOeyDLZwU0/2bIbr7BeW7AmAplo94L6QfHWx31wwSODj2raEc22iyEEn90w6p/sgnkuZ61F/FSxkAxTxg1BRDAyb+58KFaYCMFxXbzXPnsNfKw79QiWinavEsoHMBtxNc0Br6W94pK0dxXKqSALXoZ567NgtK+en2",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers"
        }

        payload = {
            "flightList":[
                {
                    "departureStation": "PRG",
                    "arrivalStation": "LON",
                    "departureDate": start_date.strftime("%Y-%m-%d")
                }
            ],
            "adultCount": adults,
            "childCount": children,
            "infantCount": infants,
            "wdc": wdc,
            "isFlightChange": False,
        }

        URL = 'https://be.wizzair.com/17.5.0/Api/search/search'

        dates = [start_date + timedelta(days=x) for x in range(0, trip_length)]
        for origin_iata in airport_iatas:
            for destination_iata in airport_iatas:
                if origin_iata == destination_iata:
                    continue

                for date in dates:
                    payload["flightList"][0]["departureStation"] = origin_iata
                    payload["flightList"][0]["arrivalStation"] = destination_iata
                    payload["flightList"][0]["departureDate"] = date.strftime("%Y-%m-%d")
                    response = requests.post(URL, json=payload, headers=headers)
                    try:
                        response.raise_for_status()
                    except requests.HTTPError as ex:
                        if ex.response.status_code == 400:
                            continue

                        raise ex
                    except requests.Timeout:
                        pass

                    response = response.json()

                    print(response)

                    # flights += response["fares"]
                    # offset += limit
        return flights

    def __parse_raw_data(self, flights: List, adults: int, teens: int, children: int, infants: int):
        flights = []

        for flight in flights:
            outbound = flight["outbound"]
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


            flight_search_url= 'https://wizzair.com/#/booking/select-flight/{origin_iata}/{destination_iata}/{date_out}/null/{adults}/{children}/{infants}/null'.format(origin_iata=departure_airport.iata_code, destination_iata=arrival_airport.iata_code, date_out=departure_date.strftime('%Y-%m-%d'), adults=adults, children=children, infants=infants)

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

            flights.append(Flight(departure_airport=departure_airport, arrival_airport=arrival_airport,
                                  company="Ryanair", departure_date=departure_date, arrival_date=arrival_date, price=price,
                                  flight_search_url=flight_search_url, currency_code=currency_code, flight_key=flight_key,
                                  flight_number=flight_number))

        return flights

