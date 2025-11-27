# Architecture Diagrams

## 1. Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DEVELOPER WORKFLOW                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Developer writes code                                                  │
│         ↓                                                                │
│  git commit & git push → GitHub Repository                              │
│         ↓                                                                │
│  GitHub Webhook triggers Jenkins                                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        JENKINS PIPELINE                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Stage 1: CHECKOUT                                                      │
│  ┌─────────────────────────┐                                            │
│  │ git clone from GitHub   │                                            │
│  └──────────────┬──────────┘                                            │
│                 ↓                                                        │
│  Stage 2: BUILD                                                         │
│  ┌─────────────────────────┐                                            │
│  │ sam build               │                                            │
│  │ - Validates template    │                                            │
│  │ - Builds Lambda code    │                                            │
│  └──────────────┬──────────┘                                            │
│                 ↓                                                        │
│  Stage 3: PACKAGE                                                       │
│  ┌─────────────────────────┐                                            │
│  │ sam package             │                                            │
│  │ - Creates ZIP file      │                                            │
│  │ - Uploads to S3         │                                            │
│  └──────────────┬──────────┘                                            │
│                 ↓                                                        │
│  Stage 4: DEPLOY                                                        │
│  ┌─────────────────────────┐                                            │
│  │ sam deploy              │                                            │
│  │ - CloudFormation        │                                            │
│  │ - Creates AWS resources │                                            │
│  └──────────────┬──────────┘                                            │
│                 ↓                                                        │
│  Stage 5: VALIDATE                                                      │
│  ┌─────────────────────────┐                                            │
│  │ Confirm success         │                                            │
│  │ Print outputs           │                                            │
│  └──────────────┬──────────┘                                            │
│                 ↓                                                        │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                     AWS INFRASTRUCTURE CREATED                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  CloudFormation Stack (template.yaml defines everything)                │
│  ┌────────────────────────────────────────────────────────┐             │
│  │                                                        │             │
│  │  ┌──────────────────┐        ┌──────────────────┐    │             │
│  │  │  S3 Input        │        │  S3 Output       │    │             │
│  │  │  Bucket          │        │  Bucket          │    │             │
│  │  │                  │        │                  │    │             │
│  │  │ uploads/         │        │ processed/       │    │             │
│  │  │                  │        │                  │    │             │
│  │  └────────┬─────────┘        └────────▲─────────┘    │             │
│  │           │                           │               │             │
│  │           │ S3 Event Trigger          │               │             │
│  │           │ (ObjectCreated)           │               │             │
│  │           ▼                           │               │             │
│  │     ┌──────────────────────┐          │               │             │
│  │     │   Lambda Function    │──────────┘               │             │
│  │     │                      │                          │             │
│  │     │ csv_processor        │                          │             │
│  │     │ - Read CSV           │                          │             │
│  │     │ - Clean data         │                          │             │
│  │     │ - Remove duplicates  │                          │             │
│  │     │ - Write CSV          │                          │             │
│  │     └────────────────────────┘                        │             │
│  │           │                                           │             │
│  │           └── (Permissions via IAM Role)             │             │
│  │                                                        │             │
│  └────────────────────────────────────────────────────────┘             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                       USER INTERACTION                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  User uploads CSV → S3 input bucket                                     │
│         ↓                                                                │
│  S3 event notification → Lambda triggered                               │
│         ↓                                                                │
│  Lambda processes data (clean, deduplicate, transform)                  │
│         ↓                                                                │
│  Lambda writes result → S3 output bucket                                │
│         ↓                                                                │
│  User downloads processed CSV                                           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Flow Inside Lambda

```
INPUT (CSV from S3)
│
│ Read CSV file
│ ┌─────────────────────┐
│ │ Name, Email, Age... │
│ │ John, j@e.com, 32   │
│ │ Jane, j@e.com, 28   │ ← Same email as John (duplicate)
│ └─────────────────────┘
│
│ Clean data:
│ • Remove whitespace
│ • Trim fields
│ ┌─────────────────────┐
│ │ Name | Email | Age  │
│ │ John | j@e   | 32   │
│ │ Jane | j@e   | 28   │
│ └─────────────────────┘
│
│ Remove duplicates:
│ • Keep first occurrence
│ ┌─────────────────────┐
│ │ Name | Email | Age  │
│ │ John | j@e   | 32   │
│ └─────────────────────┘
│
│ Remove empty/invalid rows
│
│ Write to S3
│
OUTPUT (Cleaned CSV)
```

---

## 3. Jenkins Pipeline Execution Flow

