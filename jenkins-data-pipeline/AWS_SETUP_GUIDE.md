# AWS Prerequisites & Setup Guide

## Prerequisites Before Running the Pipeline

### 1. AWS Account Setup

```bash
# Configure AWS CLI with your credentials
aws configure
# Enter:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region: us-east-1
# - Default output format: json

# Verify credentials work
aws sts get-caller-identity
```

### 2. Create S3 Bucket for SAM Artifacts

```bash
# Get your AWS Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create S3 bucket for packaged SAM artifacts
aws s3 mb s3://jenkins-sam-artifacts-${ACCOUNT_ID} --region us-west-2

# Enable versioning (optional but recommended)
aws s3api put-bucket-versioning \
    --bucket jenkins-sam-artifacts-${ACCOUNT_ID} \
    --versioning-configuration Status=Enabled
```

**Note this bucket name!** You'll need it in the Jenkinsfile.

### 3. Install Required Tools

#### SAM CLI
```bash
# macOS
brew install aws-sam-cli

# Windows (using Chocolatey)
choco install aws-sam-cli

# Linux or universal
pip install --user aws-sam-cli
```

#### AWS CLI
```bash
# Already included with SAM, but can install separately
pip install awscli --upgrade
```

#### Docker (Optional but Recommended)
SAM can use Docker to build Lambda functions in isolated environments.
- Download: https://www.docker.com/products/docker-desktop

### 4. Jenkins IAM Permissions

Your Jenkins server (or Jenkins user/role) needs these IAM permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "cloudformation:CreateStack",
                "cloudformation:UpdateStack",
                "cloudformation:DeleteStack",
                "cloudformation:DescribeStacks",
                "cloudformation:DescribeStackEvents"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "lambda:CreateFunction",
                "lambda:UpdateFunctionCode",
                "lambda:DeleteFunction",
                "lambda:GetFunction",
                "lambda:ListFunctions"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:CreateBucket",
                "s3:ListBucket",
                "s3:DeleteBucket"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:CreateRole",
                "iam:PutRolePolicy",
                "iam:DeleteRole",
                "iam:PassRole"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}
```

### 5. Jenkins Configuration

#### Install Required Plugins
1. Go to **Manage Jenkins** → **Plugin Manager**
2. Install:
   - Pipeline
   - GitHub Integration (if using GitHub)
   - AWS Steps (optional)
   - CloudBees AWS Credentials (optional)

#### Add AWS Credentials
1. **Manage Jenkins** → **Manage Credentials** → **System**
2. **Add Credentials** → AWS Credentials
3. Fill in:
   - Access Key ID: Your AWS access key
   - Secret Access Key: Your AWS secret key
   - Scope: Global

#### Update Jenkinsfile Variables
Edit `Jenkinsfile` with your values:

```groovy
environment {
    AWS_REGION = 'us-east-1'                    # Your region
    STACK_NAME = 'data-pipeline-stack'          # Stack name
    AWS_CREDENTIALS = 'your-aws-creds-id'       # Jenkins creds ID
    S3_DEPLOY_BUCKET = 'jenkins-sam-artifacts-YOUR_ACCOUNT_ID'  # Your bucket
}
```

### 6. Test SAM Locally (Optional)

```bash
# Navigate to project directory
cd jenkins-data-pipeline

# Build locally
sam build

# Test Lambda function with sample event
sam local invoke CSVProcessorFunction -e events/s3_event.json

# Start local API Gateway (if configured)
sam local start-api
```

### 7. GitHub Repository Setup

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Jenkins data pipeline"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/jenkins-data-pipeline.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 8. Jenkins GitHub Integration (Optional)

If using GitHub webhooks:

1. Go to your GitHub repo → **Settings** → **Webhooks**
2. Click **Add webhook**
3. Payload URL: `https://your-jenkins-server/github-webhook/`
4. Content type: `application/json`
5. Trigger on: Push events
6. Active: ✓

---

## Manual Deployment (Without Jenkins)

If you want to test deployment without Jenkins:

```bash
# 1. Build
sam build

# 2. Package
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket jenkins-sam-artifacts-${ACCOUNT_ID} \
    --region us-west-2

# 3. Deploy
sam deploy \
    --template-file packaged.yaml \
    --stack-name data-pipeline-stack \
    --region us-west-2 \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides Environment=dev

# 4. Get outputs
aws cloudformation describe-stacks \
    --stack-name data-pipeline-stack \
    --query 'Stacks[0].Outputs' \
    --output table
```

---

## Troubleshooting

### "sam: command not found"
```bash
# Install SAM CLI
pip install aws-sam-cli

# Or verify installation
sam --version
```

### "Unable to locate credentials"
```bash
# Check AWS credentials are configured
aws sts get-caller-identity

# Or set credentials explicitly
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
```

### "S3 bucket already exists"
```bash
# Bucket names must be globally unique in AWS
# Use your account ID and timestamp
BUCKET_NAME="jenkins-sam-artifacts-$(date +%s)"
aws s3 mb s3://${BUCKET_NAME}
```

### "CloudFormation stack already exists"
```bash
# To update existing stack instead of creating
sam deploy --stack-name data-pipeline-stack

# To delete and recreate
aws cloudformation delete-stack --stack-name data-pipeline-stack
```

### "Lambda function not triggered"
```bash
# Check S3 event notification
aws s3api get-bucket-notification-configuration \
    --bucket data-pipeline-input-ACCOUNT_ID-dev

# Check Lambda permissions
aws lambda get-policy \
    --function-name csv-processor-dev \
    --query Policy \
    --output text | jq .
```

---

## Cost Estimation

Typical monthly costs for this pipeline:

| Service | Usage | Cost |
|---------|-------|------|
| S3 | 1GB stored | $0.023 |
| Lambda | 1M invocations | ~$0.20 |
| CloudFormation | Deployments only | Free |
| Data Transfer | <1GB | Free (within region) |
| **Total** | Minimal usage | **~$0.25/month** |

*Costs vary by region and usage. Use [AWS Pricing Calculator](https://calculator.aws/)*

---

## Environment Variables

Key environment variables used throughout the pipeline:

```bash
# AWS Configuration
AWS_REGION              # AWS region (default: us-east-1)
AWS_ACCESS_KEY_ID       # AWS credentials
AWS_SECRET_ACCESS_KEY   # AWS credentials

# Jenkins Configuration
STACK_NAME              # CloudFormation stack name
S3_DEPLOY_BUCKET        # Bucket for SAM artifacts
ENVIRONMENT             # Deployment environment (dev/prod)

# Lambda Configuration
INPUT_BUCKET            # Input S3 bucket
OUTPUT_BUCKET           # Output S3 bucket
PROCESSED_PREFIX        # Prefix for processed files
```

---

## Next Steps

1. ✅ Complete AWS prerequisites above
2. ✅ Configure Jenkins
3. ✅ Push code to GitHub
4. ✅ Create Jenkins pipeline job
5. ✅ Trigger pipeline
6. ✅ Test with sample CSV
7. ✅ Monitor CloudWatch logs
8. ✅ Iterate and customize

**Ready to deploy?** Create a Jenkins job pointing to your GitHub repository and trigger the pipeline!
