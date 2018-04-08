import csv

import requests
from lxml import html

from read_csv import get_amendments_from_csv_as_dict


if __name__ == '__main__':
    amendments = get_amendments_from_csv_as_dict('./14_esito.csv')
    # amendments = get_amendments_from_csv_as_dict('./tst.csv')

    with open('./14_precluso.csv', newline='', mode='w+') as csvfile:
    # with open('./tst.out.csv', newline='', mode='w+') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=amendments[0].keys())
        writer.writeheader()
        for i, a in enumerate(amendments):
            print('{}/{}'.format(i + 1, len(amendments)))
            if a['ESITO'] == "Parzialmente recluso":
                a['ESITO'] = "Parzialmente precluso"

            writer.writerow(a)
