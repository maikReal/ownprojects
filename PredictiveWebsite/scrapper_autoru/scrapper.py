import requests
import re
from lxml import etree
from functools import reduce
import time

web_url = 'https://www.avito.ru/nizhniy_novgorod/avtomobili'


def get_html(url):
    response = requests.get(url)
    return response.text


def get_number_pages(string):
    res = int(re.search(r'\d+', string).group())

    all_pages = ['https://www.avito.ru/nizhniy_novgorod/avtomobili?p=' + str(i)
                 for i in range(2, res)]
    all_pages.insert(0, 'https://www.avito.ru/nizhniy_novgorod/avtomobili')
    return all_pages


def gathering_of_links(html_text):
    dom = etree.HTML(html_text)

    links = []

    catalog1 = dom.xpath("//div[@class='js-catalog_before-ads']/div")
    catalog1 = catalog1[1:]
    catalog2 = dom.xpath("//div[@class='js-catalog_after-ads']/div")

    catalog = catalog1 + catalog2

    for item in catalog:
        try:
            link = item.xpath(".//a[@class='item-description-title-link']")[0].get('href')
            links.append(link)
        except IndexError:
            continue

    return links


def saving(links):
    # links = reduce(lambda x, y: x + y, links)

    with open(r'links.txt', 'a') as f_object:
        for link in links:
            f_object.writelines(link)
            f_object.write('\n')


def main():
    dom = etree.HTML(get_html(web_url))

    pages = dom.xpath("//div[@class='pagination-pages clearfix']/a")[-1].get('href')
    all_pages = get_number_pages(pages)

    for page in all_pages:
        print(round((all_pages.index(page) * 100) / len(all_pages), 3), '%')
        saving(gathering_of_links(get_html(page)))
        time.sleep(13)

    print('Tha parsing has finished')


if __name__ == '__main__':
    main()

