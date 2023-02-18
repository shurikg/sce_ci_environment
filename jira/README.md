# SCE CI Environment

# Deprecated - DON'T USE IT

## Introduction

This document describe the steps that should be done in order to create CI environment for academical course.


### Jira

We are using Jira as product manager tool. In order to prepare the Jira for course the below script do the below steps:

* create student users
* create group and assign relevant users to it
* create project for each group
* create permission schema that give permission only for team group and not to everyone
* assign the correct permission schema to project

#### Jira Configuration files

The jira script require input configuration file.
The configuration file in csv format.

The csv file format:

```csv
full name,tz,email,project_key,project_name
```

* `full name` - the student full name
* `tz` - student id (teudat zeut), it's also the default password
* `email` - the student e-mail address
* `project_key` - the jira project key, can be only [A-Z0-9] character
* `project_name` - the jira project name

Example:

```csv
full name,tz,email,project_key,project_name
Dummy User 1,12345, dummy1@gmail.com, PM2020T1, PM2020_TEAM_1
Dummy User 2,54321, dummy2@gmail.com, PM2020T1, PM2020_TEAM_1
Dummy User 3,54321, dummy3@gmail.com, PM2020T2, PM2020_TEAM_2
```

#### Jira Usage

```sh
sce_jira_preperation.py --url http://jira:8080 \
                        --jira_user dummy1 \
                        --jira_password 12345 \
                        --input_file jira_example_input.csv
```
