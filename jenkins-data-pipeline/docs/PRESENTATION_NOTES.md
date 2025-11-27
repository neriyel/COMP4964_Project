# Jenkins Data Pipeline - Presentation Notes

## 5-Minute Presentation Script

### Opening (30 seconds)
"Today I'll demonstrate how Jenkins automates a serverless data pipeline using Infrastructure as Code. This addresses the DevOps aspect of pipeline automation while staying focused on data processing."

---

### Part 1: Architecture (1 minute)

**Show the flow diagram:**
```
Developer → GitHub → Jenkins → SAM/CloudFormation → AWS Resources → S3 Event → Lambda → Output
```

**Key Points:**
- **Developer Action**: Pushes code to GitHub
- **Jenkins Trigger**: Automatically detects code change
- **Infrastructure as Code**: SAM template defines all AWS resources
- **Serverless Resources**: Lambda + S3 + IAM (no servers to manage)
- **Automation**: Entire deployment happens without manual steps

---

### Part 2: Infrastructure as Code (1.5 minutes)

**What is IaC?**
- Define infrastructure in code (template.yaml)
- Reproducible: Deploy same infrastructure anywhere
- Version controlled: Track all changes
- Auditable: Know exactly what was deployed

**Our Template Includes:**
```
✓ 2 S3 Buckets (input for raw data, output for processed)
✓ Lambda Function (the processing logic)
✓ IAM Role (permissions for Lambda to access S3)
✓ S3 Event Trigger (automatically invoke Lambda on file upload)
```

**Why This Matters:**
- No clicking around AWS console
- Deploy to dev/prod consistently
- Rollback changes easily
- New team members understand infrastructure

---

### Part 3: The Pipeline (1.5 minutes)

**Walk through Jenkinsfile stages:**

1. **Checkout** (10 sec)
   - Gets latest code from GitHub
   - Runs every time code pushed

2. **Build** (20 sec)
   - Runs `sam build`
   - Prepares Lambda function
   - Validates template syntax

3. **Package** (20 sec)
   - Runs `sam package`
   - Creates deployment artifact
   - Stores in S3

4. **Deploy** (30 sec)
   - Runs `sam deploy`
   - CloudFormation creates/updates resources
   - Sets up S3 buckets, Lambda, IAM, triggers

5. **Validate** (10 sec)
   - Confirms deployment successful
   - Shows output bucket names

---

### Part 4: Live Demo (1 minute - if time permits)

**Option A: Show Jenkins UI**
```
1. Click "Build Now" in Jenkins
2. Watch pipeline progress through stages
3. Show logs of sam build/deploy
4. Highlight successful deployment message
```

**Option B: Show Manual Test**
```bash
# Upload file to input bucket
aws s3 cp sample_data.csv s3://<bucket>/uploads/

# Wait for Lambda
# Show file appeared in output bucket
aws s3 ls s3://<output-bucket>/processed/
```

---

### Part 5: Key DevOps Concepts (1 minute)

**Why This Is DevOps:**

✅ **Automation** - Jenkins automates deployment  
✅ **Infrastructure as Code** - SAM template in Git  
✅ **CI/CD** - Code → Build → Deploy → Validate  
✅ **Reproducibility** - Same deployment every time  
✅ **Scalability** - Lambda scales automatically  
✅ **Monitoring** - CloudWatch logs all activity  
✅ **Version Control** - Everything in Git  

**The Data Processing Part:**
- Lambda function reads CSV from S3
- Cleans data (removes duplicates, whitespace, empty rows)
- Writes processed CSV to output bucket
- All triggered automatically

---

## Presentation Q&A Prep

**Q: Why Lambda instead of EC2?**
A: Serverless = no servers to manage, automatic scaling, pay only for execution time.

**Q: How is this different from a regular CI/CD pipeline?**
A: This deploys *infrastructure* (not just code). The infrastructure IS part of the automation.

**Q: What if the CSV is very large?**
A: Lambda has 15-minute timeout and 10GB memory limit. Could extend with Step Functions or Batch for larger files.

**Q: How much would this cost?**
A: Very little for small workloads. Pay per S3 API call and Lambda execution time.

**Q: What if deployment fails?**
A: Jenkins logs show exactly what failed. CloudFormation can rollback changes automatically.

**Q: Can this handle multiple file formats?**
A: Yes, modify `lambda_handler.py` to handle JSON, Parquet, Excel, etc.

**Q: How does the Lambda get triggered?**
A: S3 event notification (native AWS feature) → Lambda automatically invokes.

---

## Demo Talking Points

### Before Running Demo
"Notice everything is version-controlled in Git. We have:
- Infrastructure definition (template.yaml)
- Pipeline definition (Jenkinsfile)
- Application code (lambda_handler.py)
- Documentation (README.md)

This is Infrastructure as Code in action."

### During Pipeline Execution
"Each stage shows what's happening:
- **Build**: Lambda function verified
- **Package**: Creates ZIP file for deployment
- **Deploy**: CloudFormation creates all resources
- **Validate**: Confirms everything deployed correctly"

### During Data Processing
"The Lambda function:
1. Detected the S3 upload event automatically
2. Read the CSV file
3. Cleaned the data (removed duplicates, whitespace)
4. Wrote results to output bucket

No manual intervention needed!"

---

## Slide Suggestions

Slide 1: Title slide
- Jenkins Data Pipeline
- Automated Infrastructure Deployment
- COMP4964 Term Project

Slide 2: Architecture Diagram
- Show the flow: Dev → GitHub → Jenkins → AWS

Slide 3: What is Infrastructure as Code?
- template.yaml defines all resources
- Reproducible, versioned, auditable

Slide 4: Jenkins Pipeline Stages
- Checkout → Build → Package → Deploy → Validate

Slide 5: AWS Resources Created
- S3 buckets, Lambda function, IAM role, Event triggers

Slide 6: Data Processing Flow
- CSV input → Lambda processes → CSV output

Slide 7: Why This Is DevOps
- Automation, IaC, CI/CD, Scalability, Monitoring

Slide 8: Demo Results
- Screenshot of processed CSV or CloudWatch logs

---

## File Structure to Show

```
jenkins-data-pipeline/
├── template.yaml          ← Infrastructure as Code
├── Jenkinsfile            ← Pipeline automation
├── src/
│   ├── lambda_handler.py  ← Processing logic
│   └── requirements.txt
├── sample_data.csv        ← Test data
└── README.md
```

"Everything is in code. Nothing is configured manually."

---

## Key Phrases to Use

- "Infrastructure as Code"
- "Automated deployment"
- "Serverless architecture"
- "Event-driven processing"
- "Reproducible infrastructure"
- "CI/CD pipeline"
- "Infrastructure automation"
- "DevOps best practices"

---

## Time Breakdown

- **Opening**: 30 sec
- **Architecture**: 1 min
- **IaC Explanation**: 1.5 min
- **Pipeline Walkthrough**: 1.5 min
- **Demo or Q&A**: 1 min

**Total: 5-6 minutes**
