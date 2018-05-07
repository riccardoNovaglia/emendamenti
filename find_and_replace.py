import csv

from read_csv import get_amendments_from_csv_as_dict


class FindAndReplace:
    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename

    def find_and_replace(self, match_lambda=lambda x: True, update_lambda=lambda x: x):

        amendments = get_amendments_from_csv_as_dict(self.input_filename)

        self._read_and_update(amendments, amendments[0].keys(), match_lambda, update_lambda)

    def find_and_replace_with_headers(self, headers_lambda=lambda x: x, match_lambda=lambda x: True, update_lambda=lambda x: x):

        amendments = get_amendments_from_csv_as_dict(self.input_filename)

        self._read_and_update(amendments, headers_lambda(amendments[0]), match_lambda, update_lambda)

    def _read_and_update(self, amendments, csv_headers, match_lambda, update_lambda):
        with open(self.output_filename, newline='', mode='w+', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=csv_headers)
            writer.writeheader()
            for i, a in enumerate(amendments):
                print('{}/{}'.format(i + 1, len(amendments)))
                if match_lambda(a):
                    updated = update_lambda(a)
                    writer.writerow(updated)
                else:
                    writer.writerow(a)

    def test(self):
        return FindAndReplace('./tst.csv', 'tst.out.csv')


if __name__ == '__main__':
    def match(amendment):
        return True

    def update(amendment):
        amendment['URL'] = 'url'
        return amendment

    FindAndReplace("", "")\
        .test()\
        .find_and_replace(match, update)
