pipeline {
  agent any

  stages {
    stage('Install dependencies') {
      steps {
        script {
          if (isUnix()) {
            sh 'python -m venv .venv'
            sh '. .venv/bin/activate && pip install -r requirements.txt'
          } else {
            bat 'python -m venv .venv'
            bat '.venv\\Scripts\\activate && pip install -r requirements.txt'
          }
        }
      }
    }

    stage('Run tests') {
      steps {
        script {
          if (isUnix()) {
            sh '. .venv/bin/activate && pytest -q --junitxml=report.xml'
          } else {
            bat '.venv\\Scripts\\activate && pytest -q --junitxml=report.xml'
          }
        }
      }
    }
  }

  post {
    always {
      junit 'report.xml'
    }
  }
}
