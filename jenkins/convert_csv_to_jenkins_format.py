#!/usr/bin/python3

import argparse
import csv
import yaml
import os
import subprocess

ROOT_PATH = os.path.realpath(os.path.dirname(__file__))

def main():
    args = script_parameters()


    convert_csv(args)


def script_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_csv",
                        help="input csv file", action="store", required=True)
    parser.add_argument("-o", "--output_csv",
                        help="output csv file", action="store", required=True)
    args = parser.parse_args()

    return args


def convert_csv(args):

    data = [['email','full name','tz','team_number']]

    with open(args.input_csv, 'r',encoding='utf-8') as file:
        reader = csv.reader(file)
        _ = next(reader)

        for current_user in reader:
            data.append([current_user[3],current_user[2],current_user[1],current_user[13]])
            data.append([current_user[6],current_user[5],current_user[4],current_user[13]])
            data.append([current_user[9],current_user[8],current_user[7],current_user[13]])
            data.append([current_user[12],current_user[11],current_user[10],current_user[13]])


    with open(args.output_csv, mode='w',encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

    with open(args.output_csv, 'r',encoding='utf-8', newline='') as file:
        reader = csv.reader(file)

        for current_user in reader:
            print(current_user)

main()
