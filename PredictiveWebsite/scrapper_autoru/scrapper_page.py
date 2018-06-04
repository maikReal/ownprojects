import requests
import re
from lxml import etree
import time


page1 = 'https://www.avito.ru/nizhniy_novgorod/avtomobili/mitsubishi_space_star_2004_1123443675'
page2 = 'https://www.avito.ru/nizhniy_novgorod/avtomobili/skoda_yeti_2014_1398553298'
page3 = 'https://www.avito.ru/nizhniy_novgorod/avtomobili/suzuki_grand_vitara_2008_1721107846'


def get_html(url):
    response = requests.get(url)
    return response.text


def get_num(string):
    try:
        num = re.search(r'\d+', string).group()
    except AttributeError:
        num = '?'
    return num


def get_volume(string):
    try:
        vol = re.search(r'\d+.\d+', string).group()
    except AttributeError:
        vol = '?'
    return vol


def scrapper(html):

    dom = etree.HTML(html)

    desc = dom.xpath("//ul[@class='item-params-list']/li/text()")
    price = dom.xpath("//div[@id='price-value']/span[@class='price-value-string js-price-value-string']")[0]

    information = []

    if len(desc) == 32:
        information.append(desc[1].strip() + ',')  # model
        information.append(desc[5].strip() + ',')  # year
        information.append(get_num(desc[7].strip()) + ',')  # distance
        information.append(desc[9].strip() + ',')  # type
        information.append(get_volume(desc[13].strip()) + ',')  # volume

        if desc[15].strip().isdigit():  # transmission
            information.append(desc[17].strip() + ',')

        information.append(desc[19].strip() + ',')  # type_engine
        information.append(desc[21].strip() + ',')  # drive
        information.append(get_num(desc[31].strip()) + ',')  # power

        price = re.findall(r'\d+', price.text)
        price = ''.join(price)
        information.append(price + ',')

    if len(desc) == 30:
        information.append(desc[1].strip() + ',')  # model
        information.append(desc[5].strip() + ',')  # year
        if desc[7].strip() != 'NoneType':
            information.append(get_num(desc[7].strip()) + ',')  # distance
        information.append(desc[9].strip() + ',')  # type
        information.append(get_volume(desc[13].strip()) + ',')  # volume

        if desc[15].strip().isdigit():  # transmission
            information.append(desc[17].strip() + ',')

        information.append(desc[17].strip() + ',')  # type_engine
        information.append(desc[19].strip() + ',')  # drive
        information.append(get_num(desc[29].strip()) + ',')  # power

        price = re.findall(r'\d+', price.text)
        price = ''.join(price)
        information.append(price + ',')
    return information


def saving(arr):
    with open(r'new_info.txt', 'a') as f_obj:
        f_obj.writelines(arr)
        f_obj.write('\n')


def main():
    with open(r'links.txt') as f_obj:
        links = f_obj.readlines()
    links = list(map(lambda x: x.strip(), links))

    counter = 0
    for link in links:
        try:
            print(round((links.index(link) * 100) / len(links), 3), '%')
            print('Number of errors: ', counter)
            link = 'https://www.avito.ru' + link
            infor = scrapper(get_html(link))
            if len(infor) == 0:
                counter += 1
                continue
            else:
                saving(infor)
            time.sleep(13)
        except IndexError:
                counter += 1
                continue

    print('The parsing has finished')
    print('Spaces: ', counter)


if __name__ == '__main__':
    main()
