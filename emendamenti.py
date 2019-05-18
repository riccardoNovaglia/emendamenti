import csv


class Senator:
    def __init__(self, name, parties):
        self.name = name
        self.parties = parties

    def __str__(self):
        return '{}, {}'.format(self.name, self.parties)


def get_amendments_from_csv():
    with open('./data/senato/sen_emendamenti_gov_18.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [row for row in reader]


def get_senators(legislature_number):
    with open('./data/senato/leg_{}.csv'.format(legislature_number), newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [Senator(row['NAME'], row['PARTIES'].split(',')) for row in reader]


def write_new_rows(rows, filename):
    print('Writing all new rows to file')
    with open(filename, newline='', mode='w+') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def names_match(sponsor_name, senator_name):
    if sponsor_name.isspace():
        return False

    split_sponsor = sponsor_name.lower().split(' ')

    for name_part in split_sponsor:
        if name_part not in senator_name.lower():
            return False
    return True


def find_matching_parties(sponsors, legislature_senators):
    all_matching_parties = []
    for sponsor in sponsors:
        try:
            matching_parties = next(
                senator.parties for senator in legislature_senators if names_match(sponsor, senator.name))
            all_matching_parties.extend(matching_parties)
        except StopIteration as stop:
            not_found.add(sponsor)
    return all_matching_parties


if __name__ == '__main__':
    legislatures = {
        # '16': get_senators(16),
        # '17': get_senators(17),
        '18': get_senators(18)
    }
    amendments_rows = get_amendments_from_csv()
    not_found = set()

    for row in amendments_rows:
        sponsors_list = row['FIRMATARI'].split(', ')

        # legislature = row['Legislatura']

        senators = legislatures.get('18')

        found_parties = find_matching_parties(sponsors_list, senators)

        row['SPONSOR_PARTIES'] = ';'.join(found_parties)

    write_new_rows(
        amendments_rows,
        './data/senato/with_parties.csv'
    )

    # print('not found {}:'.format(len(not_found)))
    # for n in sorted(not_found):
    #     print(n)
