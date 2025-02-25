pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                script {
                    docker.image('python:3.9').inside {
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
                    docker.image('python:3.9').inside {
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
            steps {
                script {
                    docker.image('docker:latest').inside('-v /var/run/docker.sock:/var/run/docker.sock') {
                        sh 'docker --version'
                        sh 'docker build -t ${DOCKER_IMAGE_NAME}:latest .'
                        sh 'docker login -u ${DOCKER_REGISTRY_USER} -p ${DOCKER_REGISTRY_PASSWORD} ${DOCKER_REGISTRY}'
                        sh 'docker push ${DOCKER_IMAGE_NAME}:latest'
                    }
                }
            }
        }
    }
}
