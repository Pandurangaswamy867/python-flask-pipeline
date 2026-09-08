pipeline {
agent any

```
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
                set -e

                docker stop test-container || true
                docker rm test-container || true

                docker run -d \
                    --name test-container \
                    $IMAGE_NAME:$IMAGE_TAG

                echo "Waiting for application..."
                sleep 10

                docker ps -a

                echo "Testing application..."

                docker exec test-container \
                    python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/health').read().decode())"

                echo "Test successful"
            '''
        }

        post {
            always {
                sh '''
                    docker stop test-container || true
                    docker rm test-container || true
                '''
            }
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
                    echo "$DOCKER_PASS" | docker login \
                        -u "$DOCKER_USER" \
                        --password-stdin
                '''
            }
        }
    }

    stage('Push Docker Image') {
        steps {
            sh '''
                docker push $IMAGE_NAME:$IMAGE_TAG

                docker tag \
                    $IMAGE_NAME:$IMAGE_TAG \
                    $IMAGE_NAME:latest

                docker push $IMAGE_NAME:latest
            '''
        }
    }

    stage('Deploy Application') {
        steps {
            sh '''
                set -e

                echo "Stopping old application..."

                docker stop flask-app || true
                docker rm flask-app || true

                echo "Starting new application..."

                docker run -d \
                    --name flask-app \
                    -p 5000:5000 \
                    --restart unless-stopped \
                    $IMAGE_NAME:$IMAGE_TAG

                echo "Waiting for application..."
                sleep 10

                echo "Running containers:"
                docker ps

                echo "Checking application health..."

                curl -f http://localhost:5000/health

                echo ""
                echo "Deployment successful"
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
        sh '''
            docker stop test-container || true
            docker rm test-container || true
            docker image prune -f || true
        '''
    }
}
```

}
