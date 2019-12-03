#!/usr/bin/python3

import argparse
import requests
import base64
import pandas as pd

CSV_FULL_NAME_COLUMN = "full name"
CSV_TZ_COLUMN = "tz"
CSV_EMAIL_COLUMN = "email"
CSV_PROJECT_KEY_COLUMN = "project_key"
CSV_PROJECT_NAME_COLUMN = "project_name"
CSV_GROUP_NAME_COLUMN = "group_name"

PERMISSION_SCHEMA_OPTIONS = [
    "BROWSE_PROJECTS", "CREATE_ISSUES", "EDIT_ISSUES", "ASSIGN_ISSUES", "RESOLVE_ISSUES", "ADD_COMMENTS", "DELETE_ISSUES",
    "ASSIGNABLE_USER", "CLOSE_ISSUES", "CREATE_ATTACHMENTS", "WORK_ON_ISSUES", "LINK_ISSUES", "ADMINISTER_PROJECTS", "MOVE_ISSUES",
    "SCHEDULE_ISSUES", "MODIFY_REPORTER", "VIEW_VOTERS_AND_WATCHERS", "MANAGE_WATCHERS", "EDIT_ALL_COMMENTS", "EDIT_OWN_COMMENTS",
    "DELETE_ALL_COMMENTS", "DELETE_OWN_COMMENTS", "DELETE_ALL_ATTACHMENTS", "DELETE_OWN_ATTACHMENTS", "EDIT_OWN_WORKLOGS",
    "EDIT_ALL_WORKLOGS", "DELETE_OWN_WORKLOGS", "DELETE_ALL_WORKLOGS", "VIEW_READONLY_WORKFLOW", "TRANSITION_ISSUES",
    "VIEW_DEV_TOOLS", "MANAGE_SPRINTS_PERMISSION"
]
PERMISSION_ADMIN_ROLE = 10002


def main():
    args = script_parameters()
    api_authorization = base64.b64encode(("{}:{}".format(args.jira_user,args.jira_password).encode())).decode()
    auth_header = { 'Authorization': "Basic {}".format(api_authorization) }

    create_student_users(args, auth_header)
    create_groups(args, auth_header)
    assign_users_to_group(args, auth_header)

    create_permission_schema_for_project(args, auth_header)
    create_projects(args,auth_header)

def script_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--jira_url", help="jira url", action="store", required=True)
    parser.add_argument("-ju", "--jira_user", help="jira user", action="store", required=True)
    parser.add_argument("-jp", "--jira_password", help="jira password", action="store", required=True)
    parser.add_argument("-i", "--input_file", help="input file", action="store", required=True)
    args = parser.parse_args()

    return args

def create_student_users(args, auth_header):
    api_url = "{0}/rest/api/2/user".format(args.jira_url)
    api_headers = { 'Content-Type': 'application/json' }
    api_headers.update(auth_header)

    df = pd.read_csv(args.input_file)
    for _, row in df.astype(str).iterrows():
        user_name = row[CSV_EMAIL_COLUMN].strip().split('@')[0]

        print("Checking if [{}] user exists".format(user_name))
        if is_user_exists(args, auth_header, user_name):
            print("User already exists")
            continue

        print("Create [{}] user".format(user_name))
        payload = { "name": user_name,
                    "password": row[CSV_TZ_COLUMN].strip(),
                    "emailAddress": row[CSV_EMAIL_COLUMN].strip(),
                    "displayName": row[CSV_FULL_NAME_COLUMN].strip()
               }

        response = requests.request("POST", api_url, headers=api_headers, json=payload)

        if response.status_code != 201:
            print("Failed to create user {}".format(response.text))
            continue

        print("User created successfully")

def create_projects(args, auth_header):
    api_url = "{0}/rest/api/2/project".format(args.jira_url)
    api_headers = { 'Content-Type': 'application/json' }
    api_headers.update(auth_header)

    df = pd.read_csv(args.input_file)
    for _, row in df.astype(str).iterrows():
        print("Checking if [{}] project exists".format(row[CSV_PROJECT_KEY_COLUMN].strip()))
        if is_project_exists(args, auth_header, row[CSV_PROJECT_KEY_COLUMN].strip()):
            print("Project already exists")
            continue

        print("Create [{}] project".format(row[CSV_PROJECT_KEY_COLUMN].strip()))
        payload = { "key": row[CSV_PROJECT_KEY_COLUMN].strip(),
                    "name": row[CSV_PROJECT_NAME_COLUMN].strip(),
                    "projectTypeKey": "software",
                    "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-scrum-template",
                    "permissionScheme": get_permission_schema_id(args,auth_header,"{}_PS".format(row[CSV_PROJECT_KEY_COLUMN].strip())),
                    "lead": args.jira_user
                    }

        response = requests.request("POST", api_url, headers=api_headers, json=payload)

        if response.status_code != 201:
            print("Failed to create project {}".format(response.text))
            continue

        print("Project created successfully")

