pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Lint') {
            steps {
                echo 'Running code quality checks...'
                sh '''
                    pip install flake8
                    flake8 app/ --max-line-length=120 --exclude=__pycache__ || true
                '''
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    pytest tests/ -v --tb=short
                '''
            }
        }
        
        stage('Coverage') {
            steps {
                echo 'Generating coverage report...'
                sh '''
                    pip install pytest-cov
                    pytest tests/ --cov=app --cov-report=term-missing
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed'
        }
        success {
            echo '✅ Build succeeded!'
        }
        failure {
            echo '❌ Build failed!'
        }
    }
}
