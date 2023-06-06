import requests
import json
from time import sleep

## WIZZAIR COOKIES
# _abck
# bm_sz - unnecessary
# ak_bmsc
# bm_sv
# bm_mi - unnecessary
# ASP.NET_SessionId - unnecessary
# RequestVerificationToken - necessary

def get_cookie_str(cookies):
    # print(cookies)

    cookies_str = ""
    for i, key in enumerate(cookies.keys()):
        if i > 0:
            cookies_str += "; "

        cookies_str += f"{key}={cookies[key]}"

    return cookies_str


h_agent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
}

headers_start = {
    'authority': 'wizzair.com',
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
}


flight_headers = {
    "Host": "be.wizzair.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://wizzair.com/",
    "Content-Type": "application/json;charset=utf-8",
    # "X-RequestVerificationToken": "d48fdc35a41340cbade681a40ca8ca32",
    "sentry-trace": "be6c2325e0974c1ea1c30f0943e3d42c-b1d2d318ab8950e0-0",
    "Content-Length": "175",
    "Origin": "https://wizzair.com",
    "Connection": "keep-alive",
    # "Cookie": "_abck=8C0D3E242A37107E229941191B7AE1F0~-1~YAAQrW7UF6M1hZWIAQAAk6YXmwp25QB3XnNzLwUN9puezwhcRDuDJXmlVRbTiva411e0Rwv/cyPlRmHpYGaeaFNHtK2RX3CqPZ1LfL6gR2J37FVWgG++WTyYr2+SKH1YONbLQ0CkFvwRe9Z34ODcj++bx4tEmUTg0zmUmVO7J5iqszLLEVseHQUygaPbSoGvqw973k7eh7WYwN4oYT/FgWCNY2Sm4fbuY7QrwTNyRUPNKvTVjX7Mdnacpttkhth4dialAQfNtf53rodhW9uI0JuiHUdYX4RDbu+EzAPx58afBOXlAF2qre+utNncN7tPcFYbhhrylhC3NxIwioeZ8Hbnowtl3A7VfUIs9JfLq0d3B5btTUo4I2nb329oDXb+b2N4xGcDFtv0uTSnL8A9C7PDRq0Ao9LZ55uIxeqqKQFzHweml+bfBXM2gLU9lr+ANMt3fviFZyCvYDIyJSE=~-1~-1~-1; _gcl_au=1.1.406035971.1686155990; _ga_G2EKSJBE0J=GS1.1.1686226744.2.1.1686229198.0.0.0; _ga=GA1.2.283287025.1686155990; _gid=GA1.2.925305282.1686155991; RequestVerificationToken=d48fdc35a41340cbade681a40ca8ca32; ak_bmsc=097BC9019D892052161CB6891F3F685F~000000000000000000000000000000~YAAQDpJkX9FnEZqIAQAALyfymhQp49L78x2aXmfiFl3JlY/uzmEvhHoNEfjXDsl5W3NgB1yPdJOSWp75NWKqSYrpoWC402uNt6JkpPkGjB7poWU5Bg7HI9OLRo7t/vrt3b49NGEbVqDZ6lLryh3On4zRMkRRCtXIQFBUnQ49utCRkR7wkPFsgYPoEHz9XWg7aZDQJmXubAnyBWgdlPRQAuaC0yAJUZihWvmPXLeDUkPwojk/W6caqy4RcH6ffPvqArcIEGtQu1mSNvMJGgH+nj13rF1oi7B8S4dRDVVYVrcV1sUqHTFBvJzxg8Cav5yWkdN39CCdSHJ9jutGqTpGzrk2GncUW7f9bdM2QYfLXUHg1MfnFrB7m91VpNUPI+ZQUksYTSa79GwR1qgAyxKkJ4AtjngkUu7gqjzcvB6FzzxS1M5SWIdnDlUlrOE7agInsPqe+jVef3xg8IHvLZPp3xUz37u2wIlb6Q3lNdx65sExoyFPnYBpYmjkUMpRqplW8ajpp6gvmIqWFnPmmPIA1VNi9qN5Nw==; bm_sz=ADDB25562E1BA20EEA94EEA7F8FEB301~YAAQDpJkX4xnEZqIAQAA3iHymhQCcCfhNwJEtROx7+dQW202ykuFGbnDM8LRHlbyeUzMWDly/JjjIPrdpmAMH3iEV89d/8EEgevvHfe8390xkHTJLKQLQWhmgbp1UxAvy+OJNWoAwlb0KcRaMvULxRMrDOOdk2Ms2jSMVAnl61x1xZQdv3Fn5QzIjh854SKYIcpNC9Xx9FUc0qmMh5YhdVMHDR/x/qk2wjc/j+Ex1Tb1Ch6e+YGhxPIO3Wvh0XZzHG9NXuT6fv4xMWdgdxgl334KMtRcJu6ECkuxDzGkj2cUj3eFF/jQ3hw3ecaryuAXioV23B6Vvsa3V+eD793KF80/DilyuxvaMY8PpjlPhb3xxNX/pi6LWhxElDEWOa4pqw0zjPVkwDyG4vLoM+O2P7/Y0xuaK7MAwMJFEkAEV++bBICqOJtrczpPYUo=~3749688~4404535; bm_sv=054AA76F638BA9F9AE3EE7C8E6964F19~YAAQrW7UF841hZWIAQAAIaoXmxTaL9HT+pakLffpQPFGsTAamHc/kgVZeYUd4bZNwYc+x5rK418RiNWqOZ73TfBr9Vfx6eCQNuIz+gPxLSbqMY1JF+Em2wyFwzxeh2w6/afiavFMbKaByAxx01EpjQ3zz8BXXU/rLZ9M8by1hHmQzThTpr61f2gNQjkHe5xs/QGUZJVZ5/WsszUQZfNpX+c6ukWgbzmm6rdeG25Ke+MOA7xZUMlkaLlCUMXvp/NwPF8=~1; _ga_GDS04RS8G3=GS1.1.1686226750.1.0.1686226753.0.0.0; _pin_unauth=dWlkPU1HWm1abVk1WlRNdE1qUmlNeTAwWlRJM0xUZzBNMkl0T0dJd1pHWXdaams0TTJKaw; _tt_enable_cookie=1; _ttp=RvlA5lR_mjged34Zprud4ZPWN-X; _gat_gtag_UA_2629375_25=1; ASP.NET_SessionId=0g515powxljqnagnrn5hxx2c",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers"
}