```
Git Push to GitHub
       │
       │ (GitHub Webhook)
       ▼
┌─────────────────┐
│ JENKINS PICKS   │
│ UP CHANGES      │
└────────┬────────┘
         │
         ▼
    ┌─────────────────────────┐
    │ CHECKOUT Stage          │
    │ • Clone GitHub repo     │
    │ Duration: 5-10 sec      │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ BUILD Stage             │
    │ • sam build             │
    │ • Validate YAML         │
    │ • Build Lambda ZIP      │
    │ Duration: 30-60 sec     │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ PACKAGE Stage           │
    │ • sam package           │
    │ • Create .zip           │
    │ • Upload to S3          │
    │ Duration: 20-30 sec     │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ DEPLOY Stage            │
    │ • sam deploy            │
    │ • CloudFormation        │
    │ • Create/Update stack   │
    │ Duration: 1-3 min       │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ VALIDATE Stage          │
    │ • Check stack status    │
    │ • Print outputs         │
    │ • Get bucket names      │
    │ Duration: 10-20 sec     │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ ✅ PIPELINE COMPLETE    │
    │ Ready for use!          │
    └─────────────────────────┘

Total Duration: 2-5 minutes
```

---

## 4. Infrastructure as Code Concept

```
Traditional Approach (Manual/Error-Prone)
────────────────────────────────────────
Admin logs into AWS Console
         ↓
Click to create S3 bucket
         ↓
Click to create Lambda function
         ↓
Upload code via console
         ↓
Create IAM role manually
         ↓
Link S3 trigger to Lambda
         ↓
Document what was done
         ↓
Problem: Hard to reproduce, version control, repeat


Infrastructure as Code Approach (Automated)
──────────────────────────────────────────
template.yaml (code) defines:
  • S3 buckets
  • Lambda function
  • IAM role
  • S3 event trigger
         ↓
Version in Git
         ↓
Jenkins reads template
         ↓
sam deploy reads template
         ↓
CloudFormation creates all resources
         ↓
Repeatable, versioned, auditable
         ↓
Benefits:
✓ Same deployment every time
✓ Tracked in Git
✓ Rollback on failure
✓ Team collaboration
✓ Disaster recovery
```

---

## 5. Event-Driven Architecture

```
User Action
    │
    │ Uploads CSV file
    │
    ▼
┌─────────────────────────┐
│ S3 Input Bucket         │
│                         │
│ /uploads/data.csv ──────┐
│                      │
└─────────────────────┘│
                       │
                       │ S3 Event Notification
                       │ (Asynchronous trigger)
                       │
                       ▼
            ┌──────────────────────┐
            │ AWS Lambda           │
            │ (csv_processor)      │
            │                      │
            │ Auto-triggered ◄─────┤
            │ • No manual action   │
            │ • Scales auto       │
            │ • Logs in CloudWatch│
            │                      │
            └─────────┬────────────┘
                      │
                      │ Write output
                      │
                      ▼
        ┌──────────────────────┐
        │ S3 Output Bucket     │
        │                      │
        │ /processed/data.csv  │
        └──────────────────────┘
```

---

## 6. How It Fits DevOps

```
Traditional Development (Siloed)
────────────────────────────────
Developer          Operations
    │                   │
    ├─ Write code       │
    │                   │
    └─ Deploy? ────────►│ Manual AWS setup?
                        │ Unclear process?
                        │ Error-prone?
                        │
Problem: Miscommunication, manual steps, inconsistency

DevOps Approach (Integrated)
───────────────────────────
Developer + Operations (Collaboration)
    │
    ├─ Write code (src/lambda_handler.py)
    │
    ├─ Define infrastructure (template.yaml)
    │
    ├─ Define pipeline (Jenkinsfile)
    │
    ├─ Commit to Git
    │
    └─ Push to GitHub
         │
         ▼
    Jenkins (Automation)
         │
         ├─ Build
         ├─ Test
         ├─ Deploy (CloudFormation)
         └─ Validate
         │
         ▼
    AWS (Fully automated)
         │
         └─ S3 + Lambda live and running

Benefits:
✓ Everyone knows what runs where
✓ No manual configuration
✓ Reproducible
✓ Faster deployment
✓ Easier debugging
```

---

## 7. Key DevOps Principles Demonstrated

```
┌──────────────────┐
│ Automation       │ ← Jenkins automates build/deploy
└──────────────────┘

┌──────────────────┐
│ Infrastructure   │ ← template.yaml is code
│ as Code          │   (version controlled, reproducible)
└──────────────────┘

┌──────────────────┐
│ CI/CD Pipeline   │ ← Git push → Build → Deploy → Validate
└──────────────────┘

┌──────────────────┐
│ Monitoring &     │ ← CloudWatch logs, metrics
│ Observability    │
└──────────────────┘

┌──────────────────┐
│ Scalability      │ ← Serverless auto-scales
└──────────────────┘

┌──────────────────┐
│ Reliability      │ ← CloudFormation rollback on error
└──────────────────┘

┌──────────────────┐
│ Collaboration    │ ← Code review, Git history
└──────────────────┘
```
