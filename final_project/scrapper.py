""""
Scrapper of the air company 'POBEDA'.
Version 0.1.

Useful info:
For the beginning of the program indicate 2 places
in the form of IATA-code

Developed by Krupin Mihail
"""
import sys
import requests
from lxml import etree

URL = 'https://www.pobeda.aero/services/flight_schedule'


def get_html(departure, arrival):
    """
    Send request to website and get the answer from server
    Check for an error
    Then if everything ok, make answer like HTML

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
    try:
        html.raise_for_status()
        return html.text
    except requests.HTTPError:
        print('Sorry, some problems with server response.'
              'Try later')


def clear_string(string):
    """
    Replace symbols from symbols_for_removing
    to an empty space

    :param string:
    :return checking string:
    """
    symbols_for_removing = (' ', '[', ']', '\\n', ',')
    for symbol in symbols_for_removing:
        string = string.replace(symbol, '')
    return string


def web_scraping(html_text):
    """
    Receive HTML and get all necessary information
    about all flights

    :param html_text:
    :return all_info:
    """
    dom = etree.HTML(html_text)

    all_info = []

    flight_blocks = dom.xpath(
        '//div[@class="schedule-table__wrapper"]'
        '//div[contains(@class, "schedule-table")]'
        '/div[contains(@class, "schedule-table-row_flight")]'
    )

    for flight_block in flight_blocks:
        flight_number = str(flight_block.xpath('.//span[@class=\''
                                               'schedule-filght-name\']'
                                               '/text()'))

        duration_flight = str(flight_block.xpath('.//div[@class=\''
                                                 'schedule-table-time\']'
                                                 '/text()'))

        days_flight = [
            day.strip().replace('\n', '')
            for day in flight_block.xpath(
                './/div[contains(@class, \'schedule-table-cell_period\')]'
                '//div[@class=\'weak-row\']'
                '/span[not(contains(@class,\'disable\'))]/text()')
        ]

        days_flight = ', '.join(days_flight)

        dates_flight = str(flight_block.xpath(
            './/div[@class=\'schedule-time-period\']'
            '/text()')).replace('\n', '')

        place_departure = str(flight_block.xpath(
            './/div[@class=\'schedule-table-flight__direction\']'
            '/div[1]/text()'))

        place_arrival = str(flight_block.xpath(
            './/div[@class=\'schedule-table-flight__direction\']'
            '/div[3]/text()'))

        all_info.append(['Departure: ' + clear_string(place_departure)
                         + '\n',
                         'Arrival: ' + clear_string(place_arrival)
                         + '\n',
                         'Days of flight: ' + clear_string(days_flight)
                         + '\n',
                         'Dates of departure-arrival: '
                         + clear_string(dates_flight) + '\n',
                         'Flight number: ' + clear_string(flight_number)
                         + '\n',
                         'Duration of flight: ' + clear_string(duration_flight)
                         + '\n'])

    if not all_info:
        print('Sorry, there is no information for this flight')
    else:
        return all_info


def save_file(info):
    """
    Receive all info and save it on file

    :param info:
    """
    # flight_information.txt - file where all flight information is located
    with open(r'flight_information.txt', 'w') as f_object:
        for flight in info:
            f_object.writelines(flight)
            f_object.write('\n')


def print_info_flight(flight):
    """
    Take the certain flight and
    give the details of it
    Then print them

    :param flight:
    :print details of flight:
    """
    for info in flight:
        print(info.strip())


def print_information(data):
    """
    Take all flights and use the print_info_flight()
    to every flight

    :param data:
    :return:
    """
    for flight in data:
        print_info_flight(flight)
        print('\n')


def print_hint():
    """
    Print some hint for user

    :print hint:
    """
    hint = """
        VKO - MOSCOW
        LED - SAINT-PETERSBURG
        AMS - AMSTERDAM
        JRB - NEW-YORK
        BQH - LONDON
        DLP - PARIS
        BZS - WASHINGTON
        """
    print(hint)


def check_input(input_raw):
    """
    Check the input of user

    :param input_raw:
    :return first_place, second_place:
    """
    input_raw = input_raw.split()
    first_place = input_raw[0]
    second_place = input_raw[1]
    if len(first_place) == 3 and len(second_place) == 3:
        return first_place, second_place
    else:
        print('Wrong format of IATA code! Try again!')


def main():
    """
    The main function where we use all another fucntions
    for parsing of website

    :return information about flights:
    """
    print('WELCOME TO FLIGHT SEARCHING APP\n'
          'Input two places in the IATA-code form (like VKO, it\'s Moscow)\n'
          'For watching the most popular IATA-codes, input \'help\'')

    while True:
        word = sys.stdin.readline()

        if word == 'help':
            print_hint()
        else:
            places = check_input(word)
            if places:
                website = get_html(places[0], places[1])
                if website:
                    information = web_scraping(website)
                    if information:
                        save_file(information)
                        print_information(information)
                        print("All information in the text file "
                              "'flight_information.txt'")
                        break


if __name__ == '__main__':
    main()