flight_cookies = {
    "_abck": "8C0D3E242A37107E229941191B7AE1F0~-1~YAAQrW7UF013hZWIAQAA4DAimwrhgnoRhP4bOv3ZF7RVgpB5rII+ho3baL6XfykDdaFCsgwYSOgv2fSPhFwU5eNEroVeVcmaBGYIByzvOE7nTjRBx3BHMh6NrUd13l06pHGUr+RedQkUvP+SbgtnOnaGz7ncLfKQA8e07ZESIIMAsJcXqlBQtjMd4f0p/513E5Keo/OqVclhShM5B6k1zCULop3jvw9/mUnN4hBkcRrPS8aZYIrNp4QrTD8ITwTaxfvuNZGvqopN6VBeLmBlxd4E121kWi7WR1v/o+5k0vzOboX7HUyk3Umt5qUBA/CaMGA+gqM7VbEkfQW8bd7hVFpx0zz4PN+1a8DYPTFxV3xOuNzae6Wjinu9ZsUu/uM6H6URMdkUiHUEhiMBg3jpk9+Hf6zD6hLGfC/Y74bHXjJPcSY7iOPU4WuosfMvmCKRra3LA5oPj4pARcbBiDk=~-1~-1~-1",
    "RequestVerificationToken": "d48fdc35a41340cbade681a40ca8ca32",
    "ak_bmsc": "097BC9019D892052161CB6891F3F685F~000000000000000000000000000000~YAAQDpJkX9FnEZqIAQAALyfymhQp49L78x2aXmfiFl3JlY/uzmEvhHoNEfjXDsl5W3NgB1yPdJOSWp75NWKqSYrpoWC402uNt6JkpPkGjB7poWU5Bg7HI9OLRo7t/vrt3b49NGEbVqDZ6lLryh3On4zRMkRRCtXIQFBUnQ49utCRkR7wkPFsgYPoEHz9XWg7aZDQJmXubAnyBWgdlPRQAuaC0yAJUZihWvmPXLeDUkPwojk/W6caqy4RcH6ffPvqArcIEGtQu1mSNvMJGgH+nj13rF1oi7B8S4dRDVVYVrcV1sUqHTFBvJzxg8Cav5yWkdN39CCdSHJ9jutGqTpGzrk2GncUW7f9bdM2QYfLXUHg1MfnFrB7m91VpNUPI+ZQUksYTSa79GwR1qgAyxKkJ4AtjngkUu7gqjzcvB6FzzxS1M5SWIdnDlUlrOE7agInsPqe+jVef3xg8IHvLZPp3xUz37u2wIlb6Q3lNdx65sExoyFPnYBpYmjkUMpRqplW8ajpp6gvmIqWFnPmmPIA1VNi9qN5Nw==",
    "bm_sv": "054AA76F638BA9F9AE3EE7C8E6964F19~YAAQrW7UF7t3hZWIAQAAbkYimxRTdMEAwce1tRD3RtTQBkqI7xnguY7BanfRQJsvG7NgSh/hr+xQSUmZu3Dxu3cQ9mGXlR5Blc+hAlSq57NJA6iq+WTcnDSfhiOPpsS3nY32+mY1rlUIYQ9zk7dhe8dqJE9SBRHo1WwIwBbpUovMSaFf+W+dz3NIexg8y6KCbpQtDvqfh6PCOZjWrOQP+ej79xDOLKbXoOugdpPzxAlnJLqNcA5wquLMD36mtffkQkk=~1",
}


