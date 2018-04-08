import csv


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def write_new_rows(rows):
    with open('./updated_sponsors.csv', newline='', mode='w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(rows)


def p(rows):
    for r in rows:
        print(r)


if __name__ == '__main__':
    with open('amendments_14.csv', newline='', errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        all_rows = [row for row in reader]
        up_to_sponsor = [row[:9] for row in all_rows]
        updated_sponsors = [row[9:] for row in all_rows]

        # remove quotes
        updated_sponsors = [
            [x.replace('"', '').strip() for x in s]
            for s in updated_sponsors
        ]

        # replace question marks left by funny accents with commas
        updated_sponsors = [
            [x.replace('?', ',').strip() for x in s]
            for s in updated_sponsors
        ]

        # remove blanks
        updated_sponsors = [
            ','.join(filter(lambda name: name is not '', s))
            for s in updated_sponsors
        ]

        # remove numbers
        updated_sponsors = [
            ','.join(filter(lambda name: not has_numbers(name), s.split(',')))
            for s in updated_sponsors
        ]

        # strip spaces from names
        updated_sponsors = [
            ','.join([x.strip() for x in s.split(',')])
            for s in updated_sponsors
        ]

        to_semicolons = [s.replace(',', ';') for s in updated_sponsors]

        for index, row in enumerate(up_to_sponsor):
            row.append(to_semicolons[index])

        write_new_rows(up_to_sponsor)
