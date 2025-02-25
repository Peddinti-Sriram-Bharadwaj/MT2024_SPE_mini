pipeline {
    agent any

    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3.9'
                }
            }
            steps {
                sh 'python --version'
                sh 'pip install --upgrade pip'
                sh 'pip install -e .[test] || pip install .[test]'  // Fallback
                sh 'pytest'  // Modern testing instead of setup.py test
            }
        }

        stage('Build') {
            agent {
                docker {
                    image 'python:3.9'
                }
            }
            steps {
                sh 'python --version'
                sh 'pip install --upgrade pip'
                sh 'pip install -e . || pip install .'  // Fallback
                sh 'python setup.py sdist bdist_wheel'
                archiveArtifacts artifacts: 'dist/*', fingerprint: true
            }
        }

        stage('Docker Build and Push') {
            agent {
                docker {
                    image 'docker:latest'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            environment {
                REGISTRY = "${env.DOCKER_REGISTRY ?: 'docker.io'}"
                REGISTRY_USER = "${env.DOCKER_REGISTRY_USER ?: 'default-user'}"
                REGISTRY_PASSWORD = "${env.DOCKER_REGISTRY_PASSWORD ?: 'default-pass'}"
                IMAGE_NAME = "${env.DOCKER_IMAGE_NAME ?: 'my-image'}"
            }
            steps {
                sh 'docker --version'
                sh 'docker build -t ${IMAGE_NAME}:latest .'
                sh 'echo ${REGISTRY_PASSWORD} | docker login -u ${REGISTRY_USER} --password-stdin ${REGISTRY}'
                sh 'docker push ${IMAGE_NAME}:latest'
            }
        }
    }
}
