# SCE Jenkins Environment

## Introduction

This document describes the steps that should be done to create a Jenkins environment for the academic course.

### Jenkins

The CI based on Jenkins tools that will run as a Docker container based on the [official Jenkins image](https://github.com/jenkinsci/docker/blob/master/README.md), and all the Jenkins configuration is done via the [Configuration as Code plugin](https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/README.md).

This Docker image contains:

* Jenkins version 2.387.1 (LTS)
* Relevant plugins for pipeline execution

The below configurations are defined via CasC:

* Admin users
* Student users
* Example pipelines for Python and Java
* Split users into groups
* Each group has a separate folder
* Permissions for users

#### Getting Started

1. Docker installation

    ```sh
        sudo apt install docker.io
    ```

    > Important: The local Docker group ID should be aligned with the created image.
    >
    > Validate what the Docker GUID is on the server and update the Dockerfile if needed.

2. The local folder that will be acting as volume to the Jenkins container

    ```sh
        mkdir sce_jenkins_home sce_jenkins_casc sce_jenkins_jobs
    ```

3. Create 2 CSV files

    * Admin users - jenkins_admin.csv

    ```csv
    user,full name
    admin,Administrator
    david.ben-gurion,David Ben-Gurion
    ```

    * Student users - jenkins_students.csv

    ```csv
    email,full name,tz,team_number
    dov.yosef@knesset.gov.il, Dov Yosef, 1234560, 1
    zalman.shazar@knesset.gov.il, Zalman Shazar, 1234561, 1
    moshe.sharett@knesset.gov.il, Moshe Sharett, 1234562, 1
    eliezer.kaplan@knesset.gov.il, Eliezer Kaplan, 1234563, 2
    golda.meir@knesset.gov.il, Golda Meir, 1234564, 2
    david.remez@knesset.gov.il, David Remez, 1234565, 2
    pinchas.rosen@knesset.gov.il, Pinchas Rosen, 1234566, 3
    bechor-shalom.sheetrit@knesset.gov.il, Bechor-Shalom Sheetrit, 1234567, 3
    haim-moshe.shapira@knesset.gov.il, Haim-Moshe Shapira, 1234568, 4
    yehuda.leib-maimon@knesset.gov.il, Yehuda Leib Maimon, 1234569, 4
    yitzhak-meir.levin@knsesset.gov.il, Yitzhak-Meir Levin. 1234570, 4
    ```

4. Install python dependency

    ```sh
        pip install -r requirements.txt
    ```

5. Run CasC preparation script

    ```sh
        python3 sce_jenkins_preparation.py --admin_password knesset1 \
                                            --staff_csv input_example/jenkins_admin.csv \
                                            --student_csv input_example/jenkins_students.csv \
                                            --output_folder sce_jenkins_casc
    ```

6. Run jenkins

    ```sh
        docker run -d --name sce_jenkins_2023 \
           -v <full_path>/sce_jenkins_home:/var/jenkins_home \
           -v /var/run/docker.sock:/var/run/docker.sock \
           -v <full_path>/sce_jenkins_casc:/var/jenkins_home/sce_casc/ \
           -v <full_path>/sce_jenkins_jobs:/var/jenkins_home/jobs/ \
           -p 80:8080 -p 50000:50000 \
           --restart=on-failure \
           shurikg/sce_jenkins:2.387.1
    ```

    > Note: In the volume parameter provide the full path to the relevant folder
