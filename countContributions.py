import csv

from structures.CommitteeMember import get_committee_members
from structures.Deputy import get_deputies


def get_amendments_from_csv(filename):
    with open(filename, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [row for row in reader]


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


if __name__ == '__main__':
    deputies = get_deputies('./data/camera_and_parties/camera_parties_legislature_13.csv')
    committee_members = get_committee_members('./data/camera_and_parties/committee_members_camera_legislature_13.csv')
    amendments_rows = get_amendments_from_csv('./data/Chamber_amend_quadro_cicli_updated.csv')

    for deputy in deputies:
        for amendment in amendments_rows:
            amendment_sponsors = amendment['sponsor'].split(', ')
            if sponsor_name_in_sponsor_list(deputy.name, amendment_sponsors):
                deputy.increase_contribution()

        for committee_member_name in [member.name for member in committee_members]:
            if deputy.name == committee_member_name:
                deputy.set_committee_member()

    write_to_csv(
        deputies,
        './data/camera_quadro_legislature_13_contributions_counts.csv'
    )
