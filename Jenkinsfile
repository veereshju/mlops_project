pipeline {
    agent any

    stages {
        stage('Check and Stop Existing Container') {
            steps {
                script {
                    def containerId = sh(script: "docker ps --filter 'publish=5000' --format '{{.ID}}'", returnStdout: true).trim()

                    if (containerId) {
                        // Stop the container
                        sh "docker stop ${containerId}"
                        echo "Stopped container ${containerId} that was using port 5000"

                        // Verify the container is stopped
                        def containerRunning = sh(script: "docker ps --filter 'id=${containerId}' --format '{{.ID}}'", returnStdout: true).trim()

                        if (containerRunning) {
                            error "Failed to stop container ${containerId}. Manual intervention required."
                        } else {
                            echo "Container ${containerId} successfully stopped."
                        }
                    } else {
                        echo "No container found using port 5000."
                    }
                }
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t my-flask-app .'
                sh 'docker tag my-flask-app $DOCKER_BFLASK_IMAGE'
            }
        }
        stage('Test') {
            steps {
                sh 'docker run my-flask-app python -m pytest app/tests/'
            }
        }
        stage('Push image to Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_REGISTRY_CREDS}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin docker.io"
                    sh 'docker push $DOCKER_BFLASK_IMAGE'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    sh 'docker run -p 5000:5000 -td $DOCKER_BFLASK_IMAGE'
                }
            }
        }
    }
}
