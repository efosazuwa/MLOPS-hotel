pipeline{
    agent any

    environment {
        VENV_DIR = '.venv'
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
    }
}