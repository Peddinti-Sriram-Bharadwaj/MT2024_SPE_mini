pipeline {
    agent {
        label 'built-in'
    }
    
    stages {
        stage('Test') {
            steps {
                script {
                    docker.image('python:3.9').inside('-u root') {
                        sh 'python --version'
                        sh 'pip install --upgrade pip'
                        sh 'pip install -e .[test]'
                        sh 'python setup.py test'
                    }
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    docker.image('python:3.9').inside('-u root') {
                        sh 'python --version'
                        sh 'pip install --upgrade pip'
                        sh 'pip install -e .'
                        sh 'python setup.py sdist bdist_wheel'
                        archiveArtifacts artifacts: 'dist/*', fingerprint: true
                    }
                }
            }
        }

        stage('Docker Build and Push') {
            environment {
                REGISTRY = "${env.DOCKER_REGISTRY ?: 'docker.io'}"
                REGISTRY_USER = "${env.DOCKER_REGISTRY_USER}"
                REGISTRY_PASSWORD = "${env.DOCKER_REGISTRY_PASSWORD}"
                IMAGE_NAME = "${env.DOCKER_IMAGE_NAME}"
            }
            steps {
                script {
                    docker.image('docker:latest').inside('-v /var/run/docker.sock:/var/run/docker.sock -u root') {
                        sh 'docker --version'
                        sh 'docker build -t ${IMAGE_NAME}:latest .'
                        withCredentials([string(credentialsId: 'docker-hub-password', variable: 'REGISTRY_PASSWORD')]) {
                            sh "docker login -u ${REGISTRY_USER} -p ${REGISTRY_PASSWORD} ${REGISTRY}"
                        }
                        sh 'docker push ${IMAGE_NAME}:latest'
                    }
                }
            }
        }
    }
}
