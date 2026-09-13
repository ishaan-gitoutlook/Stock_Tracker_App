pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        VENV_DIR = '.venv-ci'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from Git repository...'
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv ${VENV_DIR} || python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate || ${VENV_DIR}/Scripts/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Executing test suite across all modules...'
                sh '''
                    . ${VENV_DIR}/bin/activate || ${VENV_DIR}/Scripts/activate
                    python -m unittest discover tests -v
                '''
            }
        }

        stage('Smoke Test & Integrity Check') {
            steps {
                echo 'Verifying core application modules...'
                sh '''
                    . ${VENV_DIR}/bin/activate || ${VENV_DIR}/Scripts/activate
                    python -c "import fastapi, streamlit; from src.api import app; from src.dashboard import render_dashboard_app; print('FastAPI & Streamlit modules loaded successfully!')"
                '''
            }
        }

        stage('Deploy Notification') {
            steps {
                echo '✅ All tests passed. Application is ready for cloud deployment.'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up CI environment...'
            sh 'rm -rf ${VENV_DIR} __pycache__ src/__pycache__ tests/__pycache__ || true'
        }
        success {
            echo '🎉 Pipeline completed successfully!'
        }
        failure {
            echo '⚠️ Pipeline failed. Please inspect stage logs above.'
        }
    }
}
