import csv

from read_csv import get_amendments_from_csv_as_dict


class UpdateStage:
    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename

    def find_and_replace(self, match_lambda, replace_lambda):

        amendments = get_amendments_from_csv_as_dict(self.input_filename)

        with open(self.output_filename, newline='', mode='w+') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=amendments[0].keys())
            writer.writeheader()
            for i, a in enumerate(amendments):
                print('{}/{}'.format(i + 1, len(amendments)))
                if match_lambda(a):
                    updated = replace_lambda(a)
                    writer.writerow(updated)
                else:
                    writer.writerow(a)

    def test(self):
        return UpdateStage('./tst.csv', 'tst.out.csv')


if __name__ == '__main__':
    def match(amendment):
        return True

    def update(amendment):
        amendment['URL'] = 'url'
        return amendment

    UpdateStage("", "")\
        .test()\
        .find_and_replace(match, update)
