/*
Declarative Jenkinsfile.

Replace placeholders and configure credentials in Jenkins:
 - <JENKINS_DOCKERHUB_CREDENTIAL_ID>  : credential id storing DockerHub username/password (usernamePassword).
 - <JENKINS_ADMIN_EMAIL_CREDENTIAL_ID>: credential id (string) storing admin email for notifications or set as global variable.
 - Ensure Docker is available on the Jenkins agent or use a Docker-in-Docker setup.

SMTP/email:
 - Configure Jenkins -> Manage Jenkins -> Configure System -> E-mail Notification / Extended E-mail Notification.
 - If you use emailext, install the Email Extension Plugin.

This pipeline:
 - Checks out code
 - Builds Docker image and tags with build number and latest
 - Logs into Docker Hub using credentials and pushes
 - Sends email notification on success/failure
*/

pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = 'huzaifa007'
        DOCKERHUB_REPO = 'mlops-ass'
        DOCKERHUB_FULL_REPO = "${DOCKERHUB_USERNAME}/${DOCKERHUB_REPO}"
        DOCKERHUB_CREDENTIALS = 'jenkins-dockerhub-cred'
        ADMIN_EMAIL_CREDENTIAL = 'jenkins-admin-email'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker') {
            steps {
                script {
                    def imageTag = "${env.BUILD_NUMBER}"
                    def imageName = "${DOCKERHUB_FULL_REPO}:${imageTag}"
                    def latestTag = "${DOCKERHUB_FULL_REPO}:latest"

                    sh "docker build -t ${imageName} -f Dockerfile ."
                    sh "docker tag ${imageName} ${latestTag}"
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                // Uses withCredentials in Jenkins pipeline to access username/password pair
                withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS,
                                                  usernameVariable: 'DOCKERHUB_USER',
                                                  passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh """
                        echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker push ${DOCKERHUB_FULL_REPO}:${BUILD_NUMBER}
                        docker push ${DOCKERHUB_FULL_REPO}:latest
                        docker logout
                    """
                }
            }
        }
    }

    post {
        success {
            // Send success email to admin
            script {
                // Try to retrieve stored admin email from credentials (string credential)
                def adminEmail = ''
                try {
                    adminEmail = credentials("${ADMIN_EMAIL_CREDENTIAL}")
                } catch (err) {
                    echo "Could not load admin email from credentials id '${ADMIN_EMAIL_CREDENTIAL}': ${err}"
                }
                if (adminEmail) {
                    emailext (
                        subject: "Jenkins: Docker push SUCCESS - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: "Build and push succeeded.\nJob: ${env.JOB_NAME}\nBuild: ${env.BUILD_NUMBER}\nRepository: ${DOCKERHUB_FULL_REPO}",
                        to: adminEmail
                    )
                } else {
                    echo "Admin email not configured; skipping email."
                }
            }
        }
        failure {
            script {
                def adminEmail = ''
                try {
                    adminEmail = credentials("${ADMIN_EMAIL_CREDENTIAL}")
                } catch (err) {
                    echo "Could not load admin email from credentials id '${ADMIN_EMAIL_CREDENTIAL}': ${err}"
                }
                if (adminEmail) {
                    emailext (
                        subject: "Jenkins: Docker push FAILED - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: "Build or push failed.\nJob: ${env.JOB_NAME}\nBuild: ${env.BUILD_NUMBER}\nCheck console output for details.",
                        to: adminEmail
                    )
                } else {
                    echo "Admin email not configured; skipping failure email."
                }
            }
        }
    }
}
