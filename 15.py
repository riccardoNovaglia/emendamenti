import csv

import requests
from lxml import html

from emendamenti import Senator
from find_and_replace import FindAndReplace


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


def update_sponsors_parties(senators_filename):
    global senators

    def get_senators():
        with open(senators_filename, newline='') as csvfile:
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

    parties \
        .find_and_replace(update_lambda=update)


if __name__ == '__main__':
    # commissione = FindAndReplace('./data/amendments_15.csv', './outputs/15_commissione.csv')
    # update_commissione(find_and_replace=commissione)

    # sponsor = FindAndReplace('./outputs/15_commissione.csv', './outputs/15_sponsors.csv')
    # update_sponsor(find_and_replace=sponsor)

    # TODO: DOES NOT UPDATE THE HEADER!
    parties = FindAndReplace('./outputs/15_sponsors.csv', './outputs/15_parties.csv')
    update_sponsors_parties('senators_parties_legislature_15.csv')
