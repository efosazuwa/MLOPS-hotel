pipeline{
    agent any

    environment {
        VENV_DIR = '.venv'
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/efosazuwa/MLOPS-hotel.git']])
                }
            }
        }
    }
}