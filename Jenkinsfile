pipeline {
    agent any

    environment {
        DOCKER_USER = credentials('docker-username')
        DOCKER_TOKEN = credentials('docker-password')
        IMAGE_NAME = 'mdjiyaulhaq/food-nepal:latest'
    }

    stages {

        stage('Docker Login') {
            steps {
                sh """
                    echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin
                """
            }
        }

        stage('Run Linter') {
            steps {
                sh 'docker compose run --rm web sh -c "flake8"'
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                    docker compose run --rm web sh -c "while ! pg_isready -h db -p 5432 -U myuser; do sleep 1; done && pytest"
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker push $IMAGE_NAME'
            }
        }
    }
}


