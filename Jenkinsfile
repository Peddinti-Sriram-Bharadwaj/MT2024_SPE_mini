pipeline {
    agent {
        label 'built-in'
    }
    environment {
        // Define environment variables here, making them accessible throughout the pipeline
        REGISTRY = "${env.DOCKER_REGISTRY ?: 'docker.io'}"
        IMAGE_NAME = "sriram9217/scientific-calculator"
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
                //define environment variables only if needed.
                IMAGE_TAG = "latest" //Define the tag
            }
            steps {
                script {
                    docker.image('docker:latest').inside('-v /var/run/docker.sock:/var/run/docker.sock -u root') {
                        sh 'docker --version'
                        sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ." //Use tag
                        withCredentials([
                           usernamePassword(credentialsId: 'docker-hub-user', passwordVariable: 'REGISTRY_PASSWORD', usernameVariable: 'REGISTRY_USER')
                        ]) {
                            sh "docker login -u ${REGISTRY_USER} -p ${REGISTRY_PASSWORD} ${REGISTRY}"
                            sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}" //Use tag
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
                        sh 'docker --version'
                        sh "docker login -u ${DOCKER_REGISTRY_USER} -p ${DOCKER_REGISTRY_PASSWORD} ${REGISTRY}"
                        sh 'ansible-galaxy collection install community.docker'
                        sh 'ansible-playbook -i inventory.ini deployment.yml'
                    }
                }
            }
        }
    }
}