blank = requests.Session()
blank.headers.update(headers_start)

def foo(my_session: requests.Session):
    # get cookies
    url = "https://www.wizzair.com"
    r = my_session.get(url)
    if r.status_code != 200:
        print(url, r.status_code, r.text)

    r = my_session.get("https://be.wizzair.com/17.5.0/Api/asset/country?languageCode=en-gb")
    if r.status_code != 200:
        print(url, r.status_code, r.text)

    url = "https://be.wizzair.com/17.5.0/Api/asset/map?languageCode=en-gb"
    r = my_session.get(url)
    if r.status_code != 200:
        print(url, r.status_code, r.text)

    pl = {"isRescueFare": False, "adultCount": 2, "childCount": 0, "dayInterval": 7, "wdc": False, "isFlightChange": False, "flightList": [{"departureStation": "PRG", "arrivalStation": "LTN", "date": "2023-06-09"}]}
    url = "https://be.wizzair.com/17.5.0/Api/asset/farechart"
    r = my_session.post(url, json=pl)
    if r.status_code != 200:
        print(url, r.status_code, r.text)

    # get X-RequestVerificationToken cookie
    # my_session.headers.update(headers_start)
    url = "https://be.wizzair.com/17.5.0/Api/asset/currencies"
    r = requests.get(url, headers=h_agent)
    if r.status_code != 200:
        print(url, r.status_code, r.text)

    url = "https://be.wizzair.com/17.5.0/Api/search/flightDates?departureStation=PRG&arrivalStation=LTN&from=2023-06-09&to=2023-08-09"
    r = my_session.get(url)
    if r.status_code != 200:
        print(url, r.status_code, r.text)
    # my_session.cookies.set("RequestVerificationToken", q.cookies.get_dict()["RequestVerificationToken"])

    return my_session

payload = {
    "flightList":[
        {
            "departureStation": "PRG",
            "arrivalStation": "LTN",
            "departureDate": "2023-06-09"
        }
    ],
    "adultCount": 2,
    "childCount": 0,
    "infantCount": 0,
    "wdc": True,
    "isFlightChange": False,
    # "dayInterval": 3
}

blank = foo(blank)
blank_cookies = blank.cookies.get_dict()

# flight_headers["X-RequestVerificationToken"] = blank_cookies["RequestVerificationToken"]
# flight_headers["Cookie"] = get_cookie_str(blank_cookies)

flight_headers["Cookie"] = get_cookie_str(flight_cookies)
flight_headers["X-RequestVerificationToken"] = flight_cookies["RequestVerificationToken"]

print(blank_cookies)
print()
print()
print(flight_cookies)


URL = 'https://be.wizzair.com/17.5.0/Api/search/search'
response = blank.post(URL, json=payload, headers=flight_headers)
# response = blank.post(url, data=json.dumps(payload))
print(response.status_code)
print(response.text)
