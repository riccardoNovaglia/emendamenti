from find_and_replace import FindAndReplace

if __name__ == '__main__':

    def match(amendment):
        return amendment['ESITO'] == "Parzialmente recluso"


    def update(amendment):
        amendment['ESITO'] = "Parzialmente precluso"
        return amendment


    FindAndReplace(input_filename="./14_esito.csv", output_filename="./14_precluso_2.csv") \
        .find_and_replace(match, update)
