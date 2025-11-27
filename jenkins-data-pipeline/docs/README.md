# Jenkins Data Pipeline Demo
## Automating Infrastructure with Jenkins, AWS SAM, and Lambda

> **🎯 FOR YOUR PRESENTATION:** Start with `START_HERE_JENKINS.md` to get Jenkins running and presentation-ready!

This project demonstrates a complete DevOps data pipeline automation using **Infrastructure as Code (IAC)** principles.

---

## ⚡ Quick Start: Get Jenkins Running (5 minutes)

**New to Jenkins?** Follow this quick start guide:

```powershell
# 1. Install Docker Desktop from https://www.docker.com/products/docker-desktop

# 2. Start Jenkins (copy-paste all at once):
docker volume create jenkins_home
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 `
  -v jenkins_home:/var/jenkins_home `
  -v /var/run/docker.sock:/var/run/docker.sock `
  jenkins/jenkins:lts

# 3. Get admin password:
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# 4. Open browser to http://localhost:8080 and login
```

📖 **Full guide:** See `JENKINS_QUICK_START.md` in this directory

---

## 🎬 Using Jenkins for Your Presentation

We've created **4 comprehensive Jenkins guides** for your presentation:

1. **`JENKINS_QUICK_START.md`** ⚡ - 5-minute Docker setup
2. **`JENKINS_SETUP_GUIDE.md`** 📚 - Detailed configuration with all options
3. **`JENKINS_DEMO_SCRIPT.md`** 🎤 - Presentation talking points & Q&A
4. **`JENKINS_PRESENTATION_CHECKLIST.md`** ✅ - Pre-presentation checklist

**Start here:** `JENKINS_QUICK_START.md`

---

## 📋 Architecture Overview

```
Developer pushes code → GitHub  
       ↓  
Jenkins Pipeline triggers  
       ↓  
Jenkins runs "sam build" & "sam deploy"  
       ↓  
AWS CloudFormation creates resources:
   - S3 Input Bucket
   - S3 Output Bucket
   - Lambda Function
   - S3 Event Trigger
       ↓  
User uploads CSV → S3 Input Bucket  
       ↓  
Lambda automatically processes and outputs cleaned CSV
```

---

## 🎯 Key Concepts

### Infrastructure as Code (IaC)
- **SAM (Serverless Application Model)**: AWS's framework for defining serverless infrastructure
- **template.yaml**: Defines all AWS resources declaratively
- **Benefits**: Version control, reproducibility, automated deployment

### Automation Components
- **Jenkins**: Orchestrates the pipeline
- **AWS SAM**: Builds and deploys serverless applications
- **CloudFormation**: Creates and manages AWS resources
- **AWS Lambda**: Serverless compute for processing

---

## 📁 Project Structure

```
jenkins-data-pipeline/
├── template.yaml              # SAM template (Infrastructure as Code)
├── Jenkinsfile               # Jenkins pipeline configuration
├── src/
│   ├── lambda_handler.py     # Lambda function code
│   └── requirements.txt       # Python dependencies
├── sample_data.csv           # Test data
└── README.md                 # This file
```

---

## 🚀 Step-by-Step Setup Guide

### Prerequisites
- AWS Account with appropriate permissions
- Jenkins server configured
- AWS CLI and SAM CLI installed
- Git repository (GitHub)
- Python 3.9+

### Step 1: Prepare Your GitHub Repository

1. Create a new GitHub repository or clone this project
2. Push all files to your repository
3. Ensure Jenkins has access to your GitHub repo (via SSH key or token)

### Step 2: Configure Jenkins

#### Create Jenkins Credentials
1. Go to **Manage Jenkins** → **Manage Credentials**
2. Add AWS credentials:
   - Username: AWS Access Key ID
   - Password: AWS Secret Access Key
3. Add GitHub credentials if using private repos

#### Update Jenkinsfile (if needed)
Update these environment variables:
```groovy
AWS_REGION = 'us-west-2'          # Your preferred region
STACK_NAME = 'data-pipeline-stack' # CloudFormation stack name
S3_DEPLOY_BUCKET = 'your-deploy-bucket'  # For packaged SAM artifacts
```

#### Create Jenkins Job
1. New Item → Pipeline
2. Name: "data-pipeline"
3. Pipeline → Definition → Pipeline script from SCM
4. SCM: Git
5. Repository URL: Your GitHub repo URL
6. Branch: */main (or your branch)
7. Script Path: Jenkinsfile

### Step 3: Configure AWS (Manual Setup)

Before pipeline deployment, ensure you have:

```bash
# Create S3 bucket for SAM artifacts (for packaged.yaml)
aws s3 mb s3://jenkins-sam-artifacts-$(aws sts get-caller-identity --query Account --output text)

