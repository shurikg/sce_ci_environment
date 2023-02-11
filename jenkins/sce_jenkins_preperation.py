#!/usr/bin/python3

import argparse
import csv
import yaml
import os

ROOT_PATH = os.path.realpath(os.path.dirname(__file__))

def main():
    args = script_parameters()

    create_admin_users(args)
    create_student_users(args)
    role_assignment(args)
    create_team_folders(args)
    general_configuration(args)
    create_jobs(args)

def script_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ap", "--admin_password",
                        help="admin password", action="store", required=True)
    parser.add_argument("-o", "--output_folder",
                        help="output folder", action="store", required=True)
    parser.add_argument("-s", "--student_csv",
                        help="student csv file", action="store", required=True)
    parser.add_argument("-st", "--staff_csv",
                        help="staff csv file", action="store", required=True)
    args = parser.parse_args()

    return args


def create_admin_users(args):
    casc_data = {"jenkins": {"securityRealm": {
        "local": {"allowsSignup": "false", "users": []}}}}

    with open(args.staff_csv, 'r') as file:
        reader = csv.reader(file)
        _ = next(reader)

        for current_user in reader:
            casc_data["jenkins"]["securityRealm"]["local"]["users"].append(
                {"id": current_user[0], "name": current_user[1], "password": args.admin_password})

    with open(f"{args.output_folder}/admin.yaml", 'w') as file:
        yaml.dump(casc_data, file)

def create_student_users(args):
    casc_data = {"jenkins": {"securityRealm": {
        "local": {"users": []}}}}

    with open(args.student_csv, 'r') as file:
        reader = csv.reader(file)
        _ = next(reader)

        # CSV header - email,full name,tz,team_number
        for current_user in reader:
            casc_data["jenkins"]["securityRealm"]["local"]["users"].append(
                {"id": current_user[0].split('@')[0], "name": current_user[1], "password": current_user[2], "properties": [{"mailer": {"emailAddress": current_user[0]}}]})

    with open(f"{args.output_folder}/student_user.yaml", 'w') as file:
        yaml.dump(casc_data, file)

def role_assignment(args):
    casc_data = {"jenkins": {"authorizationStrategy": {"roleBased": {"roles": {"global":[], "items": []}}}}}
    student_permission = [
                            "Job/Move","Job/Build","Credentials/Delete","Job/Create","Credentials/ManageDomains","Job/Discover","Job/Read",
                            "Credentials/View","Credentials/Update","Run/Replay","Run/Delete","Job/Cancel","Run/Update","Job/Delete","Credentials/Create",
                            "Job/Configure","Job/Workspace"
                        ]

    with open(args.staff_csv, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)

        admin_users = []
        for current_user in reader:
            admin_users.append(current_user[0])

        casc_data["jenkins"]["authorizationStrategy"]["roleBased"]["roles"]["global"].append(
                {"assignments": admin_users, "name": "admin", "pattern": ".*", "permissions": ["Overall/Administer"]})

        student_teams, students_id = get_team_users(args)
        for current_team in student_teams:
            casc_data["jenkins"]["authorizationStrategy"]["roleBased"]["roles"]["global"].append(
                {"assignments": student_teams[current_team], "name": current_team, "pattern": ".*", "permissions": ["Overall/Read"]})
            casc_data["jenkins"]["authorizationStrategy"]["roleBased"]["roles"]["items"].append(
                {"assignments": list(student_teams[current_team]), "name": current_team, "pattern": f"^{current_team}/.*|{current_team}", "permissions": list(student_permission)})

        casc_data["jenkins"]["authorizationStrategy"]["roleBased"]["roles"]["items"].append(
            {"assignments": list(students_id), "name": f"Examples", "pattern": "^Examples/.*|Examples", "permissions": ["Job/Read", "Job/ExtendedRead"]})


    with open(f"{args.output_folder}/role_mapping.yaml", 'w') as file:
        yaml.dump(casc_data, file)

def get_team_users(args):
    """_summary_

    Args:
        args (_type_): _description_

    Returns:
        dict: key is team name and value is the list of students id
    """
    team_mapping = {}
    students_id = []
    with open(args.student_csv, 'r') as file:
        reader = csv.reader(file)
        _ = next(reader)

        # CSV header - email,full name,tz,team_number
        for current_user in reader:
            current_key = f"Team-{current_user[3]}"
            current_user_id = current_user[0].split('@')[0]
            students_id.append(current_user_id)
            if current_key in team_mapping:
                team_mapping[current_key].append(current_user_id)
            else:
                team_mapping[current_key] = [current_user_id]

    return team_mapping, students_id

def create_team_folders(args):
    folder_names = list(get_team_users(args)[0].keys())
    folder_names.append("Examples")

    with open(f"{ROOT_PATH}/casc_templates/create_folders.groovy", 'r') as file:
        template = file.readlines()

    for i, line in enumerate(template):
        if 'def folderNames = TEMPLATE' in line:
            template[i] = f'        def folderNames = {folder_names};\n'

    with open(f"{args.output_folder}/folders.yaml", 'w') as file:
        file.writelines(template)

def create_jobs(args):
    with open(f"{ROOT_PATH}/casc_templates/jobs.yaml", 'r') as file:
        template = file.readlines()

    with open(f"{args.output_folder}/jobs.yaml", 'w') as file:
        file.writelines(template)

def general_configuration(args):
    with open(f"{ROOT_PATH}/casc_templates/general.yaml", 'r') as file:
        template = file.readlines()

    with open(f"{args.output_folder}/general.yaml", 'w') as file:
        file.writelines(template)

main()
