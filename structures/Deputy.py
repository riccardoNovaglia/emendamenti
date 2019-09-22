import csv


class Deputy:
    def __init__(self, name, parties):
        self.name = name
        self.surname = self._extract_surname(name)
        self.parties = parties
        self.contributions = 0
        self.is_committee_member = False

    def __str__(self):
        return '{}, {}, {}'.format(self.name, self.parties, self.contributions)

    def increase_contribution(self):
        self.contributions = self.contributions + 1

    def set_committee_member(self):
        self.is_committee_member = True

    def get_committee_member(self):
        return 'yes' if self.is_committee_member else 'no'

    def _extract_surname(self, name):
        name_parts = name.split(' ')
        relevant = []
        for part in name_parts:
            if part.isupper():
                relevant.append(part)

        return ' '.join(relevant)


def get_deputies(filename):
    with open(filename, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [Deputy(row['NAME'], row['PARTIES'].split(',')) for row in reader]
