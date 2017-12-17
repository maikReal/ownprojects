""""

Scrapper of the air company 'POBEDA'

Useful info:
For the beginning of the program indicate 2 places
in the form of IATA-code

Developed by Krupin Mihail

"""

import requests
from lxml import etree

URL = 'https://www.pobeda.aero/services/flight_schedule'

help_me = """
VKO - MOSCOW
LED - SAINT-PETERSBURG
AMS - AMSTERDAM
JRB - NEW-YORK
BQH - LONDON
DLP - PARIS
BZS - WASHINGTON
"""


def get_html(departure, arrival):
    """
    Send request to website and get the answer from server
    Then make answer like HTML

    :param departure:
    :param arrival:
    :return html of website:
    """

    head = {
        'Host': 'www.pobeda.aero',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://www.pobeda.aero/services/flight_schedule',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    payload = {
        'action': 'get_schedules',
        'from': departure,
        'to': arrival
    }

    html = requests.post(URL, data=payload, headers=head)
    if str(html.status_code).startswith('5'):
        print('Sorry, some problems with server answer')
        return 1
    return html.text


def web_scraping(html_text):
    """
    Receive HTML and get all necessary information

    :param html_text:
    :return all_info:
    """

    dom = etree.HTML(html_text)

    flights_blocks = dom.xpath(
        '//div[@class="schedule-table__wrapper"]'
        '//div[contains(@class, "schedule-table")]'
        '/div[contains(@class, "schedule-table-row_flight")]'
    )

    # Flight numbers
    flight_numbers = dom.xpath("//div[@class='schedule-table-flight__cell'][1]/"
                               "span[@class='schedule-filght-name']/text()")

    # Find the place of transfer if he is
    transfer_link = "//div[@class='schedule-table-flight__direction']/text()"
    transfer = [transfer.strip() for transfer in dom.xpath(transfer_link) if transfer.strip()]

    # Duration of every flight
    # And time during the transfer
    if transfer:
        duration_flight = dom.xpath("//div[@class='schedule-tottal-mobile-time hide-on-desctop']/text()")
        time_transfer = dom.xpath("//div[@class='schedule-table-time transfer']/text()")
    else:
        duration_flight = dom.xpath("//div[@class='schedule-table-cell"
                                    " hide-on-mobile']/"
                                    "div[@class='schedule-table-time']/text()")

    # All dates of flights
    dates_flight = [date.strip() for date in dom.xpath("//div[@class='schedule-table-cell"
                                                       " schedule-table-cell_period']/"
                                                       "div[@class='schedule-time-period']/"
                                                       "text()")]

    link = "//div[@class='schedule-table-flight__direction']" \
           "/div[{0}]/{1}text()"

    # Create tuples: (place_departure, time_departure)
    #                (place_arrival, time_arrival)
    place_departure = [place.strip() for place in dom.xpath(link.format('1', '')) if place != None]

    place_arrival = [place.strip() for place in dom.xpath(link.format('3', '')) if place != None]

    time_departure = [time.strip() for time in dom.xpath(link.format('1', 'span/'))]

    time_arrival = [time.strip() for time in dom.xpath(link.format('3', 'span/'))]

    departure = []
    arrival = []
    for i in range(len(flight_numbers)):
        departure.append(place_departure[i] + ' -> ' + time_departure[i])
        arrival.append(place_arrival[i] + ' -> ' + time_arrival[i])

    # Different paths for days flight
    if transfer:
        days_flight = dom.xpath("//div[@class='schedule-table-cell"
                                " schedule-table-cell_period']/"
                                "div[@class='weak-row']/span")
    else:
        days_flight = dom.xpath("//div[@class='schedule-table-cell"
                                " schedule-table-cell_period']/"
                                "div[@class='weak-row']/span")

    # Days of all available flights
    # I know that hardcore, but right now
    # I don't know how can write this part easier

    all_days_flight = []
    for flight_block in flights_blocks:
        days_flight = [
            day.strip().replace('\n', '')
            for day in flight_block.xpath(
                './/div[contains(@class, "schedule-table-cell_period")]'
                '//div[@class="weak-row"]'
                '/span[not(contains(@class,"disable"))]/text()')
        ]
        all_days_flight.append(days_flight)

    all_info = []
    for i in range(len(transfer)):
        all_info.append(['Departure: ' + departure[i],
                         'Arrival: ' + arrival[i],
                         'Days of flight: ' + str(all_days_flight[i]),
                         'Dates of departure-arrival: ' + dates_flight[i],
                         'Flight number: ' + flight_numbers[i],
                         'Duration of flight: ' + duration_flight[i]])
        if transfer:
            all_info[i].insert(1, 'Transfer place: ' + transfer[i] + ' during ' + time_transfer[i])

    if not all_info:
        print('Sorry, there is no information for this flight')
        return 1
    return all_info


def save_file(info):
    """
    Receive all info and save it on file

    :param info:
    """

    # flight_information.txt - file where all flight information is located
    with open(r'flight_information.txt', 'w') as file:
        for flight in info:
            for value in flight:
                file.write(str(value) + '\n')
            file.write('\n')


if __name__ == '__main__':
    print('\t\t\t\t\t\t\t\t\tWELCOME TO FLIGHT SEARCHING APP\n'
          '\t\t\t\t\tInput two places in the IATA-code form (like VKO, it\'s Moscow)\n'
          '\t\t\t\t\t\tFor watching the most popular IATA-codes, input \'help\'')

    while True:
        word = input('Try to input: ')

        if word == 'help':
            print(help_me)
        else:
            word = word.split()
            first_place = word[0].upper()
            second_place = word[1].upper()
            if len(first_place) == 3 and len(second_place) == 3:
                website = get_html(first_place, second_place)
                if website == 1:
                    break
                else:
                    information = web_scraping(website)
                    if information == 1:
                        break
                    else:
                        save_file(information)
                        print("All information in the text file " 
                              "'flight_information.txt'")
                        break
