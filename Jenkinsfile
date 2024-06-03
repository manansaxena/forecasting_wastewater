pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'ghcr.io/manansaxena/wastewater-forecast'
        REGISTRY_CREDENTIAL_ID = "4da7cd78-7585-4f26-9d67-c41d9b90340e"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Check Branch') {
            steps {
                script {
                    echo "Running on branch: ${env.BRANCH_NAME}"
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    docker.build("${env.DOCKER_IMAGE}:${env.IMAGE_TAG}", '.')
                }
            }
        }

        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://ghcr.io', env.REGISTRY_CREDENTIAL_ID) {
                        docker.image("${env.DOCKER_IMAGE}:${env.IMAGE_TAG}").push('latest')
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
