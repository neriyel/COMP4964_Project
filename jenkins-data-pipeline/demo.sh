#!/bin/bash
# Demo script to test the data pipeline locally

set -e

echo "=================================="
echo "Jenkins Data Pipeline Demo Script"
echo "=================================="
echo ""

# Configuration (update these with your values)
AWS_REGION="us-west-2"
STACK_NAME="data-pipeline-stack"
SAMPLE_CSV="sample_data.csv"

echo "📋 Step 1: Getting CloudFormation Stack Outputs..."
echo "---"

OUTPUT=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $AWS_REGION \
    --query 'Stacks[0].Outputs' \
    --output json)

INPUT_BUCKET=$(echo $OUTPUT | jq -r '.[] | select(.OutputKey=="InputBucketName") | .OutputValue')
OUTPUT_BUCKET=$(echo $OUTPUT | jq -r '.[] | select(.OutputKey=="OutputBucketName") | .OutputValue')

echo "Input Bucket: $INPUT_BUCKET"
echo "Output Bucket: $OUTPUT_BUCKET"
echo ""

echo "📤 Step 2: Uploading sample CSV to S3..."
echo "---"
echo "Uploading: $SAMPLE_CSV → s3://$INPUT_BUCKET/uploads/"

aws s3 cp $SAMPLE_CSV s3://$INPUT_BUCKET/uploads/$SAMPLE_CSV \
    --region $AWS_REGION

echo "✅ Upload complete!"
echo ""

echo "⏳ Step 3: Waiting for Lambda to process... (30 seconds)"
echo "---"
echo "Lambda is automatically triggered by S3 upload event..."

for i in {30..1}; do
    printf "\rWaiting... $i seconds remaining"
    sleep 1
done
echo ""
echo "✅ Processing complete!"
echo ""

echo "📥 Step 4: Listing processed files in output bucket..."
echo "---"

aws s3 ls s3://$OUTPUT_BUCKET/processed/ --region $AWS_REGION

echo ""
echo "✅ Demo complete! Your processed CSV is ready."
echo ""

echo "📊 To download the processed file:"
echo "---"
echo "aws s3 cp s3://$OUTPUT_BUCKET/processed/<filename> ./"
echo ""

echo "📝 To view Lambda logs:"
echo "---"
echo "aws logs tail /aws/lambda/csv-processor-dev --follow --region $AWS_REGION"
