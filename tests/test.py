# DO NOT MODIFY this script
import csv
import unittest
from tempfile import TemporaryDirectory
from csv import reader, writer
import os
import sys
sys.path.append(os.path.realpath("code/"))
from script import covid_vaccine


def read_output_file(output_file):
    if not os.path.isfile(output_file):
        raise FileNotFoundError("File {output_file} doesn't exist".format(output_file=output_file))
    data = {}
    num_rows = 0
    with open(output_file) as ifh:
        #skip header
        next(ifh)
        csv_reader = reader(ifh, delimiter="\t")
        for row in csv_reader:
            #City State Vaccine Gender Users
            if len(row) != 5:
                raise Exception("Output file expected to have only 5 columns, {size} found!".format(size=len(row)))
            city, state, vaccine, gender, users = row
            state_dict = data.get(city, {})
            vaccine_dict = state_dict.get(state, {})
            gender_dict = vaccine_dict.get(vaccine, {})
            gender_dict[gender] = int(users.strip())
            vaccine_dict[vaccine] =  gender_dict
            state_dict[state] = vaccine_dict
            data[city] = state_dict
            num_rows += 1
    return data, num_rows
     

class TestCovidVaccine(unittest.TestCase):

    def test_single_file(self):
        with TemporaryDirectory() as tmp_dir:
            dir_path = tmp_dir
            vaccine_path = os.path.join(dir_path, "vaccination_status")
            if not os.path.exists(vaccine_path):
                os.mkdir(vaccine_path)
            input_file_path = os.path.join(vaccine_path, "input_file.tsv")
            with open(input_file_path, "w") as ifh:
                csv_writer = writer(ifh, delimiter="\t")
                csv_writer.writerow(["user", "vaccine", "date"])
                csv_writer.writerows([["9297629", "C","29-11-2020"],
                                        ["5054692", "B","08-07-2021"],
                                        ["1348029", "A","14-08-2021"],
                                        ["8089418", "A","03-01-2021"],
                                        ["1793913", "B","23-08-2020"],
                                        ["1423551", "B","21-06-2020"],
                                        ["6744398", "B","16-06-2020"],
                                        ["6744397", "B","14-06-2020"],
                                        ["6893959", "A","28-07-2021"],
                                        ["7137362", "C","29-01-2021"],
                                        ["1754454", "C","01-01-1970"],
                                        ["9297629", "C","03-03-2021"],
                                        ["1545454", "Z","01-04-2020"]])
            user_info_path = os.path.join(dir_path, "user_meta.tsv")
            with open(user_info_path, "w") as ofh:
                csv_writer = writer(ofh, delimiter="\t")
                csv_writer.writerow(["user", "gender", "city", "state"])
                csv_writer.writerows([
                                    ["8089418", "F", "Bahraigh", "Uttar Pradesh"],
                                    ["6893959", "M", "Hyderabad", "Telangana"],
                                    ["6744398", "M", "Sonipat", "Haryana"],
                                    ["6744397", "M", "Sonipat", "Haryana"],
                                    ["1348029", "M", "Vishakhapatnam", "Andhra Pradesh"],
                                    ["1793913", "M", "Bhiwandi", "Maharashtra"],
                                    ["1423551", "F", "Raipur", "Chhattisgarh"],
                                    ["9297629", "F", "Chennai", "Tamil Nadu"],
                                    ["5054692", "F", "Chennai", "Tamil Nadu"],
                                    ["7137362", "M", "Gurgaon", "Haryana"],
                                    ["1754454", "M", "Mangalore", "Karnataka"],
                                    ["1545454", "F", "Chennai", "Tamil Nadu"]])
            output_file_path = os.path.join(dir_path, "output_file")
            covid_vaccine([input_file_path], user_info_path , output_file_path)
            data, num_rows = read_output_file(output_file_path)
            expected_results = {"Bahraigh" : {"Uttar Pradesh" : {"A" : {"F" : 1}}},
                                "Bhiwandi" : {"Maharashtra" : {"B" : {"M" : 1}}},
                                "Chennai" : {"Tamil Nadu" : {"B" : {"F" : 1}, "C" : {"F" : 1}}},
                                "Gurgaon" : {"Haryana" : {"C" : {"M" : 1}}},
                                "Hyderabad" : {"Telangana" : {"A" : {"M" : 1}}},
                                "Raipur" : {"Chhattisgarh" : {"B" : {"F" : 1}}},
                                "Sonipat" : {"Haryana" : {"B" : {"M" : 2}}},
                                "Vishakhapatnam" : {"Andhra Pradesh" : {"A" : {"M" : 1}}}
            }
            self.assertEqual(data, expected_results)


    def test_empty_input_file(self):
        with TemporaryDirectory() as tmp_dir:
            dir_path = tmp_dir
            vaccine_path = os.path.join(dir_path, "vaccination_status")
            if not os.path.exists(vaccine_path):
                os.mkdir(vaccine_path)
            input_file_path = os.path.join(vaccine_path, "input_file.tsv")
            with open(input_file_path, "w") as ifh:
                csv_writer = writer(ifh, delimiter="\t")
                csv_writer.writerow(["user", "vaccine", "date"])
            user_info_path = os.path.join(dir_path, "user_meta.tsv")
            with open(user_info_path, "w") as ofh:
                csv_writer = writer(ofh, delimiter="\t")
                csv_writer.writerow(["user", "gender", "city", "state"])
            output_file_path = os.path.join(dir_path, "output_file")
            covid_vaccine([input_file_path], user_info_path , output_file_path)
            data, num_rows = read_output_file(output_file_path)
            expected_results = {}
            self.assertEqual(data, expected_results)


    def test_multiple_input_file(self):
        with TemporaryDirectory() as tmp_dir:
            dir_path = tmp_dir
            vaccine_path = os.path.join(dir_path, "vaccination_status")
            if not os.path.exists(vaccine_path):
                os.mkdir(vaccine_path)
            input_file_path_one = os.path.join(vaccine_path, "input_file_one.tsv")
            with open(input_file_path_one, "w") as ifh:
                csv_writer = writer(ifh, delimiter="\t")
                csv_writer.writerow(["user", "vaccine", "date"])
                csv_writer.writerows([["9297629", "C","29-11-2020"],
                                        ["5054692", "B","08-07-2021"],
                                        ["1348029", "A","14-08-2021"],
                                        ["8089418", "A","03-01-2021"],
                                        ["1793913", "B","23-08-2020"],
                                        ["1423551", "B","21-06-2020"],
                                        ["6744398", "B","16-06-2020"],
                                        ["6744397", "B","14-06-2020"],
                                        ["6893959", "A","28-07-2021"],
                                        ["7137362", "C","29-01-2021"]])
            input_file_path_two = os.path.join(vaccine_path, "input_file_two.tsv")
            with open(input_file_path_two, "w") as ifh:
                csv_writer = writer(ifh, delimiter="\t")
                csv_writer.writerow(["user", "vaccine", "date"])
                csv_writer.writerows([["1754454", "C","01-01-1970"],
                                        ["9297629", "C","03-03-2021"],
                                        ["1545454", "Z","01-04-2020"]])
            user_info_path = os.path.join(dir_path, "user_meta.tsv")
            with open(user_info_path, "w") as ofh:
                csv_writer = writer(ofh, delimiter="\t")
                csv_writer.writerow(["user", "gender", "city", "state"])
                csv_writer.writerows([
                                    ["8089418", "F", "Bahraigh", "Uttar Pradesh"],
                                    ["6893959", "M", "Hyderabad", "Telangana"],
                                    ["6744398", "M", "Sonipat", "Haryana"],
                                    ["6744397", "M", "Sonipat", "Haryana"],
                                    ["1348029", "M", "Vishakhapatnam", "Andhra Pradesh"],
                                    ["1793913", "M", "Bhiwandi", "Maharashtra"],
                                    ["1423551", "F", "Raipur", "Chhattisgarh"],
                                    ["9297629", "F", "Chennai", "Tamil Nadu"],
                                    ["5054692", "F", "Chennai", "Tamil Nadu"],
                                    ["7137362", "M", "Gurgaon", "Haryana"],
                                    ["1754454", "M", "Mangalore", "Karnataka"],
                                    ["1545454", "F", "Chennai", "Tamil Nadu"]])
            output_file_path = os.path.join(dir_path, "output_file")
            covid_vaccine([input_file_path_one, input_file_path_two], user_info_path , output_file_path)
            data, num_rows = read_output_file(output_file_path)
            expected_results = {"Bahraigh" : {"Uttar Pradesh" : {"A" : {"F" : 1}}},
                                "Bhiwandi" : {"Maharashtra" : {"B" : {"M" : 1}}},
                                "Chennai" : {"Tamil Nadu" : {"B" : {"F" : 1}, "C" : {"F" : 1}}},
                                "Gurgaon" : {"Haryana" : {"C" : {"M" : 1}}},
                                "Hyderabad" : {"Telangana" : {"A" : {"M" : 1}}},
                                "Raipur" : {"Chhattisgarh" : {"B" : {"F" : 1}}},
                                "Sonipat" : {"Haryana" : {"B" : {"M" : 2}}},
                                "Vishakhapatnam" : {"Andhra Pradesh" : {"A" : {"M" : 1}}}
            }
            self.assertEqual(data, expected_results)


if __name__ == "__main__":
    unittest.main()
    
    



