
Use the following **exact content** in your GitHub `Jenkinsfile` — copy from `pipeline {` to the final `}` only:

:::writing{variant="document" id="31467" title="Jenkinsfile"}
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
                echo "Building Docker image..."

                docker build -t $IMAGE_NAME:$IMAGE_TAG .

                echo "Docker image built successfully"
                docker images $IMAGE_NAME
                '''
            }
        }

        stage('Test Container') {
            steps {
                sh '''
                set -e

                echo "Cleaning previous test container..."

                docker stop test-container || true
                docker rm test-container || true

                echo "Starting test container..."

                docker run -d \
                    --name test-container \
                    $IMAGE_NAME:$IMAGE_TAG

                echo "Waiting for Flask application..."
                sleep 10

                echo "Container status:"
                docker ps -a

                echo "Testing Flask health endpoint..."

                docker exec test-container \
                    python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/health').read().decode())"

                echo "Application test successful"

                echo "Removing test container..."

                docker stop test-container || true
                docker rm test-container || true
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
                echo "Pushing image..."

                docker push $IMAGE_NAME:$IMAGE_TAG

                echo "Tagging image as latest..."

                docker tag \
                    $IMAGE_NAME:$IMAGE_TAG \
                    $IMAGE_NAME:latest

                echo "Pushing latest image..."

                docker push $IMAGE_NAME:latest
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                set -e

                echo "======================================"
                echo "Stopping old application"
                echo "======================================"

                docker stop flask-app || true

                echo "Removing old application..."

                docker rm flask-app || true

                echo "======================================"
                echo "Starting new application"
                echo "======================================"

                docker run -d \
                    --name flask-app \
                    -p 5000:5000 \
                    --restart unless-stopped \
                    $IMAGE_NAME:$IMAGE_TAG

                echo "New application started"

                echo "Waiting for application..."
                sleep 10

                echo "======================================"
                echo "Container Status"
                echo "======================================"

                docker ps

                echo "======================================"
                echo "Health Check"
                echo "======================================"

                curl -f http://localhost:5000/health

                echo ""
                echo "======================================"
                echo "Deployment Successful"
                echo "======================================"
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
            echo "Cleaning test container..."

            docker stop test-container || true
            docker rm test-container || true

            echo "Cleaning unused Docker images..."

            docker image prune -f || true
            '''
        }
    }
}
:::

### One more thing

Don't copy the `:::writing...` lines either. Those are just formatting from this chat.

Your GitHub file should literally look like:

```text
pipeline {
    agent any

    environment {
        ...
    }

    stages {
        ...
    }

    post {
        ...
    }
}
