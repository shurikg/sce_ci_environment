pipelineJob('Examples/Python-Example') {
    description('Java/Maven example job. Reference - https://github.com/shurikg/simple-python-pyinstaller-app')
    definition {
        cpsScm {
            scriptPath 'jenkins/Jenkinsfile'
            scm {
                git {
                    remote { url 'https://github.com/shurikg/simple-python-pyinstaller-app.git' }
                    branch '*/master'
                    extensions {}
                }
            }
        }
    }
}