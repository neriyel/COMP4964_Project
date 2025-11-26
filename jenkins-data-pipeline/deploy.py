#!/usr/bin/env python3
"""
CloudFormation deployment script using boto3
"""
import boto3
import json
import sys
import time
from pathlib import Path

def deploy_stack(template_file, stack_name, region, environment):
    """Deploy CloudFormation stack using boto3"""
    
    # Read template
    template_path = Path(template_file)
    if not template_path.exists():
        print(f"❌ Template file not found: {template_file}")
        return False
    
    with open(template_path) as f:
        template_body = f.read()
    
    # Create CloudFormation client
    try:
        cf = boto3.client('cloudformation', region_name=region)
        print(f"✅ AWS CloudFormation client created for region: {region}")
    except Exception as e:
        print(f"❌ Failed to create CloudFormation client: {e}")
        print("   Make sure AWS credentials are configured!")
        return False
    
    # Check if stack exists
    try:
        cf.describe_stacks(StackName=stack_name)
        stack_exists = True
        print(f"📊 Stack '{stack_name}' exists, updating...")
    except cf.exceptions.ClientError as e:
        if 'does not exist' in str(e):
            stack_exists = False
            print(f"📊 Stack '{stack_name}' does not exist, creating...")
        else:
            print(f"❌ Error checking stack: {e}")
            return False
    
    # Deploy or create stack
    try:
        if stack_exists:
            response = cf.update_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Capabilities=['CAPABILITY_IAM'],
                Parameters=[
                    {
                        'ParameterKey': 'Environment',
                        'ParameterValue': environment
                    }
                ]
            )
            print(f"✅ Stack update initiated")
            print(f"   Stack ID: {response['StackId']}")
        else:
            response = cf.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Capabilities=['CAPABILITY_IAM'],
                Parameters=[
                    {
                        'ParameterKey': 'Environment',
                        'ParameterValue': environment
                    }
                ]
            )
            print(f"✅ Stack creation initiated")
            print(f"   Stack ID: {response['StackId']}")
        
        # Wait for stack operation to complete
        print(f"⏳ Waiting for stack operation to complete...")
        waiter = cf.get_waiter('stack_create_complete' if not stack_exists else 'stack_update_complete')
        try:
            waiter.wait(StackName=stack_name)
            print(f"✅ Stack operation completed successfully!")
        except Exception as e:
            if 'ResourceStatus.UPDATE_COMPLETE' in str(e) or 'does not exist' in str(e):
                print(f"⚠️  Stack operation in progress or completed (may take a few minutes)")
            else:
                print(f"⚠️  Stack operation status: {e}")
        
        # Get stack outputs
        try:
            stacks = cf.describe_stacks(StackName=stack_name)
            stack = stacks['Stacks'][0]
            print(f"\n📋 Stack Status: {stack['StackStatus']}")
            
            if 'Outputs' in stack:
                print(f"\n📦 Stack Outputs:")
                for output in stack['Outputs']:
                    print(f"   {output['OutputKey']}: {output['OutputValue']}")
            else:
                print(f"\n⚠️  No outputs found in stack")
        except Exception as e:
            print(f"⚠️  Could not retrieve stack outputs: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: deploy.py <template_file> <stack_name> <region> <environment>")
        sys.exit(1)
    
    template_file = sys.argv[1]
    stack_name = sys.argv[2]
    region = sys.argv[3]
    environment = sys.argv[4]
    
    print(f"🚀 CloudFormation Deployment Script")
    print(f"   Template: {template_file}")
    print(f"   Stack: {stack_name}")
    print(f"   Region: {region}")
    print(f"   Environment: {environment}\n")
    
    success = deploy_stack(template_file, stack_name, region, environment)
    sys.exit(0 if success else 1)
