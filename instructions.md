## Project Overview

This project involves forecasting using machine learning techniques, with an infrastructure setup that includes containerization and continuous integration/deployment. Below are the key components and setup details:

### 1. Development

- **Forecasting Model**: Developed a forecasting model using Facebook's Prophet and Statsmodels. This involved writing Python code to analyze and predict time-series data.
- **MLflow**: Utilized MLflow for experiment tracking and artifact management, enhancing the reproducibility and transparency of the forecasting experiments.

### 2. Containerization

- **Docker**: Created a Dockerfile to containerize the forecasting application. This allows the application to run consistently across different computing environments.

### 3. Continuous Integration/Deployment (CI/CD)

- **Jenkins Setup**: Opted to use Jenkins within a Docker container rather than a host installation. This approach simplifies the Jenkins setup and isolates the CI/CD tools from the host system.

#### Setup Commands:
```bash
apt-get update
apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
apt-get update
apt-get install -y docker-ce-cli
grep docker /etc/group
docker run -d -p 8080:8080 -p 50000:50000 \
    -v jenkins_home:/var/jenkins_home \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --group-add <host-docker-group-id> \
    --name jenkins jenkins/jenkins:lts
```
### 4. Jenkins Pipeline Configuration

- **Jenkinsfile**: Developed a Jenkinsfile to define the pipeline stages, which includes steps for building the Docker image, running tests, and pushing the image to a registry.
- **Credentials Setup**: Configured Jenkins with the necessary credentials for accessing the GitHub Container Registry, ensuring secure handling of access tokens and other sensitive data.

### 5. Usage Instructions

To pull and run the Docker image from the GitHub Container Registry:

```bash
echo "YOUR_PERSONAL_ACCESS_TOKEN" | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
docker pull ghcr.io/manansaxena/wastewater-forecast:latest
docker run -p 5000:5000 ghcr.io/manansaxena/wastewater-forecast:latest
```
