import csv


class Senator:
    def __init__(self, name, parties):
        self.name = name
        self.parties = parties

    def __str__(self):
        return '{}, {}'.format(self.name, self.parties)


def get_yes_nos():
    with open('./data/vezzi.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [row for row in reader]


def get_senators():
    with open('./data/senato/senators_parties_legislature_17.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [Senator(row['NAME'], row['PARTIES'].split(',')) for row in reader]


def write_new_rows(rows, filename):
    print('Writing all new rows to file')
    with open(filename, newline='', mode='w+', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def find_party(senator_name, senators_with_parties):
    for senator in senators_with_parties:
        if senator_name.lower() in senator.name.lower():
            return ';'.join(senator.parties)


if __name__ == '__main__':
    yes_nos = get_yes_nos()
    senators = get_senators()

    not_found = set()

    for row in yes_nos:
        name = row['NAME']

        senator_party = find_party(name, senators)
        row['PARTY'] = senator_party

    write_new_rows(
        yes_nos,
        './data/yes_nos_with_party.csv'
    )

    # print('not found {}:'.format(len(not_found)))
    # for n in sorted(not_found):
    #     print(n)