# Verify IAM permissions for Lambda, S3, CloudFormation, IAM
# (Jenkins EC2 instance or user needs these permissions)
```

### Step 4: Run the Pipeline

1. Go to your Jenkins job
2. Click **Build Now**
3. Monitor the pipeline stages:
   - **Checkout**: Pulls code from GitHub
   - **Build**: Runs `sam build`
   - **Package**: Creates deployment package
   - **Deploy**: Runs `sam deploy` to CloudFormation
   - **Post-Deploy Validation**: Outputs AWS resource names

### Step 5: Test the Data Pipeline

Once deployed, test the pipeline:

```bash
# Get bucket names from CloudFormation outputs
aws cloudformation describe-stacks \
    --stack-name data-pipeline-stack \
    --region us-west-2 \
    --query 'Stacks[0].Outputs' \
    --output table

# Upload sample CSV to input bucket
aws s3 cp sample_data.csv s3://<INPUT_BUCKET>/uploads/sample_data.csv --region us-west-2

# Wait 10-30 seconds for Lambda to process
# Check output bucket for processed file
aws s3 ls s3://<OUTPUT_BUCKET>/processed/ --region us-west-2

# Download and verify processed file
aws s3 cp s3://<OUTPUT_BUCKET>/processed/20240525_143022_sample_data.csv . --region us-west-2
```

---

## 🔍 What Each Component Does

### template.yaml (Infrastructure as Code)
- **Defines all AWS resources** in YAML format
- **S3 Buckets**: 
  - Input bucket (receives raw CSVs)
  - Output bucket (stores processed CSVs)
- **Lambda Function**: 
  - Reads CSV from S3
  - Cleans/deduplicates data
  - Writes processed CSV to output bucket
- **IAM Role**: Grants Lambda permissions to read/write S3
- **S3 Event Trigger**: Automatically invokes Lambda when CSV uploaded

### lambda_handler.py (Processing Logic)
- **Triggered** automatically when file uploaded to input bucket
- **Operations**:
  - Reads CSV from S3
  - Removes duplicates
  - Trims whitespace
  - Removes empty rows
  - Validates data
- **Output**: Timestamped cleaned CSV in output bucket

### Jenkinsfile (Pipeline Automation)
1. **Checkout**: Gets latest code from GitHub
2. **Build**: Runs `sam build` to prepare Lambda function
3. **Package**: Creates deployment package stored in S3
4. **Deploy**: Executes `sam deploy` using CloudFormation
5. **Validation**: Confirms successful deployment

---

## 💡 Why This Is DevOps

✅ **Infrastructure as Code**: All AWS resources defined in YAML  
✅ **Automated Deployment**: Jenkins pipeline handles entire deployment  
✅ **Scalability**: Serverless scales automatically  
✅ **Repeatability**: Same deployment every time  
✅ **Version Control**: Infrastructure tracked in Git  
✅ **CI/CD Integration**: Changes trigger automated pipeline  
✅ **Cloud-Native**: Leverages AWS managed services  

---

## 🔧 Customization Options

### Modify Processing Logic
Edit `src/lambda_handler.py`:
```python
def process_csv_data(data):
    # Add custom transformation logic here
    # Examples:
    # - Data validation
    # - Format conversion (CSV to JSON, Parquet, etc.)
    # - Data enrichment
    # - Machine learning predictions
