pipeline {
    agent {
        label 'built-in'
    }
    environment {
        REGISTRY = "${env.DOCKER_REGISTRY ?: 'docker.io'}"
        IMAGE_NAME = "sriram9217/scientific-calculator"
        IMAGE_TAG = "latest"
        DOCKER_CREDENTIALS = credentials('docker-hub-user')
    }
    stages {
        stage('Setup and Test') {
            steps {
                sh 'apt-get update && apt-get install -y python3 python3-venv python3-pip || true'
                sh 'python3 -m venv venv || true'
                sh './venv/bin/pip install --upgrade pip || true'
                sh './venv/bin/pip install -r requirements.txt || true'
                sh './venv/bin/pip install -e .[test] || true'
                sh './venv/bin/pytest src/scientific_calculator/test/ || true'
            }
        }
        stage('Build Python Package') {
            steps {
                sh 'python3 -m venv venv || true'
                sh './venv/bin/pip install --upgrade pip || true'
                sh './venv/bin/pip install -r requirements.txt || true'
                sh './venv/bin/python setup.py sdist bdist_wheel || true'
                archiveArtifacts artifacts: 'dist/*', fingerprint: true
            }
        }
        stage('Docker Build and Push') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
                sh 'echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin ${REGISTRY}'
                sh 'docker push ${IMAGE_NAME}:${IMAGE_TAG}'
            }
        }
        stage('Deploy') {
            steps {
                sh 'apt-get update && apt-get install -y ansible || true'
                sh 'ansible-galaxy collection install community.docker || true'
                sh 'ansible-playbook -i inventory.ini deployment.yml'
            }
        }
    }
    post {
        always {
            sh 'docker logout ${REGISTRY} || true'
            cleanWs()
        }
    }
}