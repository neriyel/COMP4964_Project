"""
Unit tests for Lambda function
"""

import unittest
import sys
import os

# Add src to path so we can import lambda_handler
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestLambdaBasic(unittest.TestCase):
    """Basic unit tests for Lambda function"""

    def test_lambda_handler_exists(self):
        """Test that lambda_handler function exists"""
        try:
            from lambda_handler import lambda_handler

            self.assertTrue(callable(lambda_handler))
            print("✓ Lambda handler function exists")
        except ImportError as e:
            self.fail(f"Failed to import lambda_handler: {e}")

    def test_process_csv_data_exists(self):
        """Test that process_csv_data function exists"""
        try:
            from lambda_handler import process_csv_data

            self.assertTrue(callable(process_csv_data))
            print("✓ process_csv_data function exists")
        except ImportError as e:
            self.fail(f"Failed to import process_csv_data: {e}")

    def test_read_csv_from_s3_exists(self):
        """Test that read_csv_from_s3 function exists"""
        try:
            from lambda_handler import read_csv_from_s3

            self.assertTrue(callable(read_csv_from_s3))
            print("✓ read_csv_from_s3 function exists")
        except ImportError as e:
            self.fail(f"Failed to import read_csv_from_s3: {e}")

    def test_write_csv_to_s3_exists(self):
        """Test that write_csv_to_s3 function exists"""
        try:
            from lambda_handler import write_csv_to_s3

            self.assertTrue(callable(write_csv_to_s3))
            print("✓ write_csv_to_s3 function exists")
        except ImportError as e:
            self.fail(f"Failed to import write_csv_to_s3: {e}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
