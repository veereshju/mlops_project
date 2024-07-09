pipeline {
  agent any

  stages {
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
    stage('Image Push to Registry') {
      steps {
          sh 'docker push $DOCKER_BFLASK_IMAGE'
      }
    }
  stage('Deploy to Kubernetes') {
      steps {
        script {
          withCredentials([file(credentialsId: 'kubernetes-config-file', variable: 'KUBECONFIG')]) {
                        sh 'kubectl apply -f deploy/deployment.yaml'
                        sh 'kubectl apply -f deploy/service.yaml'
          }
        }
      }
    }

  }

}