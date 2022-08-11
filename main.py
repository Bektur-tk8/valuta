import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup as BS


def get_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return 'Error'


def get_data(html):
    current_data = datetime.now().strftime('%m_%d_%Y')
    soup = BS(html, 'html.parser')
    table = soup.find('table', {'id': 'rates_table'})

    thead = table.find_all('tr')

    table_headers = []
    table_rates = [[]]

    for i in thead:
        table_th = i.find_all('th')
        table_td = i.find_all('td')
        if table_th:
            for th in table_th:
                th = th.text.strip()
                if th in ['USD', 'EURO', 'RUB', 'KZT']:
                    table_headers.append(th)
                    table_headers.append('')
                else:
                    table_headers.append(th)
        if table_td:
            bank_rates = []
            for td in table_td:
                td = td.text.strip()
                bank_rates.append(td)

            table_rates.append(bank_rates)

    with open(file=f'data_{current_data}.csv', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file)

        writer.writerow(table_headers)

        for row in table_rates:
            writer.writerow(row)

    return table_headers

def main():
    URL = 'https://www.akchabar.kg/ru/exchange-rates/'
    html = get_response(url=URL)
    # print(html)

    table = get_data(html)
    print(table)

# if name == '__main__':#
main()
