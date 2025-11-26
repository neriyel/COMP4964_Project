FROM jenkins/jenkins:lts

USER root

# Install Docker CLI
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

# Add jenkins user to docker group
RUN usermod -aG docker jenkins

USER jenkins

# Skip setup wizard and create initial admin user
ENV JENKINS_OPTS="-Djenkins.install.runSetupWizard=false -Djenkins.security.ApiTokenProperty.enableCompatibilityMode=true"
ENV JENKINS_USER=admin
ENV JENKINS_PASS=admin123

# Create groovy init script to set admin password
RUN mkdir -p $JENKINS_HOME/init.groovy.d
COPY init.groovy $JENKINS_HOME/init.groovy.d/
