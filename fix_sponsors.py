import csv


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def write_new_rows(rows):
    with open('./updated_sponsors.csv', newline='', mode='w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(rows)


if __name__ == '__main__':
    with open('amendments_14.csv', newline='', errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        all_rows = [row for row in reader]
        up_to_sponsor = [row[:9] for row in all_rows]
        sponsor_and_blanks = [row[9:] for row in all_rows]

        updated_sponsors = [
            ','.join(filter(lambda name: name is not '', sponsor_and_blank))
            for sponsor_and_blank in sponsor_and_blanks
        ]

        updated_sponsors_without_numbers = [
            ','.join(filter(lambda name: not has_numbers(name), s.split(',')))
            for s in updated_sponsors
        ]

        to_semicolons = [s.replace(',', ';') for s in updated_sponsors_without_numbers]

        for index, row in enumerate(up_to_sponsor):
            row.append(to_semicolons[index])

        write_new_rows(up_to_sponsor)
