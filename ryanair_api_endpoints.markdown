* copy of [vool / ryanapi.md](https://gist.github.com/vool/bbd64eeee313d27a82ab)

# API domains

https://desktopapps.ryanair.com

https://api.ryanair.com

## Airports

https://api.ryanair.com/aggregate/3/common?embedded=airports,countries,cities,regions,nearbyAirports,defaultAirport&market=en-gb

https://desktopapps.ryanair.com/en-gb/res/stations

## Closures

https://api.ryanair.com/aggregate/3/common?embedded=closures

## Flight info

https://api.ryanair.com/flightinfo/3/flights/?&arrivalAirportIataCode=&departureAirportIataCode=DUB&departureTimeScheduledFrom=00:00&departureTimeScheduledTo=23:59&length=&number=&offset=

## Schedules

https://desktopapps.ryanair.com/Calendar?Destination=EIN&IsTwoWay=false&Months=16&Origin=CFU&StartDate=2016-11-06

https://api.ryanair.com/timetable/3/schedules/DUB/LGW/years/2016/months/11

## Availability and fares info

https://desktopapps.ryanair.com/en-gb/availability?ADT=1&CHD=0&DateIn=2016-11-24&DateOut=2016-11-10&Destination=STN&FlexDaysIn=6&FlexDaysOut=6&INF=0&Origin=VLC&RoundTrip=true&TEEN=0&ToUs=AGREED

## Fair Finder

### One way


https://services-api.ryanair.com/farfnd/3/oneWayFares?&departureAirportIataCode=BCN&language=en&limit=16&market=en-gb&offset=0&outboundDepartureDateFrom=2019-02-11&outboundDepartureDateTo=2019-10-28&priceValueTo=150

### Return

https://services-api.ryanair.com/farfnd/3/roundTripFares?&arrivalAirportIataCode=STN&departureAirportIataCode=VLC&inboundDepartureDateFrom=2019-04-11&inboundDepartureDateTo=2019-04-28&language=es&limit=16&market=es-es&offset=0&outboundDepartureDateFrom=2019-03-11&outboundDepartureDateTo=2019-03-28&priceValueTo=150

### Cheapest per day as well as availability:

https://api.ryanair.com/farefinder/3/oneWayFares/SXF/TSR/cheapestPerDay?market=de-de&outboundMonthOfDate=2017-04-01

### FareFinder Image paths

https://www.ryanair.com/de/de.farefinder.json is an JSON file in which several picture paths are declared :)

## Currencies

https://desktopapps.ryanair.com/bg-bg/res/currencies


## Discounts

https://api.ryanair.com/discount/3/discounts

## Markets

https://ryanair.com/ie/en.markets.json
https://www.ryanair.com/content/ryanair.markets.json

## Requires auth/session

https://desktopapps.ryanair.com/en-gb/checkin/checkinpassengers

