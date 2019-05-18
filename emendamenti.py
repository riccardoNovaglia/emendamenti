import csv


class Senator:
    def __init__(self, name, parties):
        self.name = name
        self.parties = parties

    def __str__(self):
        return '{}, {}'.format(self.name, self.parties)


def get_amendments_from_csv():
    with open('./data/Chamber_amend_BuonaScuola.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [row for row in reader]


def get_senators():
    with open('./data/camera_and_parties/camera_parties_legislature_17.csv', newline='') as csvfile:
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


if __name__ == '__main__':
    senators = get_senators()
    amendments_rows = get_amendments_from_csv()
    not_found = set()

    for row in amendments_rows:
        sponsors_list = row['Firmatari'].split(', ')
        all_matching_parties = []
        for sponsor in sponsors_list:
            try:
                matching_parties = next(
                    senator.parties for senator in senators if names_match(sponsor, senator.name))
                all_matching_parties.extend(matching_parties)
            except StopIteration as stop:
                not_found.add(sponsor)

        row['SPONSOR_PARTIES'] = ';'.join(all_matching_parties)

    write_new_rows(
        amendments_rows,
        'test.csv'
    )

    # print('not found {}:'.format(len(not_found)))
    # for n in sorted(not_found):
    #     print(n)
