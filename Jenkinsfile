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
                        sh 'pytest'
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
                //REGISTRY_USER = "${env.DOCKER_REGISTRY_USER}" remove this variable as it is not needed
                //REGISTRY_PASSWORD = "${env.DOCKER_REGISTRY_PASSWORD}" remove this variable as it is not needed
                IMAGE_NAME = "${env.DOCKER_IMAGE_NAME}"
            }
            steps {
                script {
                    docker.image('docker:latest').inside('-v /var/run/docker.sock:/var/run/docker.sock -u root') {
                        sh 'docker --version'
                        sh 'docker build -t ${IMAGE_NAME}:latest .'
                        withCredentials([
                           usernamePassword(credentialsId: 'docker-hub-user', passwordVariable: 'REGISTRY_PASSWORD', usernameVariable: 'REGISTRY_USER')
                        ]) {
                            sh "docker login -u ${REGISTRY_USER} -p ${REGISTRY_PASSWORD} ${REGISTRY}"
                        }
                        sh 'docker push ${IMAGE_NAME}:latest'
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
                        sh 'ansible-galaxy collection install community.docker'
                        sh '''
                            ansible-playbook -i inventory.ini deployment.yml
                        '''
                    }
                }
            }
        }

    }
}
