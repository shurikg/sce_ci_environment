# SCE CI Environemnt (Jenkins)

## Introduction

This document describe the steps that should be done in order to create CI environment for academical course.

The CI based on jenkins tools that will run as docker based on [official jenkins image](https://github.com/jenkinsci/docker/blob/master/README.md) and all the jenkins configuration done via [configuration as code plugin](https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/README.md).

This docker image contains:

* 90 student users
* 4 admin users
* student users splited to 22 groups
* each group has different jenkins folder with correct permission
* Example folder that contains pipeline for java and python projects
* 10 master executors
* ability to run docker in docker

## Getting Started

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

## Configuration files

| File                                   | Description                                             |
| -------------------------------------- |:--------------------------------------------------------|
| Dockerfile                             | define how to build the docker image                    |
| plugin.txt                             | list of jenkins plugins that will be installed in image |
| casc_config/casc.yaml                  | Create folders and examples jobs                        |
| casc_config/staff_users.yaml           | Create the staff users                                  |
| casc_config/student_users.yaml         | Create the jenkins users `student[1-90]`                |
| casc_config/student_group_mapping,yaml | Create 22 group and mapping student to it               |

## Usage

```sh
docker run -d --name scejenkins \
           -v sce_jenkins_home:/var/jenkins_home \
           -v /var/run/docker.sock:/var/run/docker.sock \
           -p 80:8080 -p 50000:50000 \
           shurikg/sce_jenkins:2.190.3
```
