node {
  currentBuild.result = "SUCCESS"
  setBuildStatus("Build started", "PENDING");

  try {
    stage('Checkout') {
      checkout scm
      gitCommit = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
      shortCommit = gitCommit.take(7)
    }

    stage('Build') {
      parallel 'build-image':{
        sh "docker build -t ${env.BUILD_TAG} ."
      }, 'run-test-environment': {
        sh "docker-compose --project-name myapp up -d"
      }
    }

    stage('Test') {
      ansiColor('xterm') {
        sh "docker run -t --rm --network=myapp_default -e DATABASE_HOST=postgres ${env.BUILD_TAG} python manage.py test"
      }
    }

    stage('Deploy - Staging') {
      // TODO. Use env.BRANCH_NAME to make sure we only deploy from staging
      withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'Heroku Git Login', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD']]) {
         sh('git push https://${GIT_USERNAME}:${GIT_PASSWORD}@git.heroku.com/myapp-staging.git staging')
      }
      setBuildStatus("Staging build complete", "SUCCESS");
    }

    stage('Sanity check') {
        if (env.BRANCH_NAME == 'master'){
             input "Does the staging environment look ok?"

        }
    }
    stage('Deploy - Production') {
        echo 'deploy check'
        if(env.BRANCH_NAME == 'master'){
            echo 'deploying right now'
        }
      // TODO. Use env.BRANCH_NAME to make sure we only deploy from master
      withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'Heroku Git Login', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD']]) {
       sh('git push https://${GIT_USERNAME}:${GIT_PASSWORD}@git.heroku.com/myapp-production.git HEAD:refs/heads/master')
    }
    setBuildStatus("Production build complete", "SUCCESS");
  } catch(error){
  }
}
