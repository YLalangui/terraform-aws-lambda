import boto3
import json

# Create an IAM client
iam = boto3.client('iam')

# Create a paginator for the list_roles operation
paginator = iam.get_paginator('list_roles')

# Initialize a list to hold EC2 related roles
ec2_roles = []

# Iterate through all roles using the paginator
for page in paginator.paginate():
    for role in page['Roles']:
        # Parse the AssumeRolePolicyDocument
        trust_policy = role['AssumeRolePolicyDocument']
        # Check if the trust relationship is with the EC2 service
        for statement in trust_policy.get('Statement', []):
            if statement.get('Effect') == 'Allow' and 'ec2.amazonaws.com' in statement.get('Principal', {}).get('Service', ''):
                ec2_roles.append(role)
                break

# Print out the EC2 related roles
for role in ec2_roles:
    print(f"Role Name: {role['RoleName']}")
    print(f"Role ARN: {role['Arn']}")
    print(f"Creation Date: {role['CreateDate']}")
    print('-------------------------')
