import csv


def get_amendments_from_csv_as_dict(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [row for row in reader]
