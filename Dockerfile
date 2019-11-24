FROM jenkins/jenkins:2.190.3

LABEL maintainer="shurikg" 

USER root
# Install the latest Docker CE binaries and add user `jenkins` to the docker group
RUN apt-get update && \
    apt-get -y install apt-transport-https \
      ca-certificates \
      curl \
      gnupg2 \
      software-properties-common && \
    curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg > /tmp/dkey; apt-key add /tmp/dkey && \
    add-apt-repository \
      "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
      $(lsb_release -cs) \
      stable" && \
   apt-get update && \
   apt-get -y install docker-ce && \
   groupadd -f -g 114 scedocker && \ 
   usermod -aG docker jenkins && \
   usermod -aG scedocker jenkins

USER jenkins

ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt

COPY casc_config/ /usr/share/jenkins/ref/

ENV CASC_JENKINS_CONFIG /usr/share/jenkins/ref/ 

VOLUME [ "/var/jenkins_home" ]
