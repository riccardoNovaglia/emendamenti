import csv

import requests
from lxml import html

from read_csv import get_amendments_from_csv_as_dict


def new_sponsor_from(url):
    page_content = requests.get(url).content
    tree = html.fromstring(page_content)
    return tree.xpath('//*[@id="testo"]/p[2]')[0].text


if __name__ == '__main__':
    amendments = get_amendments_from_csv_as_dict('./amendments_14_with_parties.csv')

    with open('./amendments_14_updated_commissione.csv', newline='', mode='w+') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=amendments[0].keys())
        writer.writeheader()
        for a in amendments:
            if a['SPONSOR'] == "Commissione":
                updated_sponsor = new_sponsor_from(a['URL'])
                a['SPONSOR'] = updated_sponsor
            writer.writerow(a)
