import csv


class Senator:
    def __init__(self, name, parties):
        self.name = name
        self.parties = parties
        self.contributions = 0

    def __str__(self):
        return '{}, {}, {}'.format(self.name, self.parties, self.contributions)

    def increase_contribution(self):
        self.contributions = self.contributions + 1


def get_amendments_from_csv():
    with open('./data/Senate_amend_legge_quadro_cicli.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [row for row in reader]


def get_senators(legislature_number):
    with open('./data/senato/senators_parties_legislature_{}.csv'.format(legislature_number), newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [Senator(row['NAME'], row['PARTIES'].split(',')) for row in reader]


def write_to_csv(senators, filename):
    print("Writing senators to file {}".format(filename))
    data = [['NAME', 'PARTIES', 'CONTRIBUTIONS']]
    for senator in senators:
        data.append([senator.name, ';'.join(senator.parties), senator.contributions])

    with open(filename, 'w+') as myFile:
        writer = csv.writer(myFile, lineterminator='\n')
        writer.writerows(data)


def sponsor_name_in_sponsor_list(senator_name, sponsor_list):
    split_sponsor = senator_name.lower().split(' ')
    sponsor_list_names_lowercase = [sponsor_name.lower() for sponsor_name in sponsor_list]

    for name_part in split_sponsor:
        if name_part in sponsor_list_names_lowercase:
            return True
    return False


if __name__ == '__main__':
    senators = get_senators(13)
    amendments_rows = get_amendments_from_csv()
    not_found = set()

    for senator in senators:
        for amendment in amendments_rows:
            amendment_sponsors = amendment['sponsor'].split(', ')
            if sponsor_name_in_sponsor_list(senator.name, amendment_sponsors):
                senator.increase_contribution()

    write_to_csv(
        senators,
        './data/contributions_count.csv'
    )
