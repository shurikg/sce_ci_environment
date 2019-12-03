# SCE CI Environment

## Introduction

This document describe the steps that should be done in order to create CI environment for academical course.

### Jenkins

The CI based on jenkins tools that will run as docker based on [official jenkins image](https://github.com/jenkinsci/docker/blob/master/README.md) and all the jenkins configuration done via [configuration as code plugin](https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/README.md).

This docker image contains:

* 150 student users
* 4 admin users
* student users split to 37 groups
* each group has different jenkins folder with correct permission
* Example folder that contains pipeline for java and python projects
* 10 master executors
* ability to run docker in docker

#### Getting Started

1. Docker installation

```sh
    sudo apt install docker.io
```

2. Local folder that will acting as volume to jenkins container

```sh
    mkdir sce_jenkins_home
```

> Important: the local docker group id should be align with created image.
>
> Validate what is the docker guid on the server and update the Dockerfile if needed

#### Jenkins Configuration files

| File                                   | Description                                             |
| -------------------------------------- |:--------------------------------------------------------|
| Dockerfile                             | define how to build the docker image                    |
| plugin.txt                             | list of jenkins plugins that will be installed in image |
| casc_config/casc.yaml                  | Create folders and examples jobs                        |
| casc_config/staff_users.yaml           | Create the staff users                                  |
| casc_config/student_users.yaml         | Create the jenkins users `student[1-150]`                |
| casc_config/student_group_mapping,yaml | Create 37 group and mapping student to it               |

#### Jenkins Usage

```sh
docker run -d --name scejenkins \
           -v sce_jenkins_home:/var/jenkins_home \
           -v /var/run/docker.sock:/var/run/docker.sock \
           -p 80:8080 -p 50000:50000 \
           shurikg/sce_jenkins:2.190.3
```

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
```
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
