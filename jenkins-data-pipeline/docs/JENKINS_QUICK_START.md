# Jenkins for Presentation - Quick Start

## ⚡ 5-Minute Jenkins Setup

### Step 1: Install Docker Desktop (if you don't have it)
Download from: https://www.docker.com/products/docker-desktop

Once installed, verify it's working:
```powershell
docker --version
```

### Step 2: Start Jenkins (Copy & Paste This)

```powershell
# Create storage volume
docker volume create jenkins_home

# Start Jenkins container
docker run -d `
  --name jenkins `
  -p 8080:8080 `
  -p 50000:50000 `
  -v jenkins_home:/var/jenkins_home `
  -v /var/run/docker.sock:/var/run/docker.sock `
  jenkins/jenkins:lts
```

### Step 3: Wait for Jenkins to Start
```powershell
# Watch the logs (wait for "Jenkins is fully up and running")
docker logs -f jenkins

# When you see "Jenkins is fully up and running", press Ctrl+C
```

### Step 4: Get Admin Password
```powershell
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
Copy the output (that's your password).

### Step 5: Access Jenkins
1. Open browser: `http://localhost:8080`
2. Paste the password from Step 4
3. Click "Continue"
4. Select "Install suggested plugins"
5. Create admin user (remember these credentials!)
6. Click "Save and Finish"

---

## ✅ Configure for Your Project (5 minutes)

### Step 1: Add AWS Credentials
1. **Manage Jenkins** → **Manage Credentials** → **System** → **Global credentials**
2. **Add Credentials**:
   - Kind: `AWS Credentials`
   - ID: `aws-credentials`
   - Access Key ID: (from your AWS account)
   - Secret Access Key: (from your AWS account)
3. **Create**

### Step 2: Create the Pipeline Job
1. Click **New Item**
2. Name: `data-pipeline-job`
3. Select: **Pipeline**
4. **OK**

### Step 3: Configure the Pipeline
In the "Pipeline" section:
1. Definition: `Pipeline script from SCM`
2. SCM: `Git`
3. Repository URL: `https://github.com/YOUR_USERNAME/YOUR_REPO.git`
4. Branch: `*/main`
5. Script Path: `jenkins-data-pipeline/Jenkinsfile`
6. **Save**

---

## 🎬 Run Your First Build

1. Click on `data-pipeline-job`
2. Click **Build Now**
3. Watch the magic happen! ✨

The pipeline will:
1. ✅ Check out code from GitHub
2. ✅ Build the SAM template
3. ✅ Package the Lambda function
4. ✅ Deploy to AWS CloudFormation
5. ✅ Validate the deployment

---

## 📊 What Gets Created in AWS

When Jenkins finishes, you'll have:
- ✅ Lambda function: `csv-processor-dev`
- ✅ Input bucket: `data-pipeline-input-195275680578-dev`
- ✅ Output bucket: `data-pipeline-output-195275680578-dev`
- ✅ IAM role with S3 permissions
- ✅ S3 event configuration to auto-trigger Lambda

---

## 🧪 Test the Complete Pipeline

After Jenkins finishes deploying:

```powershell
# Upload a CSV to test
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
aws s3 cp sample_data.csv "s3://data-pipeline-input-195275680578-dev/uploads/test_$timestamp.csv" --region us-west-2

# Wait 5 seconds
Start-Sleep -Seconds 5

# Check if output file appeared
aws s3 ls s3://data-pipeline-output-195275680578-dev/processed/ --region us-west-2
```

You should see a processed CSV file appear! 🎉

---

## 📝 During Your Presentation

1. **Show the Jenkinsfile** - Explain the 5 stages
2. **Click "Build Now"** in Jenkins
3. **Narrate the stages** as they execute
4. **Show the CloudFormation outputs** - Prove resources were created
5. **Optional**: Upload a CSV to show event-driven triggering

See `JENKINS_DEMO_SCRIPT.md` for detailed presentation talking points!

---

## 🛑 Stop Jenkins When Done

```powershell
# Stop the container
docker stop jenkins

# Start it again later with:
docker start jenkins

# To completely remove (deletes saved data):
docker rm jenkins
docker volume rm jenkins_home
```

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| Jenkins won't start | Check Docker is running: `docker ps` |
| Can't access http://localhost:8080 | Wait another 30 seconds and refresh |
| Build fails on "Checkout" | Check GitHub credentials in Jenkins |
| Build fails on "Deploy" | Verify AWS credentials in Jenkins |
| Can't find admin password | Run: `docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword` |

---

## 🎯 That's It!

You now have a fully automated CI/CD pipeline ready for your presentation. Jenkins will orchestrate everything - from checking out your code to deploying to AWS - all from a single "Build Now" click.

For more details, see:
- `JENKINS_SETUP_GUIDE.md` - Detailed setup with all options
- `JENKINS_DEMO_SCRIPT.md` - Full presentation script with talking points
- `QUICKSTART.md` - General project quick start
