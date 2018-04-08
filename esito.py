import csv

import requests
from lxml import html

from read_csv import get_amendments_from_csv_as_dict


def get_updated_esito_from(url):
    print(url)
    page_content = requests.get(url).content
    tree = html.fromstring(page_content)
    xpath = tree.xpath('//*[@id="testo"]/p')
    if len(xpath) < 3:
        return 'Unknown'

    text = xpath[2].text
    if text is None:
        return 'Unknown'
    if u'«' in text:
        print('funny thing in {}'.format(url))
        return 'Parzialmente recluso'
    ascii_safe = text.encode('ascii', 'ignore').decode('ascii')
    return ascii_safe


if __name__ == '__main__':
    amendments = get_amendments_from_csv_as_dict('./amendments_14_updated_commissione.csv')
    # amendments = get_amendments_from_csv_as_dict('./tst.csv')

    with open('./14_esito.csv', newline='', mode='w+') as csvfile:
    # with open('./tst.out.csv', newline='', mode='w+') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=amendments[0].keys())
        writer.writeheader()
        for i, a in enumerate(amendments):
            print('{}/{}'.format(i + 1, len(amendments)))
            if a['ESITO'] == "":
                updated_esito = get_updated_esito_from(a['URL'])
                a['ESITO'] = updated_esito

            writer.writerow(a)
