# Demo Workflow Script - COMP4964 CI/CD Pipeline
# Duration: ~10 minutes
# Follow this script exactly for consistent demo timing

---

## SETUP (Before Demo Starts)
✅ Have these open in separate windows/tabs:
   1. Jenkins dashboard: https://jenkins.neriyelreyes.org
   2. GitHub repo: https://github.com/neriyel/COMP4964_Project
   3. VS Code with project open
   4. AWS Console (S3) - Optional for Demo 3

✅ Verify:
   - Jenkins is running and logged in
   - GitHub repo is up to date (git pull)
   - You have demo_data_messy.csv in jenkins-data-pipeline/

---

## DEMO 1: Webhook Automation (4 minutes)
**Objective: Show automatic Jenkins build trigger on GitHub push**

### Step 1: Explain the Setup (30 seconds)
Say:
"We have Jenkins running on a DigitalOcean server at jenkins.neriyelreyes.org.
It's configured with a GitHub webhook that listens for code changes.
When I push to GitHub, Jenkins should automatically start a build—no manual clicks."

### Step 2: Make a Code Change (1 minute)
1. Open `jenkins-data-pipeline/src/lambda_handler.py` in VS Code
2. Find the `lambda_handler` function (around line 20)
3. Add this comment after the function definition:
   ```python
   def lambda_handler(event, context):
       """
       Triggered when a CSV file is uploaded to the input S3 bucket.
       Processes the CSV, cleans the data, and saves to output bucket.
       """
       # DEMO: This is an automated test - watch Jenkins trigger automatically!
       try:
   ```
4. Save the file

Say:
"I've added a comment to the code. Now watch what happens when I push this to GitHub..."

### Step 3: Commit and Push (1 minute)
1. Open terminal in VS Code
2. Run:
   ```
   git add jenkins-data-pipeline/src/lambda_handler.py
   git commit -m "Demo: Add webhook automation test comment"
   git push
   ```
3. Watch the output - should say "main -> main"

Say:
"Just pushed to GitHub. Let's switch to the Jenkins dashboard..."

### Step 4: Watch Jenkins Auto-Trigger (1.5 minutes)
1. Switch to Jenkins dashboard tab
2. REFRESH the page (F5)
3. Watch the build START automatically
4. Say: "See that? I didn't click anything! Jenkins automatically detected the push via GitHub webhook."
5. Click on the build number to view logs
6. Scroll to find: "Started by GitHub push by neriyel"
7. Show pipeline execution:
   - ✅ Checkout stage (pulls code)
   - ✅ Test stage (runs pytest)
   - ✅ Build stage (validates CloudFormation)
   - And so on...

Say:
"The webhook fired, Jenkins pulled the latest code, and ran the entire pipeline automatically.
This is continuous integration—the moment we push, tests and deployment begin."

---

## DEMO 2: Test Stage Validation (4 minutes)
**Objective: Show how unit tests catch broken code and prevent deployment**

### Step 1: Explain the Safety Net (30 seconds)
Say:
"Now I'm going to simulate a broken code change—something a developer accidentally deleted.
Watch how the Test stage catches it and stops the pipeline."

### Step 2: Break the Code (1.5 minutes)
1. Go back to VS Code
2. Open `jenkins-data-pipeline/src/lambda_handler.py`
3. Find the `process_csv_data` function (around line 85)
4. SELECT the ENTIRE function definition and the function body
5. DELETE it completely (leave just a blank line where it was)
6. Save the file

Say:
"I just deleted the `process_csv_data` function—simulating a developer accidentally removing code.
The unit tests should catch this..."

### Step 3: Commit and Push (1 minute)
1. Terminal:
   ```
   git add jenkins-data-pipeline/src/lambda_handler.py
   git commit -m "Demo: Accidentally delete process_csv_data function"
   git push
   ```

Say:
"Pushing the broken code to GitHub..."

### Step 4: Watch Tests Fail (1 minute)
1. Switch to Jenkins dashboard
2. REFRESH the page
3. Watch the build START automatically again
4. Wait for it to reach the **Test stage**
5. Build will FAIL with error:
   ```
   AssertionError: Failed to import process_csv_data: cannot import name 'process_csv_data'
   ```
