pipeline {
    agent any  // This allows Jenkins to use any available agent

    stages {
        stage('Prepare') {
            steps {
                script {
                    try {
                        sh 'docker pull python:3.13'
                    } catch (Exception e) {
                        error "Failed to pull Python image: ${e}"
                    }
                }
            }
        }

        stage('Test') {
            steps {
                sh 'echo Running tests...'
            }
        }

        stage('Build') {
            steps {
                sh 'echo Building project...'
            }
        }

        stage('Docker Build and Push') {
            steps {
                sh 'echo Building Docker image...'
            }
        }
    }
}
