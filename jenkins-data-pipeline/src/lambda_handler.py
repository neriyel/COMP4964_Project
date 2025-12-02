"""
CSV Data Pipeline Lambda Function
Processes incoming CSV files from S3, cleans and transforms data, outputs processed CSV
"""

# test

import json
import boto3
import csv
import io
import os
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client("s3")


def lambda_handler(event, context):
    """
    Triggered when a CSV file is uploaded to the input S3 bucket.
    Processes the CSV, cleans the data, and saves to output bucket.
    """
    try:
        print(f"Lambda event received: {json.dumps(event)}")

        # Extract S3 bucket and key from the event
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = event["Records"][0]["s3"]["object"]["key"]

        logger.info(f"Processing file: s3://{bucket}/{key}")
        print(f"Processing file: s3://{bucket}/{key}")

        # Read CSV from input bucket
        csv_data = read_csv_from_s3(bucket, key)

        # Process and clean the data
        cleaned_data = process_csv_data(csv_data)

        # Write processed CSV to output bucket
        output_key = f"processed/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(key)}"
        write_csv_to_s3(cleaned_data, output_key)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "CSV processed successfully",
                    "input_file": f"s3://{bucket}/{key}",
                    "output_file": f"s3://{os.environ['OUTPUT_BUCKET']}/{output_key}",
                    "rows_processed": len(cleaned_data),
                }
            ),
        }

    except Exception as e:
        logger.error(f"Error processing CSV: {str(e)}", exc_info=True)
        print(f"ERROR: {str(e)}")
        import traceback

        traceback.print_exc()
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


# def read_csv_from_s3(bucket, key):
#     """
#     Read CSV file from S3 bucket and return as list of dictionaries
#     """
#     try:
#         response = s3_client.get_object(Bucket=bucket, Key=key)
#         csv_content = response["Body"].read().decode("utf-8")

#         reader = csv.DictReader(io.StringIO(csv_content))
#         data = list(reader)

#         logger.info(f"Read {len(data)} rows from {key}")
#         return data

#     except Exception as e:
#         logger.error(f"Error reading CSV from S3: {str(e)}")
#         raise


def process_csv_data(data):
    """
    Process and clean the CSV data:
    - Remove duplicates
    - Remove empty rows
    - Trim whitespace
    - Standardize data
    - Remove rows with missing values
    """
    if not data:
        return []

    cleaned_data = []

    for row in data:
        # Skip empty rows
        if not any(row.values()):
            continue

        # Clean row: trim whitespace and standardize
        cleaned_row = {}
        for key, value in row.items():
            if value is not None:
                cleaned_row[key.strip()] = value.strip()
            else:
                cleaned_row[key.strip()] = ""

        # Skip rows with missing required fields (columns)
        if all(cleaned_row.values()):
            cleaned_data.append(cleaned_row)

    # Remove duplicates while preserving order
    seen = set()
    unique_data = []
    for row in cleaned_data:
        row_tuple = tuple(sorted(row.items()))
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_data.append(row)

    logger.info(
        f"Cleaned data: {len(data)} input rows → {len(unique_data)} output rows"
    )
    return unique_data


def write_csv_to_s3(data, output_key):
    """
    Write processed data to output S3 bucket.
    """
    try:
        if not data:
            logger.warning("No data to write")
            return

        output_bucket = os.environ["OUTPUT_BUCKET"]

        # Convert list of dicts back to CSV format
        output = io.StringIO()
        fieldnames = list(data[0].keys())

        # ========== DEMO: BOLD HEADERS FEATURE ==========
        # bold_headers = [f"**{header}**" for header in fieldnames]
        # output.write(",".join(bold_headers) + "\n")
        # ========== END DEMO BLOCK ==========

        # Write data rows
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        # ========== DEMO: BOLD HEADERS FEATURE ==========
        writer.writeheader()
        # ========== END DEMO BLOCK ==========
        writer.writerows(data)

        # Upload to S3
        s3_client.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=output.getvalue(),
            ContentType="text/csv",
        )

        logger.info(
            f"Successfully wrote {len(data)} rows to s3://{output_bucket}/{output_key}"
        )

    except Exception as e:
        logger.error(f"Error writing CSV to S3: {str(e)}")
        raise
