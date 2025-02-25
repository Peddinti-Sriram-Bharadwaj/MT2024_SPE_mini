pipeline {
    agent any

    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3.9'
                    reuseNode true
                }
            }
            steps {
                sh 'python --version'
                sh 'pip install --upgrade pip'
                sh 'pip install -e .[test]'
                sh 'python setup.py test'
            }
        }

        stage('Build') {
            agent {
                docker {
                    image 'python:3.9'
                    reuseNode true
                }
            }
            steps {
                sh 'python --version'
                sh 'pip install --upgrade pip'
                sh 'pip install -e .'
                sh 'python setup.py sdist bdist_wheel'
                archiveArtifacts artifacts: 'dist/*', fingerprint: true
            }
        }

        stage('Docker Build and Push') {
            agent {
                docker {
                    image 'docker:latest'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                    reuseNode true
                }
            }
            environment {
                REGISTRY = "${env.DOCKER_REGISTRY}"
                REGISTRY_USER = "${env.DOCKER_REGISTRY_USER}"
                REGISTRY_PASSWORD = "${env.DOCKER_REGISTRY_PASSWORD}"
                IMAGE_NAME = "${env.DOCKER_IMAGE_NAME}"
            }
            steps {
                sh 'docker --version'
                sh 'docker build -t ${IMAGE_NAME}:latest .'
                sh 'docker login -u ${REGISTRY_USER} -p ${REGISTRY_PASSWORD} ${REGISTRY}'
                sh 'docker push ${IMAGE_NAME}:latest'
            }
        }
    }
}
