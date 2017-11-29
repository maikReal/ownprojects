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

    return requests.post(URL, data=payload, headers=head).text


def web_scraping(html_text):
    """
    Receive HTML and get all necessary information

    :param html_text:
    :return all_info:
    """

    dom = etree.HTML(html_text)

    # Flight numbers
    flight_numbers = dom.xpath("//div[@class='schedule-table-flight__cell'][1]/"
                               "span[@class='schedule-filght-name']/text()")

    # Duration of every flight
    duration_flight = dom.xpath("//div[@class='schedule-table-cell"
                                " hide-on-mobile']/"
                                "div[@class='schedule-table-time']/text()")

    # All dates of flights
    dates_flight = list(map(lambda x: x.strip(),
                            dom.xpath("//div[@class='schedule-table-cell"
                                      " schedule-table-cell_period']/"
                                      "div[@class='schedule-time-period']/"
                                      "text()")))

    link = "//div[@class='schedule-table-flight__direction']" \
           "/div[{0}]/{1}text()"

    # Create tuples: (place_departure, time_departure)
    #                (place_arrival, time_arrival)
    place_departure = list(filter(None,
                                  map(lambda x: x.strip(),
                                      dom.xpath(link.format('1', '')))))
    place_arrival = list(filter(None,
                                map(lambda x: x.strip(),
                                    dom.xpath(link.format('3', '')))))
    time_departure = list(map(lambda x: x.strip(),
                              dom.xpath(link.format('1', 'span/'))))
    time_arrival = list(map(lambda x: x.strip(),
                            dom.xpath(link.format('3', 'span/'))))

    departure = []
    arrival = []
    for i in range(len(flight_numbers)):
        departure.append(place_departure[i] + ' -> ' + time_departure[i])
        arrival.append(place_arrival[i] + ' -> ' + time_arrival[i])

    days_flight = dom.xpath("//div[@class='schedule-table-cell"
                            " schedule-table-cell_period']/"
                            "div[@class='weak-row']/span")

    # Days of all available flights
    # I know that hardcore, but right now
    # I don't know how can write this part easier
    counter = 0
    all_days_flight = []
    mas = []
    for i in days_flight:
        if days_flight.index(i) == len(days_flight) - 1:
            all_days_flight.append(mas)
        if counter == 7:
            all_days_flight.append(mas)
            mas = []
            counter = 0
        if i.get('class') != 'disable':
            element = ' '.join(list(map(lambda x: x.strip(),
                                        i.xpath('text()'))))
            mas.append(element)
        counter += 1

    all_info = []
    for i in range(len(flight_numbers)):
        all_info.append(['Отправка: ' + departure[i],
                         'Прибытие: ' + arrival[i],
                         'Дни рейсов: ' + str(all_days_flight[i]),
                         'Даты отправки-прибытия: ' + dates_flight[i],
                         'Номер рейса: ' + flight_numbers[i],
                         'Длительность полета: ' + duration_flight[i]])

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
    PLACES = input('Input place of departure and arrival'
                   '(in the form of IATA-code): ').split()
    FIRST_PLACE = PLACES[0].upper()
    SECOND_PLACE = PLACES[1].upper()
    if len(FIRST_PLACE) == 3 and len(SECOND_PLACE) == 3:
        INFORMATION = web_scraping(get_html(FIRST_PLACE, SECOND_PLACE))
        save_file(INFORMATION)
    else:
        print('Input error! Try again!')