```

### Add More AWS Resources
Edit `template.yaml`:
```yaml
Resources:
  # Add CloudWatch alarms, SNS notifications, DynamoDB tables, etc.
```

### Change Trigger Conditions
Edit `template.yaml` S3 event filter:
```yaml
Events:
  S3UploadEvent:
    Properties:
      Filter:
        Key:
          Rules:
            - Name: prefix
              Value: uploads/        # Only trigger for files in this path
            - Name: suffix
              Value: .csv            # Only trigger for CSV files
```

---

## 📊 Monitoring & Logging

### CloudWatch Logs
```bash
# View Lambda logs
aws logs tail /aws/lambda/csv-processor-dev --follow

# View specific invocation
aws logs filter-log-events \
    --log-group-name /aws/lambda/csv-processor-dev \
    --filter-pattern "Error"
```

### CloudFormation Events
```bash
# Monitor stack creation/updates
aws cloudformation describe-stack-events \
    --stack-name data-pipeline-stack \
    --query 'StackEvents[0:10]' \
    --output table
```

### Jenkins Logs
- Available in Jenkins UI under each build
- Shows `sam build` and `sam deploy` output

---

## 🧪 Testing Locally (Optional)

Test Lambda function locally before deployment:

```bash
# Install SAM CLI if not already installed
pip install aws-sam-cli

# Build the project
sam build

# Test with local event
sam local invoke CSVProcessorFunction \
    -e events/s3_event.json
```

Create `events/s3_event.json` with sample S3 event for testing.

---

## ❌ Troubleshooting

| Issue | Solution |
|-------|----------|
| **Jenkins can't access GitHub** | Add SSH key or GitHub token to Jenkins credentials |
| **SAM build fails** | Ensure Python 3.9+ installed, `pip install -r requirements.txt` |
| **Deployment fails** | Check IAM permissions for CloudFormation, S3, Lambda, IAM |
| **Lambda doesn't trigger** | Verify S3 event notification configuration in CloudFormation stack |
| **CSV not processed** | Check CloudWatch Logs: `aws logs tail /aws/lambda/csv-processor-dev --follow` |

---

## 📚 Additional Resources

- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Infrastructure as Code (IaC) Guide](https://www.terraform.io/intro)

---

## 🎓 Presentation Talking Points

1. **DevOps Philosophy**: Automation, infrastructure as code, CI/CD
2. **SAM Framework**: Simplifies serverless deployment
3. **Jenkins Role**: Orchestrates automated deployment pipeline
4. **AWS Services**: S3, Lambda, CloudFormation, IAM
5. **Real-world Applications**:
   - Log processing pipelines
   - Data transformation and ETL
   - Real-time stream processing
   - Image/document processing
6. **Cost Benefits**: Pay only for what you use (serverless)
7. **Scalability**: Automatic horizontal scaling

---

## 📝 Demo Script

**Time: 5-10 minutes**

### Part 1: Code Push (30 seconds)
```bash
git add .
git commit -m "Data pipeline update"
git push origin main
```

### Part 2: Pipeline Execution (3-5 minutes)
- Show Jenkins Job triggered automatically
- Walk through each stage:
  - Checkout
  - Build
  - Package
  - Deploy
  - Validation

### Part 3: Manual Test (2-3 minutes)
```bash
# Upload sample CSV
aws s3 cp sample_data.csv s3://<bucket>/uploads/

# Show Lambda triggered (check CloudWatch)
# Download processed CSV
aws s3 cp s3://<output-bucket>/processed/... .
```

### Part 4: Q&A
- Infrastructure as Code benefits
- Lambda advantages
- Jenkins automation
- Cost efficiency

---

**Created for COMP4964 Term Project**
