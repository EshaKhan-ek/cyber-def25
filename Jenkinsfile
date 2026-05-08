pipeline {
    agent any
 
    // ── Global environment variables ──────────────────────
    environment {
        DOCKER_HUB_USER  = 'eshakhan3870'
        IMAGE_NAME       = 'cyber-def25'
        IMAGE_TAG        = "${IMAGE_NAME}:${BUILD_NUMBER}"
        IMAGE_LATEST     = "${IMAGE_NAME}:latest"
        DOCKER_HUB_CRED  = 'dockerhub-credentials'
    }
 
    stages {
 
        // ══════════════════════════════════════════
        // STAGE 1 – Checkout Code from GitHub
        // ══════════════════════════════════════════
        stage('Checkout') {
            steps {
                echo 'Cloning repository from GitHub...'
                git branch: 'main',
                    url: 'https://github.com/EshaKhan-ek/cyber-def25.git'
                echo 'Code checkout complete.'
            }
        }
 
        // ══════════════════════════════════════════
        // STAGE 2 – Build Docker Image
        // ══════════════════════════════════════════
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKER_HUB_USER}/${IMAGE_TAG}"
                script {
                    sh """
                        docker build \\
                            -t ${DOCKER_HUB_USER}/${IMAGE_TAG} \\
                            -t ${DOCKER_HUB_USER}/${IMAGE_LATEST} \\
                            .
                    """
                    echo 'Docker image built successfully.'
                    sh 'docker images | grep ${IMAGE_NAME}'
                }
            }
            post {
                failure {
                    echo 'ERROR: Docker build failed. Check Dockerfile and dependencies.'
                }
            }
        }
 
        // ══════════════════════════════════════════
        // STAGE 3 – Push Docker Image to Docker Hub
        // ══════════════════════════════════════════
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                script {
                    withDockerRegistry([
                        credentialsId: DOCKER_HUB_CRED,
                        url: 'https://index.docker.io/v1/'
                    ]) {
                        sh 'docker push ${DOCKER_HUB_USER}/${IMAGE_TAG}'
                        sh 'docker push ${DOCKER_HUB_USER}/${IMAGE_LATEST}'
                    }
                    echo 'Image pushed successfully to Docker Hub.'
                }
            }
            post {
                failure {
                    echo 'ERROR: Push failed. Check Docker Hub credentials.'
                }
            }
        }
 
        // ══════════════════════════════════════════
        // STAGE 4 – Run Container via Docker Compose
        // ══════════════════════════════════════════
        stage('Run with Docker Compose') {
            steps {
                echo 'Running malware detection inference via Docker Compose...'
                sh """
                    mkdir -p output
                    export DOCKER_HUB_USER=${DOCKER_HUB_USER}
                    docker-compose down --remove-orphans || true
                    docker-compose pull
                    docker-compose up --abort-on-container-exit
                    echo 'Inference complete. Check ./output/alerts.csv'
                """
            }
            post {
                always {
                    echo 'Cleaning up compose containers...'
                    sh 'docker-compose down || true'
                }
                failure {
                    echo 'ERROR: Docker Compose run failed.'
                }
            }
        }
 
    } // end stages
 
    // ── Post-pipeline notifications ───────────────────────
    post {
        success {
            echo "Pipeline SUCCESS: Image ${DOCKER_HUB_USER}/${IMAGE_TAG} built, pushed, and run."
        }
        failure {
            echo 'Pipeline FAILED. Review stage logs above for details.'
        }
        always {
            archiveArtifacts artifacts: 'output/alerts.csv',
                             allowEmptyArchive: true
            echo 'Pipeline execution finished.'
        }
    }
}
