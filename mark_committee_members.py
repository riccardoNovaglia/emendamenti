import csv


class CommitteeMember:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '{}'.format(self.name)


def get_amendments_from_csv(filename):
    with open(filename, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [row for row in reader]


def get_committee_members(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [CommitteeMember(row['NAME']) for row in reader]


def write_new_rows(rows, filename):
    print('Writing all new rows to file')
    with open(filename, newline='', mode='w+') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def sponsor_in_committee(members, sponsor):
    for committee_member in members:
        member_name_parts = committee_member.name.lower().split(' ')

        for part in member_name_parts:
            if part in sponsor:
                return 'yes'
    return 'no'


def is_sponsor_member_of_committee(committee_members, sponsors_list):
    return [
        sponsor_in_committee(committee_members, sponsor.lower())
        for sponsor in sponsors_list
    ]


if __name__ == '__main__':
    committee_members = get_committee_members('./data/senato/committee_members_senate_legislature_13.csv')
    amendments_rows = get_amendments_from_csv('./data/Senate_amend_legge_quadro_cicli_with_parties.csv')
    not_found = set()

    for row in amendments_rows:
        sponsors_list = row['sponsor'].split(', ')

        row['committee_member'] = ','.join(is_sponsor_member_of_committee(committee_members, sponsors_list))

    write_new_rows(
        amendments_rows,
        './data/Senate_amend_legge_quadro_cicli_with_parties_committee.csv'
    )
