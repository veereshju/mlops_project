pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        sh 'docker build -t my-ml-app .'
        sh 'docker tag my-ml-app $DOCKER_BFLASK_IMAGE'
      }
    }
    stage('Retraining model') {
      steps {
        sh 'docker run my-ml-app python app/tests/retrain.py'
        sh 'docker tag my-ml-app $DOCKER_BFLASK_IMAGE'
      }
    }
     stage('Test') {
       steps {
         sh 'docker run my-ml-app python -m pytest model/evaluate.py'
       }
     }
//     stage('Image Push to Registry') {
//       steps {
//           sh 'docker push $DOCKER_BFLASK_IMAGE'
//       }
//     }
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