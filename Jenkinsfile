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
        if exist "%USERPROFILE%\\.kube\\config" (
          echo kubeconfig found
          type "%USERPROFILE%\\.kube\\config"
        ) else (
          echo NO kubeconfig for this user
        )
        '''
      }
    }

    stage('Start Minikube & prepare env') {
      steps {
        bat '''
        echo Starting Minikube...
        minikube -p %MINIKUBE_PROFILE% start --driver=docker

        echo Ensuring kubectl context points to Minikube...
        minikube -p %MINIKUBE_PROFILE% update-context

        echo Checking Minikube status...
        set READY=0
        for /l %%x in (1,1,5) do (
          minikube -p %MINIKUBE_PROFILE% status && (
            echo Minikube is running!
            set READY=1
            goto :ready
          )
          echo Minikube not ready, retrying in 10 seconds...
          timeout /t 10 >nul
        )
        :ready

        if "%READY%"=="0" (
          echo Minikube failed to start after retries.
          exit /b 1
        )

        minikube -p %MINIKUBE_PROFILE% kubectl -- cluster-info || echo "cluster-info may still be unavailable"
        '''
      }
    }

    stage('Use Minikube Docker and build image') {
      steps {
        bat '''
        echo Switching Docker CLI to Minikube daemon...
        minikube -p %MINIKUBE_PROFILE% docker-env --shell=cmd > docker_env.bat
        call docker_env.bat

        echo Docker context:
        docker version
        docker info

        echo Building image %IMAGE_NAME% inside Minikube Docker...
        docker build -t %IMAGE_NAME% .
        '''
      }
    }

    stage('Deploy to Minikube') {
      steps {
        bat '''
        echo Deploying to Minikube...
        minikube -p %MINIKUBE_PROFILE% kubectl -- apply -f deployment.yaml --validate=false
        minikube -p %MINIKUBE_PROFILE% kubectl -- apply -f service.yaml --validate=false

        echo Restarting Django deployment...
        minikube -p %MINIKUBE_PROFILE% kubectl -- rollout restart deployment/django-deployment

        echo Waiting for rollout to complete...
        minikube -p %MINIKUBE_PROFILE% kubectl -- rollout status deployment/django-deployment --timeout=600s

        echo Listing pods and services:
        minikube -p %MINIKUBE_PROFILE% kubectl -- get pods -o wide
        minikube -p %MINIKUBE_PROFILE% kubectl -- get svc
        '''
      }
    }

    stage('Get Django Service URL') {
      steps {
        bat '''
        echo ===== Getting Django Service URL (headless safe) =====
        for /f "tokens=2 delims=:" %%A in ('minikube -p %MINIKUBE_PROFILE% kubectl -- get svc django-service --output="jsonpath={.spec.ports[0].nodePort}"') do (
          echo http://127.0.0.1:%%A > service_url.txt
        )
        type service_url.txt
        '''
      }
    }
  }

  

  post {
    always {
      echo 'Pipeline finished. Checking Minikube status...'
      bat 'minikube -p %MINIKUBE_PROFILE% status || echo Minikube not running'
    }
    failure {
      echo 'Pipeline failed — inspect console output for diagnostics'
    }
  }
}
