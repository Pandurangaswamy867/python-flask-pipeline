pipeline {
    agent any

    environment {
        IMAGE_NAME = "pandu867/bubu-flaskapp"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Test Container') {
            steps {
                sh '''
                docker run -d --name test-container -p 5000:5000 $IMAGE_NAME:$IMAGE_TAG

                sleep 10

                docker ps

                docker stop test-container
                docker rm test-container
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-cred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                docker push $IMAGE_NAME:$IMAGE_TAG

                docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest

                docker push $IMAGE_NAME:latest
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                docker stop flask-app || true
                docker rm flask-app || true

                docker run -d \
                --name flask-app \
                -p 5000:5000 \
                $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD Pipeline Completed Successfully'
        }

        failure {
            echo 'Pipeline Failed'
        }

        always {
            sh 'docker image prune -f || true'
        }
    }
}
