import csv


class CommitteeMember:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '{}'.format(self.name)


def get_committee_members(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [CommitteeMember(row['NAME']) for row in reader]

