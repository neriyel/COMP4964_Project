# Quick Start Guide

## 30-Second Summary

This project demonstrates **Infrastructure as Code + Jenkins automation** for a serverless data pipeline.

**The Flow:**
```
Git Push → Jenkins → SAM Build/Deploy → AWS (S3 + Lambda) → Auto-processes CSV
```

---

## Get Started in 5 Minutes

### Step 1: Prerequisites (1 min)
```bash
# Install AWS CLI & SAM
pip install aws-sam-cli awscli

# Configure AWS (us-west-2 region)
aws configure
# Enter your AWS Access Key ID & Secret Access Key
# Default region: us-west-2
```
### Step 2: Create S3 Deploy Bucket (1 min)
```bash
$ACCOUNT_ID = aws sts get-caller-identity --query Account --output text
$BUCKET_NAME = "jenkins-sam-artifacts-$ACCOUNT_ID"
aws s3 mb s3://$BUCKET_NAME --region us-west-2
``` s3 mb s3://jenkins-sam-artifacts-${ACCOUNT_ID}
```
### Step 3: Deploy Manually (2 min)
```bash
# In project directory
sam build
sam deploy --guided

# Follow prompts:
# Stack Name: data-pipeline-stack
# Region: us-west-2
# Capabilities: Y (for IAM)
```apabilities: Y (for IAM)
```

### Step 4: Test (1 min)
```bash
# Get bucket names
STACKS=$(aws cloudformation describe-stacks --stack-name data-pipeline-stack --query 'Stacks[0].Outputs')
INPUT_BUCKET=$(echo $STACKS | jq -r '.[0].OutputValue')

# Upload test CSV
aws s3 cp sample_data.csv s3://${INPUT_BUCKET}/uploads/

# Check output bucket after 30 seconds
aws s3 ls s3://<output-bucket>/processed/
```

---

## For Jenkins Integration

1. **Setup Jenkins** with Pipeline support
2. **Add GitHub repo** to Jenkins
3. **Create Pipeline job** pointing to `Jenkinsfile`
4. **Click "Build Now"**

Jenkins will automatically:
- Checkout code
- Run `sam build`
- Run `sam deploy`
- Output success message

---

## File Structure

```
├── template.yaml           # ← Infrastructure (SAM/CloudFormation)
├── Jenkinsfile            # ← Pipeline automation
├── src/
│   ├── lambda_handler.py  # ← Processing logic
│   └── requirements.txt
├── sample_data.csv        # ← Test file
├── README.md              # ← Full documentation
├── PRESENTATION_NOTES.md  # ← Presentation script
└── AWS_SETUP_GUIDE.md     # ← Detailed AWS setup
```

---

## Key Files Explained

### `template.yaml`
Defines all AWS infrastructure:
- ✅ S3 input/output buckets
- ✅ Lambda function
- ✅ IAM permissions
- ✅ S3 event triggers

**This is Infrastructure as Code!**

### `Jenkinsfile`
Jenkins pipeline with 5 stages:
1. Checkout code from GitHub
2. Build Lambda function
3. Package for deployment
4. Deploy to AWS (CloudFormation)
5. Validate success

### `src/lambda_handler.py`
Lambda function that:
- Reads CSV from S3
- Removes duplicates
- Removes empty rows
- Trims whitespace
- Writes processed CSV to output bucket

---

## Presentation Quick Reference

**Main Points:**
- ✅ Infrastructure as Code (template.yaml)
- ✅ Automated Deployment (Jenkins + SAM)
- ✅ Serverless (Lambda + S3)
- ✅ Event-Driven (S3 triggers Lambda)
- ✅ DevOps Best Practices

**Demo Steps:**
1. Show code in GitHub
2. Trigger Jenkins build
3. Watch pipeline execute
4. Upload CSV to S3
5. Show processed output

**Why It's DevOps:**
- Entire infrastructure in code
- Automated from commit to production
- Reproducible deployment
- Scalable serverless
- CloudWatch monitoring

---

## FAQ

**Q: Do I need a Jenkins server?**
A: No. You can deploy manually using SAM CLI, or use GitHub Actions instead.

**Q: How much does this cost?**
A: ~$0.25/month for typical usage (pay per Lambda invocation + S3 storage).

**Q: Can I modify the data processing?**
A: Yes, edit `src/lambda_handler.py` and commit. Pipeline redeploys automatically.

**Q: What if the pipeline fails?**
A: Check Jenkins logs for details. CloudFormation rollback on failure.

**Q: How do I delete everything?**
A: `aws cloudformation delete-stack --stack-name data-pipeline-stack`

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| SAM not found | `pip install aws-sam-cli` |
| AWS credentials error | Run `aws configure` |
| Bucket already exists | Use unique name: `s3://jenkins-sam-artifacts-$(date +%s)` |
| Lambda not triggered | Check CloudWatch: `aws logs tail /aws/lambda/csv-processor-dev --follow` |

---

## Next Steps

1. Read `README.md` for full details
2. Check `AWS_SETUP_GUIDE.md` for AWS prerequisites
3. Review `PRESENTATION_NOTES.md` for presentation script
4. Deploy and test!

**Questions?** See `README.md` for comprehensive documentation.