6. Click on the failed stage to show the error
7. Point out: **Build is STOPPED** - subsequent stages (Build, Package, Deploy) are SKIPPED

Say:
"Perfect! The test stage failed because it couldn't import the deleted function.
The pipeline automatically STOPPED—this broken code will never reach production.
This is the safety net of automated testing."

### Step 5: Fix and Re-push (1.5 minutes)
1. Go back to VS Code
2. Use Ctrl+Z to undo the deletion (or manually retype the function)
3. Verify the function is back
4. Terminal:
   ```
   git add jenkins-data-pipeline/src/lambda_handler.py
   git commit -m "Demo: Restore process_csv_data function - tests now pass"
   git push
   ```

Say:
"Now I'm restoring the function. Let's see if the pipeline passes this time..."

### Step 6: Verify Success (1 minute)
1. Switch to Jenkins dashboard
2. REFRESH
3. Watch the build trigger and execute
4. Show all stages passing: ✅ Checkout ✅ Test ✅ Build ✅ Package ✅ Deploy ✅ Validate
5. Point to "Finished: SUCCESS" at the end

Say:
"Code is fixed, tests pass, and now the entire pipeline succeeds.
This is CI/CD working as designed—automatic testing prevents bugs from reaching production."

---

## DEMO 3: S3 File Processing (2 minutes) - OPTIONAL
**Objective: Show end-to-end data processing**

### Prerequisites:
- Have AWS Console open to S3
- Have demo_data_messy.csv ready

### Step 1: Show Input Data (30 seconds)
1. Open demo_data_messy.csv in VS Code
2. Show the messy data:
   - Inconsistent whitespace ("  alice chen  ")
   - Leading/trailing spaces in values
3. Say: "This is messy data with formatting issues. Lambda will clean it."

### Step 2: Upload to S3 (1 minute)
1. Go to AWS S3 console
2. Navigate to input bucket → uploads/ folder
3. Upload demo_data_messy.csv
4. Say: "Uploading to S3 triggers Lambda automatically..."

### Step 3: Check Output (30 seconds)
1. Navigate to output bucket → processed/ folder
2. Refresh and look for the new file (with timestamp)
3. Download it and open in Excel/text editor
4. Show cleaned data:
   - Whitespace trimmed
   - Data standardized
5. Say: "Lambda ran automatically, cleaned the data, and saved it. End-to-end automation!"

---

## TALKING POINTS FOR Q&A

**Q: How does the webhook work?**
A: "GitHub is configured to send an HTTP POST to jenkins.neriyelreyes.org/github-webhook/ 
whenever code is pushed. Jenkins receives it and automatically triggers a build."

**Q: What if I want to run tests locally first?**
A: "You can run `pytest tests/test_lambda.py` locally before pushing. 
Jenkins runs the same tests, so you catch issues early."

**Q: How is Lambda deployed?**
A: "CloudFormation template defines the Lambda function and S3 buckets. 
When Jenkins runs the Deploy stage, it updates the stack, automatically deploying code changes."

**Q: Can I pause the pipeline?**
A: "Yes! You can disable the webhook trigger in Jenkins, or set up a branch protection rule in GitHub 
to require review before merging."

**Q: How long does the full pipeline take?**
A: "Usually 2-3 minutes from push to production. 
Most time is spent building/packaging the Lambda function."

---

## CLEANUP AFTER DEMO

1. Undo the deleted function if you left it deleted (git revert or fix manually)
2. Commit and push one final time so repo is in good state
3. Take a screenshot of the successful Jenkins build for documentation

---

## TIMING CHECKLIST

- [ ] Demo 1 (Webhook): 4 minutes ⏱️
- [ ] Demo 2 (Tests): 4 minutes ⏱️
- [ ] Demo 3 (S3): 2 minutes ⏱️
- **Total: ~10 minutes** ✅

If running short:
- Skip Demo 3 (S3 processing)
- Focus on Demo 1 & 2 (automation + testing)

---
