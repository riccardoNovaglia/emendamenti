import csv


class Senator:
    def __init__(self, name, parties):
        self.name = name
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


def get_amendments_from_csv():
    with open('./data/Senate_amend_legge_quadro_cicli.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [row for row in reader]


def get_senators(legislature_number):
    with open('./data/senato/senators_parties_legislature_{}.csv'.format(legislature_number), newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [Senator(row['NAME'], row['PARTIES'].split(',')) for row in reader]


def write_to_csv(senators, filename):
    print("Writing senators to file {}".format(filename))
    data = [['NAME', 'PARTIES', 'CONTRIBUTIONS', 'COMMITTEE_MEMBER']]
    for senator in senators:
        data.append([senator.name, ';'.join(senator.parties), senator.contributions, senator.get_committee_member()])

    with open(filename, 'w+') as myFile:
        writer = csv.writer(myFile, lineterminator='\n')
        writer.writerows(data)


def sponsor_name_in_sponsor_list(senator_name, sponsor_list):
    split_sponsor = senator_name.lower().split(' ')
    sponsor_list_names_lowercase = [sponsor_name.lower() for sponsor_name in sponsor_list]

    for name_part in split_sponsor:
        if name_part in sponsor_list_names_lowercase:
            return True
    return False


class CommitteeMember:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '{}'.format(self.name)


def get_committee_members(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [CommitteeMember(row['NAME']) for row in reader]


if __name__ == '__main__':
    senators = get_senators(13)
    committee_members = get_committee_members('./data/senato/committee_members_senate_legislature_13.csv')
    amendments_rows = get_amendments_from_csv()
    not_found = set()

    for senator in senators:
        for amendment in amendments_rows:
            amendment_sponsors = amendment['sponsor'].split(', ')
            if sponsor_name_in_sponsor_list(senator.name, amendment_sponsors):
                senator.increase_contribution()

        for committee_member_name in [member.name for member in committee_members]:
            if senator.name == committee_member_name:
                senator.set_committee_member()

    write_to_csv(
        senators,
        './data/contributions_count.csv'
    )
