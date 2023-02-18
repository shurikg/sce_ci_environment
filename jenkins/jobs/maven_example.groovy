pipelineJob('Examples/Maven-Example') {
    description('Java/Maven example job. Reference - https://github.com/jenkins-docs/simple-java-maven-app')
    definition {
        cpsScm {
            scriptPath 'jenkins/Jenkinsfile'
            scm {
                git {
                    remote { url 'https://github.com/jenkins-docs/simple-java-maven-app.git' }
                    branch '5a7366036f04c2b7c0d5f36f045e00056b2ede86'
                    extensions {}
                }
            }
        }
    }
}