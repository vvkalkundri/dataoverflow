# DO NOT MODIFY this script
from src.script import covid_vaccine
from argparse import ArgumentParser
from tests.test import TestCovidVaccine
import os
import unittest
import sys

def file_check(file_path):
    if os.path.isfile(file_path):
        return file_path
    raise FileNotFoundError("File {file_path} is not found".format(file_path=file_path))


def main():
    parser = ArgumentParser(description="This script is a wrapper which runs/tests the covid vaccine code")
    subparsers = parser.add_subparsers(help="sub-commands available", dest="mode")
    subparsers.required = True
    parser_run = subparsers.add_parser("run", help="Use this subcommand to run the program")
    parser_test = subparsers.add_parser("test", help="Use this subcommand to test the program")
    parser_run.add_argument("-v", "--vaccination_files", required=True, nargs="+", type=file_check, help="Path to the vaccination status TSV files")
    parser_run.add_argument("-u", "--user_meta_file", required=True, type=file_check, help="Path to TSV user information file")
    parser_run.add_argument("-o", "--output_file", required=True, help="Path to the TSV ouput file")
    args = parser.parse_args()
    if args.mode == "run":
        covid_vaccine(args.vaccination_files, args.user_meta_file, args.output_file)
    else:
        suite = unittest.TestSuite()
        suite.addTests(unittest.makeSuite(TestCovidVaccine))
        test_runner = unittest.TextTestRunner(verbosity=2).run(suite)
        if not test_runner.wasSuccessful():
            sys.exit(2)


if __name__ == "__main__":
    main()
