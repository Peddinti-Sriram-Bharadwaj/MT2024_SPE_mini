pipeline {
    agent {
        label 'built-in'
    }
    environment {
        REGISTRY = "${env.DOCKER_REGISTRY ?: 'docker.io'}"
        IMAGE_NAME = "sriram9217/scientific-calculator"
        IMAGE_TAG = "latest"
        VENV_DIR = "venv"
    }

    stages {
        stage('Setup Virtual Environment') {
            steps {
                script {
                    docker.image('ubuntu:latest').inside('-u root') {
                        sh "apt-get update && apt-get install -y python3 python3-venv python3-pip"
                        sh "python3 -m venv ${VENV_DIR}"
                        sh "${VENV_DIR}/bin/pip install --upgrade pip"
                        sh "${VENV_DIR}/bin/pip install -r requirements.txt"
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    docker.image('ubuntu:latest').inside('-u root') {
                        sh "rm -rf build/"
                        sh "python3 --version"
                        sh "${VENV_DIR}/bin/pip install --upgrade pip"
                        sh "${VENV_DIR}/bin/pip install -e .[test]"
                        sh "${VENV_DIR}/bin/pytest src/scientific-calculator/test/"
                    }
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    docker.image('ubuntu:latest').inside('-u root') {
                        sh "python3 --version"
                        sh "${VENV_DIR}/bin/pip install --upgrade pip"
                        sh "${VENV_DIR}/bin/pip install -e ."
                        sh "${VENV_DIR}/bin/python setup.py sdist bdist_wheel"
                        archiveArtifacts artifacts: 'dist/*', fingerprint: true
                    }
                }
            }
        }

        stage('Docker Build and Push') {
            steps {
                script {
                    docker.image('ubuntu:latest').inside('-u root') {
                        sh "apt-get update && apt-get install -y docker.io"
                        sh "docker --version"
                        sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                        withCredentials([
                            usernamePassword(credentialsId: 'docker-hub-user', passwordVariable: 'REGISTRY_PASSWORD', usernameVariable: 'REGISTRY_USER')
                        ]) {
                            sh "docker login -u ${REGISTRY_USER} -p ${REGISTRY_PASSWORD} ${REGISTRY}"
                            sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            agent any
            steps {
                script {
                    withCredentials([
                        usernamePassword(credentialsId: 'docker-hub-user', passwordVariable: 'DOCKER_REGISTRY_PASSWORD', usernameVariable: 'DOCKER_REGISTRY_USER')
                    ]){
                        docker.image('ubuntu:latest').inside('-u root') {
                            sh "apt-get update && apt-get install -y ansible"
                            sh "docker --version"
                            sh "docker login -u ${DOCKER_REGISTRY_USER} -p ${DOCKER_REGISTRY_PASSWORD} ${REGISTRY}"
                            sh "ansible-galaxy collection install community.docker"
                            sh "ansible-playbook -i inventory.ini deployment.yml"
                        }
                    }
                }
            }
        }
    }
}
