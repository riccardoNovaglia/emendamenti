from find_and_replace import FindAndReplace

if __name__ == '__main__':
    def match(amendment):
        return amendment['Esito'] == "approvato" \
               and amendment['Firmatari'].isspace() \
               and '0' in amendment['Numero emendamento']


    def update(amendment):
        amendment['Firmatari'] = "Rapporteur"
        return amendment


    FindAndReplace(input_filename="./data/camera_and_parties/all_leg.csv",
                   output_filename="./data/camera_and_parties/all_leg_with_rapporteur.csv") \
        .find_and_replace(match, update)
