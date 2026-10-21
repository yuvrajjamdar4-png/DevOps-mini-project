
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                bat 'py -3.13 -m venv .venv'
                bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pytest -v --junitxml=test-results.xml'
            }
        }

        stage('Coverage Report') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pytest --cov=app --cov=database --cov-report=term-missing --cov-report=html'
            }
        }
    }

    post {
        always {
            junit testResults: 'test-results.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'htmlcov/**', allowEmptyArchive: true
        }

        success {
            echo 'All pipeline stages completed successfully.'
        }

        failure {
            echo 'The pipeline failed. Check the stage logs.'
        }
    }
}
