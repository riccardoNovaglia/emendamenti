import csv

from structures.Deputy import get_deputies


def get_amendments_from_csv(filename):
    with open(filename, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [row for row in reader]


def write_new_rows(rows, filename):
    print('Writing all new rows to file')
    with open(filename, newline='', mode='w+') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def names_match(sponsor_name, senator_surname):
    if sponsor_name.isspace():
        return False

    return sponsor_name.lower() == senator_surname.lower()


def find_matching_parties(sponsors, legislature_senators):
    all_matching_parties = []
    for sponsor in sponsors:
        try:
            matching_parties = next(
                senator.parties for senator in legislature_senators if names_match(sponsor, senator.surname))
            all_matching_parties.extend(matching_parties)
        except StopIteration as stop:
            not_found.add(sponsor)
    return all_matching_parties


if __name__ == '__main__':
    deputies = get_deputies('./data/camera_and_parties/camera_parties_legislature_13.csv')
    amendments_rows = get_amendments_from_csv('./data/Chamber_amend_quadro_cicli_updated.csv')
    not_found = set()

    for row in amendments_rows:
        sponsors_list = row['sponsor'].split(', ')

        found_parties = find_matching_parties(sponsors_list, deputies)

        row['sponsor_party'] = ','.join(found_parties)

    write_new_rows(
        amendments_rows,
        './data/Chamber_amend_quadro_cicli_updated.csv'
    )

    # print('not found {}:'.format(len(not_found)))
    # for n in sorted(not_found):
    #     print(n)
