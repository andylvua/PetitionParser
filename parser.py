import json

import bs4
import cloudscraper


def get_signatories_for_petition(petition_code: str):
    scraper = cloudscraper.create_scraper()

    petition_url = f'https://petition.president.gov.ua/petition/{petition_code}'

    page_number = 1
    names_list = []
    while True:
        print(f'Page {page_number}')
        request_result = scraper.get(petition_url + f'/votes/{page_number}/json')

        content = request_result.text.encode("UTF-8").decode("unicode-escape").replace("\\", "")

        text = request_result.text
        if '404. Такої сторінки не існує' in text:
            break

        soup = bs4.BeautifulSoup(content, features="lxml")
        names = soup.find_all('div', {'class': 'table_cell name'})

        for name in names:
            names_list.append(name.text)

        page_number += 1

    return names_list


def get_number_of_signatures_for_petition(petition_url: str):
    scraper = cloudscraper.create_scraper()

    request_result = scraper.get(petition_url)

    content = request_result.text

    soup = bs4.BeautifulSoup(content, features="lxml")
    number_of_signatures = int(soup.find('div', {'class': 'petition_votes_txt'}).span.text)

    return number_of_signatures

print(get_number_of_signatures_for_petition('https://petition.president.gov.ua/petition/145004'))
# list_of_signatories = get_signatories_for_petition('141740')
#
# with open("signatories_141740.json", "w", encoding='utf-8') as final:
#     json.dump(list_of_signatories, final, sort_keys=False, ensure_ascii=False, indent=4)
