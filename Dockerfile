FROM jenkins/jenkins:2.190.3

ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt

COPY casc_config/ /usr/share/jenkins/ref/

ENV CASC_JENKINS_CONFIG /usr/share/jenkins/ref/
