pipeline {
  agent any

  stages {
    stage('Check and Stop Existing Container') {
            steps {
                script {
                    // Check if port 5000 is in use
                    def portInUse = sh(script: "lsof -i:5000", returnStatus: true) == 0

                    if (portInUse) {
                        // Find the container ID using port 5000
                        def containerId = sh(script: "docker ps --filter 'publish=5000' --format '{{.ID}}'", returnStdout: true).trim()

                        if (containerId) {
                            // Stop the container
                            sh "docker stop ${containerId}"
                            echo "Stopped container ${containerId} that was using port 5000"
                        }
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
    stage('Deploy') {
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKER_REGISTRY_CREDS}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
          sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin docker.io"
          sh 'docker push $DOCKER_BFLASK_IMAGE'
          sh 'docker run -p 5000:5000 -td $DOCKER_BFLASK_IMAGE'
        }
      }
    }
//   stage('Deploy to Kubernetes') {
//       steps {
//         script {
//           withCredentials([file(credentialsId: 'kubernetes-config-file', variable: 'KUBECONFIG')]) {
//                         sh 'kubectl apply -f deploy/deployment.yaml'
//                         sh 'kubectl apply -f deploy/service.yaml'
//           }
//         }
//       }
//     }

  }

}