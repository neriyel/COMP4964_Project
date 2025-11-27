FROM jenkins/jenkins:lts

USER root

# Install Docker CLI, Python, and pip
RUN apt-get update && \
    apt-get install -y docker.io python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest (allow system-wide install)
RUN pip3 install --break-system-packages pytest

# Add jenkins user to docker group
RUN usermod -aG docker jenkins

USER jenkins

# Create groovy init script to set admin password
RUN mkdir -p $JENKINS_HOME/init.groovy.d
COPY init.groovy $JENKINS_HOME/init.groovy.d/

# Skip setup wizard
ENV JENKINS_OPTS="-Djenkins.install.runSetupWizard=false"
