from find_and_replace import FindAndReplace

if __name__ == '__main__':
    def update(amendment):
        amendment['sponsor'] = ', '.join([name.title() for name in amendment['sponsor'].split(', ')])
        return amendment


    FindAndReplace(input_filename="./data/Senate_amend_legge_quadro_cicli_with_parties.csv",
                   output_filename="./data/Senate_amend_legge_quadro_cicli_with_parties.csv") \
        .find_and_replace(update_lambda=update)
