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
        stage('Install Dependencies') {
            steps {
                script {
                    docker.image('ubuntu:latest').inside('-u root') {
                        sh "apt-get update && apt-get install -y python3 python3-venv python3-pip git docker.io ansible"
                    }
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    docker.image('ubuntu:latest').inside('-u root') {
                        sh "apt-get update && apt-get install -y python3 python3-venv python3-pip git"
                        sh "python3 --version" // Verify installation
                        sh "python3 -m venv ${VENV_DIR}"
                        sh "${VENV_DIR}/bin/pip install --upgrade pip"
                        sh "${VENV_DIR}/bin/pip install -r requirements.txt"
                    }
                }
                stash name: 'requirements', includes: 'requirements.txt'
            }
        }


        stage('Test') {
            steps {
                script {
                    docker.image('ubuntu:latest').inside('-u root') {
                        unstash 'requirements'
                        sh "${VENV_DIR}/bin/pip install -r requirements.txt"
                        sh "rm -rf build/"
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
                        unstash 'requirements'
                        sh "${VENV_DIR}/bin/pip install -r requirements.txt"
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
                    ]) {
                        docker.image('ubuntu:latest').inside('-u root') {
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
