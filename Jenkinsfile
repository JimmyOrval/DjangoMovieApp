pipeline {
  agent any

  triggers {
    pollSCM('H/2 * * * *')
  }

  environment {
    MINIKUBE_PROFILE = 'minikube'
    IMAGE_NAME = 'my-django-app:latest'
  }

  stages {

    stage('Diagnostics - whoami & env') {
      steps {
        bat '''
        echo ===== Running as =====
        whoami
        echo USERPROFILE=%USERPROFILE%
        echo PATH=%PATH%
        echo ===== Check existing kubeconfig =====
        if exist "%USERPROFILE%\\.kube\\config" ( echo kubeconfig found & type "%USERPROFILE%\\.kube\\config" ) else ( echo NO kubeconfig for this user )
        '''
      }
    }

    stage('Start Minikube & prepare env') {
   steps {
     bat '''
     REM Start minikube with --force flag to avoid pulling the image again if it's already present
     minikube cache add registry.k8s.io/kube-apiserver:v1.29.0
     minikube cache add registry.k8s.io/kube-controller-manager:v1.29.0
     minikube start --driver=docker

     REM Ensure kubectl context points to Minikube
     minikube -p %MINIKUBE_PROFILE% update-context

     REM Show minikube & cluster status for debugging (retry in case of unavailability)
     REM Retry minikube status and kubectl cluster-info a few times in case of network/delay issues
     for /l %%x in (1, 1, 5) do (
       minikube status && (
         echo Minikube is running! 
         goto continue
       )
       echo Minikube is not ready. Retrying...
       timeout /t 10
     )

     :continue
     minikube -p %MINIKUBE_PROFILE% kubectl -- cluster-info || echo "cluster-info may still be unavailable"
     '''
   }
}

    stage('Use Minikube Docker and build image') {
      steps {
        bat '''
        REM Switch docker CLI to Minikube's Docker daemon for the rest of this step
        minikube -p %MINIKUBE_PROFILE% docker-env --shell=cmd > docker_env.bat
        call docker_env.bat

        REM Confirm docker now points to minikube (docker info should show minikube server or docker engine info)
        docker version
        docker info

        REM Build the image *inside* Minikube Docker so k8s can use it without pushing
        docker build -t %IMAGE_NAME% .
        '''
      }
    }

    stage('Deploy to Minikube') {
      steps {
        bat '''
        REM Use minikube's kubectl wrapper which uses the right kubeconfig/context
        minikube -p %MINIKUBE_PROFILE% kubectl -- apply -f deployment.yaml --validate=false

        REM Wait for rollout
        minikube -p %MINIKUBE_PROFILE% kubectl -- rollout status deployment/django-deployment --timeout=1200s

        REM Show pods to verify
        minikube -p %MINIKUBE_PROFILE% kubectl -- get pods -o wide
        '''
      }
    }
  }

  post {
    always {
      echo 'Pipeline finished'
    }
    failure {
      echo 'Pipeline failed — inspect console output for diagnostics'
    }
  }
}
