import json
import sys

import boto3

lambda_client = boto3.client('lambda')


def load_test_event(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)


if len(sys.argv) < 2:
    print("ERROR: json path missing. Example: python invoke_lambda-remote.py event.json")
    sys.exit(1)

json_file_path = sys.argv[1]
test_event = load_test_event(json_file_path)

response = lambda_client.invoke(
    FunctionName='server-explorer-function', InvocationType='RequestResponse', Payload=json.dumps(test_event)
)

response = json.loads(response['Payload'].read().decode('utf-8'))['body']
output = json.loads(response)

print('################## SERVERS ##################')
print(output['servers'])
print('#################### TOTAL EBS SIZE ####################')
print(f'{output["total_ebs_size"]}GB')
