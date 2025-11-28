# COMP4964 Data Pipeline CI/CD Automation - Demo Presentation

---

## Slide 1: Title Slide
**COMP4964 Term Project: Automated Data Pipeline**

*Demonstrating CI/CD Automation with Jenkins, GitHub, and AWS*

---

## Slide 2: Project Overview
**What We Built:**
- Automated Jenkins pipeline hosted on DigitalOcean
- GitHub webhook triggers automatic builds on code push
- Lambda function processes CSV files from S3
- Automated unit tests prevent broken code deployment

**Key Technologies:**
- Jenkins (CI/CD orchestration)
- GitHub (version control + webhooks)
- AWS Lambda (serverless compute)
- AWS S3 (file storage)
- CloudFormation (infrastructure as code)

---

## Slide 3: Pipeline Architecture
```
Code Push to GitHub
    ↓
GitHub Webhook
    ↓
Jenkins Automatically Triggered
    ↓
Pipeline Stages:
  1. Checkout (pull latest code)
  2. Test (run pytest)
  3. Build (validate CloudFormation)
  4. Package (zip Lambda function)
  5. Deploy (update AWS resources)
  6. Validate (verify Lambda works)
```

---

## Slide 4: Demo 1 - Webhook Automation
**Goal:** Show automatic Jenkins trigger on code push

*Making code changes and watching Jenkins build automatically*
- Add a comment to lambda_handler.py
- Commit and push to GitHub
- Watch Jenkins dashboard refresh and build start
- Show "Started by GitHub push" in logs

**What's happening:**
- GitHub sends webhook to jenkins.neriyelreyes.org/github-webhook/
- Jenkins detects code change and triggers pipeline
- No manual clicks needed!

---

## Slide 5: Demo 2 - Test Stage Validation
**Goal:** Show how tests catch broken code

*Deleting a function to simulate a bug*
- Remove a function from lambda_handler.py (e.g., `process_csv_data`)
- Commit and push
- Watch Jenkins build trigger automatically
- Show Test stage FAIL (pytest can't import function)
- Explain: Pipeline stops - broken code won't deploy

**What's happening:**
- Tests run immediately after checkout
- Broken code is caught before it reaches production
- This is the CI/CD safety net!

---

## Slide 6: Demo 3 - S3 Trigger (Optional)
**Goal:** Show end-to-end data processing

*Uploading a CSV and seeing it processed*
- Upload demo_data_messy.csv to S3 `uploads/` folder
- Lambda automatically triggered by S3 event notification
- CSV is cleaned (whitespace trimmed, duplicates removed)
- Processed file appears in `processed/` folder
- Download and compare input vs output

**What's happening:**
- S3 event notification triggers Lambda automatically
- Lambda reads messy CSV → cleans data → writes output
- Second layer of automation (besides webhook)

---

## Slide 7: Key Takeaways
✅ **GitHub Webhook** - Automatic trigger on code push
✅ **Jenkins Pipeline** - Multi-stage automated testing & deployment
✅ **Unit Tests** - Catch bugs early (Test stage fails if code broken)
✅ **AWS Integration** - Lambda processes data automatically
✅ **Infrastructure as Code** - CloudFormation deploys resources

**Benefits:**
- Developers push code → system automatically tests & deploys
- Broken code is caught before production
- Reproducible deployments
- Audit trail of all changes

---

## Slide 8: Questions?
*Demo ends here*

Contact: neriyel (GitHub)
Repository: github.com/neriyel/COMP4964_Project

---
