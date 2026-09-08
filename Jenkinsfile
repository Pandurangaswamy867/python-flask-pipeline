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
                echo "Building Docker image..."
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                echo "Build completed successfully."
            '''
        }
    }

    stage('Test Container') {
        steps {
            sh '''
                set -e

                echo "Cleaning old test container..."
                docker stop test-container || true
                docker rm test-container || true

                echo "Starting test container..."
                docker run -d \
                    --name test-container \
                    $IMAGE_NAME:$IMAGE_TAG

                echo "Waiting for application..."
                sleep 10

                echo "Testing Flask application..."

                docker exec test-container \
                    python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/health').read().decode())"

                echo "Application test PASSED."
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
                echo "Pushing image: $IMAGE_NAME:$IMAGE_TAG"

                docker push $IMAGE_NAME:$IMAGE_TAG

                echo "Tagging image as latest..."

                docker tag \
                    $IMAGE_NAME:$IMAGE_TAG \
                    $IMAGE_NAME:latest

                echo "Pushing latest image..."

                docker push $IMAGE_NAME:latest

                echo "Docker image pushed successfully."
            '''
        }
    }

    stage('Deploy Application') {
        steps {
            sh '''
                set -e

                echo "Stopping old application container..."

                docker stop flask-app || true

                echo "Removing old application container..."

                docker rm flask-app || true

                echo "Starting new application..."

                docker run -d \
                    --name flask-app \
                    -p 5000:5000 \
                    --restart unless-stopped \
                    $IMAGE_NAME:$IMAGE_TAG

                echo "New container started."

                echo "Waiting for application..."
                sleep 10

                echo "Checking container status..."

                docker ps

                echo "Running health check..."

                curl -f http://localhost:5000/health

                echo ""
                echo "Application deployed successfully."
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
            echo "Cleaning temporary containers..."
            docker stop test-container || true
            docker rm test-container || true

            echo "Cleaning unused Docker images..."
            docker image prune -f || true
        '''
    }
}
```

}
