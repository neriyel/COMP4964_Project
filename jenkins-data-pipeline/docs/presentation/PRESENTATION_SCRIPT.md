## Speaking notes for each slide (without demos)

---

## Slide 1: Title Slide
**COMP4964 Term Project: Automated Data Pipeline**

*Demonstrating CI/CD Automation with Jenkins, GitHub, and AWS*

**Speaker Notes:**
"Hi everyone, I'm presenting our COMP4964 term project on automated data pipeline.
Today we'll explore how continuous integration and continuous deployment works in real-world scenarios."

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

**Speaker Notes:**
"At its core, this project demonstrates the three pillars of modern DevOps:
1) Continuous Integration—automatic testing when code changes
2) Continuous Deployment—automatic deployment to production
3) Infrastructure as Code—reproducible deployments

We're using industry-standard tools: Jenkins for orchestration, GitHub for version control,
and AWS services for computing and storage. Everything is automated."

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

**Speaker Notes:**
"This is how the pipeline works:

When a developer pushes code to GitHub, GitHub sends a webhook notification to our Jenkins server.
Jenkins receives this notification and automatically starts a build.

The build goes through six stages:
1. **Checkout** pulls the latest code from the repository
2. **Test** runs unit tests to catch bugs immediately
3. **Build** validates the CloudFormation infrastructure template
4. **Package** zips up the Lambda function code
5. **Deploy** uses CloudFormation to update AWS resources with new code
6. **Validate** runs post-deployment checks to ensure Lambda is working

If ANY stage fails, the pipeline stops and won't proceed to the next stage.
This is the safety mechanism that prevents broken code from reaching production."

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

**Speaker Notes:**
"The webhook is the key innovation here. Traditionally, developers would manually run tests,
then manually deploy to production. With webhooks, this entire process is automatic.

In our demo, I'll make a small code change, push it to GitHub, and Jenkins will automatically
start building. You'll see in the logs 'Started by GitHub push by [username]', 
proving the webhook triggered it, not a manual button click.

This is the essence of CI/CD—continuous, automated testing and deployment."

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

**Speaker Notes:**
"Now I want to show you the safety mechanism. I'll deliberately introduce a bug—deleting a function.
When this broken code is pushed to GitHub, the webhook will trigger Jenkins automatically.

The Test stage will FAIL because the unit tests can't find the deleted function.
Importantly, the pipeline STOPS here. The Build, Package, and Deploy stages won't run.
This broken code will never reach production.

This is the value of CI/CD testing. It catches bugs immediately, before they cause issues in production.
Without this safety net, broken code could ship to users."

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

**Speaker Notes:**
"This is the second automation layer in our system. While the webhook automates deployment,
the S3 event notification automates the actual data processing.

When someone uploads a CSV to the input bucket, S3 automatically triggers our Lambda function.
Lambda reads the messy CSV, performs data cleaning operations, and writes a clean version to the output bucket.

This is real-world automation—no human intervention needed for the entire pipeline:
GitHub push → Jenkins tests and deploys → Lambda processes data automatically."

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

**Speaker Notes:**
"Let me summarize the key takeaways:

1. **Automation saves time**: Developers don't manually run tests or deployments
2. **Safety**: Broken code is caught by automated tests before it reaches users
3. **Reproducibility**: CloudFormation ensures deployments are consistent every time
4. **Auditability**: Every change is tracked in Git with a timestamp and commit message
5. **Scalability**: This same pipeline can handle 1 user or 1 million users

This is why companies like Google, Netflix, and Amazon use CI/CD pipelines.
It's the industry standard for modern software development."

---

## Slide 8: Questions?
*End of Presentation*

Contact: neriyel (GitHub)
Repository: github.com/neriyel/COMP4964_Project

**Speaker Notes:**
"That concludes the presentation. I've shown you:
- How webhooks automate the build process
- How unit tests catch bugs automatically
- How S3 events trigger data processing

Are there any questions?"

---

## TIMING
- Slide 1: 15 seconds (intro)
- Slide 2: 45 seconds (overview of tech stack)
- Slide 3: 1 minute (explain architecture)
- Slide 4: 1 minute (webhook explanation)
- Slide 5: 1 minute (testing explanation)
- Slide 6: 45 seconds (S3 automation)
- Slide 7: 1 minute (key takeaways)
- Slide 8: 30 seconds (closing)

**Total: ~6 minutes for slides only** (without demos)

---
