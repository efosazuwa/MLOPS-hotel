pipeline{
    agent any

    environment {
        VENV_DIR = '.venv'
        GCP_PROJECT = "windy-forge-455000-i8"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/efosazuwa/MLOPS-hotel.git']])
                }
            }
        }
        stage('Install UV Package Manager and Dependencies'){
            steps{
                script{
                    echo 'Installing UV package manager if not available...'
                    sh '''
                        if ! command -v uv &> /dev/null; then
                            echo "Installing uv package manager..."
                            curl -LsSf https://astral.sh/uv/install.sh | sh
                            export PATH="$HOME/.cargo/bin:$PATH"
                        fi
                        
                        # Make sure the path is set
                        . $HOME/.local/bin/env

                        # Make sure uv is available
                        uv --version

                        uv sync --frozen
                        uv pip install -e .
                        uv pip list
                        '''
                }
            }
        }
        stage('Building and Pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing Docker Image to GCR...'
                        sh '''
                            export PATH=$PATH:$(GCLOUD_PATH)

                            gcloud auth activate-service-account --key-flie=${GOOGLE_APPLICATION_CREDENTIALS}

                            gcloud config set project ${GCP_PROJECT}

                            gcloud auth configure-docker --quiet

                            docker build -t gcr.io/${GCP_PROJECT}/hotel-mlops:latest .

                            docker push gcr.io/${GCP_PROJECT}/hotel-mlops:latest
                            '''

                    }
                }
                
            }
        }
    }
}