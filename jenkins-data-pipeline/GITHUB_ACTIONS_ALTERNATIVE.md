# GitHub Actions Alternative (Optional)

If you prefer GitHub Actions instead of Jenkins, here's an alternative pipeline:

```yaml
name: Deploy Data Pipeline

on:
  push:
    branches: [ main ]
    paths:
      - 'src/**'
      - 'template.yaml'
      - '.github/workflows/deploy.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Install SAM CLI
      run: |
        python -m pip install --upgrade pip
        pip install aws-sam-cli
    
    - name: Build SAM application
      run: sam build
    
    - name: Package SAM application
      run: |
        sam package \
          --output-template-file packaged.yaml \
          --s3-bucket ${{ secrets.S3_DEPLOY_BUCKET }}
    
    - name: Deploy SAM application
      run: |
        sam deploy \
          --template-file packaged.yaml \
          --stack-name data-pipeline-stack \
          --region us-east-1 \
          --capabilities CAPABILITY_IAM \
          --no-confirm-changeset
    
    - name: Validate deployment
      run: |
        aws cloudformation describe-stacks \
          --stack-name data-pipeline-stack \
          --query 'Stacks[0].Outputs' \
          --output table
```

**Key Differences:**
- GitHub Actions runs in GitHub's cloud
- No need for separate Jenkins server
- Native GitHub integration
- Triggered on push to main branch
- Same SAM build/deploy commands
```

This is included for reference, but the presentation focuses on Jenkins as requested.