def create_groups(args, auth_header):
    api_url = "{0}/rest/api/2/group".format(args.jira_url)
    api_headers = { 'Content-Type': 'application/json' }
    api_headers.update(auth_header)

    df = pd.read_csv(args.input_file)
    for current_project_key in df[CSV_PROJECT_KEY_COLUMN].astype(str).unique().tolist():
        current_group_name = "{}_GROUP".format(current_project_key.strip())
        print("Create [{}] group".format(current_group_name))
        payload = { "name": current_group_name }

        response = requests.request("POST", api_url, headers=api_headers, json=payload)

        if response.status_code != 201 and response.status_code != 400:
            print("Failed to create group {}".format(response.text))
            continue

        print("Group created successfully")


def assign_users_to_group(args, auth_header):
    api_url = "{0}/rest/api/2/group/user".format(args.jira_url)
    api_headers = { 'Content-Type': 'application/json' }
    api_headers.update(auth_header)

    df = pd.read_csv(args.input_file)
    for _, row in df.astype(str).iterrows():
        current_user = row[CSV_EMAIL_COLUMN].strip().split('@')[0]
        current_group_name = "{}_GROUP".format(row[CSV_PROJECT_KEY_COLUMN].strip())
        current_api_url = "{}?groupname={}".format(api_url,current_group_name)
        print("Assign [{}] user to [{}] group".format(current_user,current_group_name))

        payload = { "name": current_user }

        response = requests.request("POST", current_api_url, headers=api_headers, json=payload)

        if response.status_code != 201 and response.status_code != 400:
            print("Failed to add user to group {}".format(response.text))
            continue

        print("User added successfully to group")

def create_permission_schema_for_project(args, auth_header):
    api_url = "{0}/rest/api/2/permissionscheme".format(args.jira_url)
    api_headers = { 'Content-Type': 'application/json' }
    api_headers.update(auth_header)

    df = pd.read_csv(args.input_file)
    for current_project_key in df[CSV_PROJECT_KEY_COLUMN].astype(str).unique().tolist():
        current_group_name = "{}_GROUP".format(current_project_key.strip())
        current_permission_schema_name = "{}_PS".format(current_project_key.strip())

        print("Checking if [{}] permission schema exist".format(current_permission_schema_name))
        if is_permission_schema_exists(args,auth_header,current_permission_schema_name):
            print("Permission schema exists")
            continue

        print("Create [{}] permission set".format(current_permission_schema_name))
        payload = {
            "name": current_permission_schema_name,
            "permissions": []
        }

        for current_permission_type in PERMISSION_SCHEMA_OPTIONS:
            payload["permissions"].append(
                {
                    "holder": {
                        "type": "group",
                        "parameter": current_group_name
                    },
                    "permission": current_permission_type
                })
            payload["permissions"].append(
                {
                    "holder": {
                        "type": "projectRole",
                        "parameter": PERMISSION_ADMIN_ROLE
                    },
                    "permission": current_permission_type
                })

        response = requests.request("POST", api_url, headers=api_headers, json=payload)

        if response.status_code != 201 and response.status_code != 400:
            print("Failed to create permission schema {} code {}".format(response.text, response.status_code))
            continue

        print("Permission schema created successfully")

def is_user_exists(args, auth_header, user_name):
    api_url = "{0}/rest/api/2/user?username={1}".format(args.jira_url, user_name)

    response = requests.request("GET", api_url, headers=auth_header)
    if response.status_code == 200:
        return True

    if response.status_code == 404:
        return False

    raise Exception("Failed to check if user exists ${0}".format(response.text))

def is_project_exists(args, auth_header, project_name):
    api_url = "{0}/rest/api/2/project/{1}".format(args.jira_url, project_name)

    response = requests.request("GET", api_url, headers=auth_header)
    if response.status_code == 200:
        return True

    if response.status_code == 404:
        return False

    raise Exception("Failed to check if project exists ${0}".format(response.text))

def is_permission_schema_exists(args, auth_header, permission_scheme_name):

    permission_id = get_permission_schema_id(args, auth_header, permission_scheme_name)
    api_url = "{0}/rest/api/2/permissionscheme/{1}".format(args.jira_url, permission_id)

    response = requests.request("GET", api_url, headers=auth_header)
    if response.status_code == 200:
        return True

    if response.status_code == 404:
        return False

    raise Exception("Failed to check if permission schema exists ${0}".format(response.text))

def get_permission_schema_id(args, auth_header, permission_scheme_name):
    api_url = "{0}/rest/api/2/permissionscheme/".format(args.jira_url)

    response = requests.request("GET", api_url, headers=auth_header)
    for current_ps in response.json()["permissionSchemes"]:
        if current_ps["name"] == permission_scheme_name:
            return current_ps["id"]

    return None


main()