import csv

import requests
from lxml import html

from emendamenti import Senator
from find_and_replace import FindAndReplace


def remove_trailing_commas(find_and_replace):
    def update(a):
        del a['']
        return a

    def headers_lambda(a):
        copy = a.copy()
        del copy['']
        return copy.keys()

    find_and_replace \
        .find_and_replace_with_headers(headers_lambda=headers_lambda, update_lambda=update)


def update_commissione(find_and_replace):
    def new_sponsor_from(url):
        page_content = requests.get(url).content
        tree = html.fromstring(page_content)
        return tree.xpath('//*[@id="testo"]/p[2]')[0].text

    def match(a):
        return a['SPONSOR'] == "Commissione"

    def update(a):
        sponsor = new_sponsor_from(a['URL'])
        a['SPONSOR'] = sponsor
        return a

    find_and_replace.find_and_replace(match, update)


def update_sponsor(find_and_replace):
    def update(a):
        sponsor = a['SPONSOR']
        a['SPONSOR'] = sponsor.replace(',', ';')
        return a

    find_and_replace \
        .find_and_replace(update_lambda=update)


def update_sponsors_parties(find_and_replace, senators_filename):
    global senators

    def get_senators():
        with open(senators_filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            return [Senator(row['NAME'], row['PARTIES'].split(',')) for row in reader]

    senators = get_senators()

    def update(a):
        sponsors = a['SPONSOR']

        sponsors_list = sponsors.split(';')
        all_matching_parties = []
        for sponsor in sponsors_list:
            for senator in senators:
                if sponsor.lower() in senator.name.lower():
                    all_matching_parties.extend(senator.parties)

        a['SPONSOR_PARTIES'] = ';'.join(all_matching_parties)

        return a

    def headers_lambda(a):
        copy = a.copy()
        copy['SPONSOR_PARTIES'] = 'anything - only for header'
        return copy.keys()

    find_and_replace \
        .find_and_replace_with_headers(headers_lambda=headers_lambda, update_lambda=update)


if __name__ == '__main__':
    source_dataset = './data/amendments leg 16.csv'

    remove_trailing_commas(FindAndReplace(source_dataset, './outputs/16.1_no_commas.csv'))

    update_commissione(FindAndReplace('./outputs/16.1_no_commas.csv', './outputs/16.2_commissione.csv'))

    update_sponsor(FindAndReplace('./outputs/16.2_commissione.csv', './outputs/16.3_sponsors.csv'))

    update_sponsors_parties(FindAndReplace('./outputs/16.3_sponsors.csv', './outputs/16.final_parties.csv'),
                            senators_filename='senators_parties_legislature_16.csv')
