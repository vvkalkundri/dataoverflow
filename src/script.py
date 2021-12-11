import csv
import os
from datetime import datetime
from csv import DictWriter

import dask.dataframe as dd


def covid_vaccine(vaccination_status_files, user_meta_file, output_file):
    """This function takes  vaccination_status_files and user_meta_file paths
    using this all the covid vaccination numbers needs to be stored in the given output file as TSV
    Args:
        vaccination_status_files: A List containing file path to the TSV vaccination_status_file.
        user_meta_file: A file path to TSV file containing User information.
        output_file: File path where output TSV results are should be stored, 
    Returns:
      None (doesnt return anything)
    """
    # your code goes here.
    #  feel free to modify this entire script, except this function signature.
    date_start, date_end = datetime(2020, 2, 1), datetime(2021, 11, 30)
    user_data_df = dd.read_csv(user_meta_file , sep='	', header=0)
    for vaccination_file in vaccination_status_files:
        file_name = dd.read_csv(vaccination_file , sep='	', header=0)
        result = dd.merge(user_data_df, file_name, on='user', how='inner', indicator=True)
    user_data = dict()
    for index, row in result.iterrows():
        year = int(datetime.strptime(row['date'], "%d-%M-%Y").strftime('%Y'))
        month = int(datetime.strptime(row['date'], "%d-%M-%Y").strftime('%M'))
        day = int(datetime.strptime(row['date'], "%d-%M-%Y").strftime('%d'))
        res = datetime(year, month, day) >= date_start and datetime(2020, 3, 1) <= date_end
        if row['_merge'] == 'both' and res and row['vaccine'] in ['A', 'B', 'C'] and row['gender'] in ['M', 'F']:
            state = row['state']
            city = row['city']
            vaccine = row['vaccine']
            gender = row['gender']
            if state not in user_data:
                user_data[state] = dict()
            if city not in user_data[state]:
                user_data[state][city] = dict()
            if vaccine not in user_data[state][city]:
                user_data[state][city][vaccine] = dict()
            if gender not in user_data[state][city][vaccine]:
                user_data[state][city][vaccine][gender] = dict()
                user_data[state][city][vaccine][gender] = 0
            user_data[state][city][vaccine][gender] = user_data[state][city][vaccine][gender] + 1
    for state, city in user_data.items():
        for city, vaccine in city.items():
            for vaccine, gender in vaccine.items():
                for gender, count in gender.items():
                    with open(output_file, 'a+', newline='') as write_obj:
                        field_name = ['state', 'city', 'vaccine', 'gender', 'unique_vaccinated_people']
                        csv_writer = DictWriter(write_obj, fieldnames=field_name)
                        row_dict = {'state': state, 'city': city, 'vaccine': vaccine, 'gender': gender,
                                    'unique_vaccinated_people': count
                                    }
                        csv_writer.writerow(row_dict)


if __name__ == '__main__':
    parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    vaccination_file_path = [parent_directory + '/data/vaccination_status/' + 'vaccination_status_*.tsv']
    user_information_file_path = parent_directory + '/data/'.strip() + 'user_*tsv'
    output_file = 'output.tsv'
    covid_vaccine(vaccination_file_path, user_information_file_path, output_file)
