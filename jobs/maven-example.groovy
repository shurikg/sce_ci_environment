pipelineJob('Examples/Maven-Example') {
    description('Java/Maven example job. Reference - https://github.com/jenkins-docs/simple-java-maven-app')
    definition {
        cpsScm {
            scriptPath 'jenkins/Jenkinsfile'
            scm {
            git {
                remote { url 'https://github.com/jenkins-docs/simple-java-maven-app.git' }
                branch '*/master'
                extensions {}
            }
            }
        }
    }
}