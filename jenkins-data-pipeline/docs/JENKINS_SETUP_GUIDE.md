# Jenkins Setup Guide for Data Pipeline Presentation

## Overview
This guide walks you through setting up Jenkins locally to run the data pipeline CI/CD automation. Jenkins will handle the build, package, and deploy stages shown in the presentation.

---

## Option 1: Jenkins with Docker (Recommended for Windows)

### Prerequisites
- Docker Desktop installed and running ([Download here](https://www.docker.com/products/docker-desktop))
- AWS credentials configured locally
- Git installed

### Step 1: Create Jenkins Docker Container

Run this PowerShell command:

```powershell
# Create a Docker volume to persist Jenkins data
docker volume create jenkins_home

# Run Jenkins container with Docker-in-Docker capability
docker run -d `
  --name jenkins `
  -p 8080:8080 `
  -p 50000:50000 `
  -v jenkins_home:/var/jenkins_home `
  -v /var/run/docker.sock:/var/run/docker.sock `
  -e JENKINS_OPTS="--httpPort=8080" `
  jenkins/jenkins:lts
```

### Step 2: Wait for Jenkins to Start

```powershell
# Check Jenkins logs until you see "Jenkins is fully up and running"
docker logs -f jenkins
```

Once you see "Jenkins is fully up and running", press Ctrl+C to exit logs.

### Step 3: Get Initial Admin Password

```powershell
# Extract the initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Copy this password - you'll need it next.

### Step 4: Access Jenkins Web UI

1. Open your browser and go to: `http://localhost:8080`
2. Paste the admin password from Step 3
3. Click "Continue"
4. Select "Install suggested plugins" (wait for installation to complete)
5. Create your first admin user (use credentials you'll remember)
6. Click "Save and Continue"
7. Keep Jenkins URL as `http://localhost:8080`
8. Click "Save and Finish"

---

## Step 5: Configure Jenkins for GitHub

### 5a. Install GitHub Integration Plugin

1. Go to **Manage Jenkins** → **Manage Plugins**
2. Search for "GitHub Integration"
3. Check the checkbox and click "Download now and install after restart"
4. Wait for restart (Jenkins will reload)

### 5b. Create GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token"
3. Name it: `Jenkins-Pipeline`
4. Select scopes:
   - `repo` (full control of private repositories)
   - `admin:repo_hook` (write access to hooks)
5. Click "Generate token"
6. **Copy the token** (you won't see it again)

### 5c. Add GitHub Credentials to Jenkins

1. Go to **Manage Jenkins** → **Manage Credentials**
2. Click "System" → "Global credentials (unrestricted)"
3. Click "Add Credentials" (top left)
4. Fill in:
   - Kind: `Username with password`
   - Username: your GitHub username
   - Password: paste the personal access token from 5b
   - ID: `github-credentials`
   - Description: `GitHub Token for Jenkins`
5. Click "Create"

---

## Step 6: Create Jenkins Pipeline Job

### 6a. Create New Job

1. Click "New Item" on Jenkins home page
2. Enter name: `data-pipeline-job`
3. Select "Pipeline"
4. Click "OK"

### 6b. Configure Pipeline

1. Scroll to "Pipeline" section
2. Select "Pipeline script from SCM"
3. Choose SCM: `Git`
4. Fill in:
   - Repository URL: `https://github.com/YOUR_USERNAME/COMP4964_term_project.git`
   - Credentials: select `github-credentials` from dropdown
   - Branch Specifier: `*/main` (or your default branch)
   - Script Path: `jenkins-data-pipeline/Jenkinsfile`
5. Click "Save"

### 6c. Test the Pipeline

1. Click "Build Now" on the job page
2. Watch the build progress in the console output
3. See stages: Checkout → Build → Package → Deploy → Validate

---

## Step 7: Configure AWS Credentials in Jenkins

### 7a. Create AWS Access Key (if you don't have one)

1. Go to AWS Console → IAM → Users → your user
2. Click "Security credentials" tab
3. Click "Create access key"
4. Choose "Command Line Interface (CLI)"
5. Click through to download the CSV file
6. **Keep this safe** - don't commit to Git

### 7b. Add AWS Credentials to Jenkins

1. Go to **Manage Jenkins** → **Manage Credentials**
2. Click "System" → "Global credentials (unrestricted)"
3. Click "Add Credentials"
4. Fill in:
   - Kind: `AWS Credentials`
   - ID: `aws-credentials`
   - Access Key ID: (from CSV file)
   - Secret Access Key: (from CSV file)
   - Description: `AWS Credentials for Data Pipeline`
5. Click "Create"

### 7c. Update Jenkinsfile with Credentials

Edit `jenkins-data-pipeline/Jenkinsfile` and add this at the top of the pipeline block (after `agent any`):

```groovy
    credentials {
        aws('aws-credentials')
    }
```

This tells Jenkins to automatically load AWS credentials during the build.

---

## Step 8: Set Up GitHub Webhook (Optional but Recommended)

### 8a. Create Jenkins Webhook Token

1. In Jenkins, go to your `data-pipeline-job` → Configure
2. Check "GitHub hook trigger for GITScm polling"
3. Click "Save"

### 8b. Add Webhook to GitHub

1. Go to your GitHub repo → Settings → Webhooks
2. Click "Add webhook"
3. Fill in:
   - Payload URL: `http://YOUR_PUBLIC_IP:8080/github-webhook/`
   - Content type: `application/json`
   - Events: `Push events` and `Pull requests`
4. Click "Add webhook"

**Note:** If Jenkins is on localhost, you'll need to use a tunnel service like ngrok for GitHub to reach it.

---

## Running the Pipeline for Your Presentation

### Quick Demo (1 minute)

1. Open Jenkins at `http://localhost:8080`
2. Click your `data-pipeline-job`
3. Click "Build Now"
4. Watch the stages execute in real-time:
   - **Checkout**: Pulls code from GitHub
   - **Build**: Runs `sam build` (creates CloudFormation template)
   - **Package**: Runs `sam package` (prepares artifacts for AWS)
   - **Deploy**: Runs `sam deploy` (creates/updates AWS resources)
   - **Validate**: Shows CloudFormation stack outputs

### Test CSV Upload During Demo (2 minutes)

After Jenkins completes the deploy:

```powershell
# Upload a test CSV to trigger the Lambda
aws s3 cp sample_data.csv s3://data-pipeline-input-195275680578-dev/uploads/demo_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv --region us-west-2

# Wait 10 seconds, then check output bucket
aws s3 ls s3://data-pipeline-output-195275680578-dev/processed/ --region us-west-2
```

This demonstrates the complete pipeline:
- Jenkins builds & deploys infrastructure
- S3 upload triggers Lambda
- CSV is processed automatically

---

## Troubleshooting

### Jenkins won't start
```powershell
# Check Docker container status
docker ps

# View Jenkins logs
docker logs jenkins

# Restart Jenkins
docker restart jenkins
```

### Build fails with "sh: command not found"
The Jenkinsfile uses `sh` commands (Linux shell). For Windows, you need to either:
- Run Jenkins in Docker (recommended) ✓ Handles this automatically
- Or use Windows PowerShell agent (more complex)

### AWS credentials not working
1. Verify credentials in **Manage Jenkins** → **Manage Credentials**
2. Check that `aws-credentials` ID matches in Jenkinsfile
3. Ensure AWS IAM user has `cloudformation:*` and `s3:*` permissions

### GitHub webhook not triggering builds
1. Verify Jenkins is accessible from GitHub (may need ngrok for localhost)
2. Check webhook delivery status in GitHub repo settings
3. For testing without webhook, click "Build Now" manually

---

## Stopping Jenkins

When you're done with the presentation:

```powershell
# Stop the Jenkins container
docker stop jenkins

# Remove the container (optional)
docker rm jenkins

# Remove the volume (optional, keeps data if you comment this out)
docker volume rm jenkins_home
```

---

## Key Points for Your Presentation

1. **Show the Jenkinsfile** - Explain the 5 stages (Checkout → Build → Package → Deploy → Validate)
2. **Click "Build Now"** - Let Jenkins run through the pipeline automatically
3. **Show CloudFormation outputs** - Prove AWS resources were created
4. **Upload test CSV** - Demonstrate event-driven Lambda triggering
5. **Show output file** - Validate data was processed

This demonstrates:
- ✅ Infrastructure as Code (Jenkinsfile + SAM template)
- ✅ Automated CI/CD (Jenkins orchestrates everything)
- ✅ AWS integration (CloudFormation + Lambda + S3)
- ✅ Event-driven serverless (S3 → Lambda automation)

---

## Next Steps

1. Install Docker Desktop if you don't have it
2. Run the Jenkins Docker command from Step 1
3. Follow the setup steps to configure GitHub and AWS
4. Test by clicking "Build Now"
5. During presentation, show the pipeline executing in real-time

Good luck with your presentation! 🚀
