import csv


class Senator:
    def __init__(self, name, parties):
        self.name = name
        self.parties = parties

    def __str__(self):
        return '{}, {}'.format(self.name, self.parties)


def get_amendments_from_csv():
    with open('updated_sponsors.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [row for row in reader]


def get_senators():
    with open('senators_parties_legislature_14.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [Senator(row['NAME'], row['PARTIES'].split(',')) for row in reader]


def write_new_rows(rows):
    print('Writing all new rows to file')
    with open('./amendments_14_with_parties.csv', newline='', mode='w+') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    senators = get_senators()
    amendments_rows = get_amendments_from_csv()
    not_found = set()

    for row in amendments_rows:
        sponsors_list = row['SPONSOR'].split(';')
        all_matching_parties = []
        for sponsor in sponsors_list:
            try:
                matching_parties = next(
                    senator.parties for senator in senators if sponsor.lower() in senator.name.lower())
                all_matching_parties.extend(matching_parties)
            except StopIteration as stop:
                not_found.add(sponsor)

        row['SPONSOR_PARTIES'] = ';'.join(all_matching_parties)

    write_new_rows(amendments_rows)

    # print('not found {}:'.format(len(not_found)))
    # for n in sorted(not_found):
    #     print(n)
