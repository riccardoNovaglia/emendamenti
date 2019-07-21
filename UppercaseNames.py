from find_and_replace import FindAndReplace

if __name__ == '__main__':
    def update(amendment):
        amendment['sponsor'] = ', '.join([name.title() for name in amendment['sponsor'].split(', ')])
        return amendment


    FindAndReplace(input_filename="./data/Chamber_amend_quadro_cicli.csv",
                   output_filename="./data/Chamber_amend_quadro_cicli_updated.csv") \
        .find_and_replace(update_lambda=update)
