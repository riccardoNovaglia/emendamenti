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