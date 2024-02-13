import json
import sys

from src.app import server_explorer


def load_test_event(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)


# Check if a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("ERROR: json path missing. Example: python invoke_lambda-locally.py event.json")
    sys.exit(1)

json_file_path = sys.argv[1]
test_event = load_test_event(json_file_path)


class DummyContext:
    def __init__(self):
        self.function_name = "server_explorer"
        self.memory_limit_in_mb = 128
        self.invoked_function_arn = "arn:aws:lambda:eu-central-1:123456789012:function:server_explorer"
        self.aws_request_id = "dummy_request_id"


response = server_explorer(test_event, DummyContext())
output = json.loads(response['body'])

print('################## SERVERS ##################')
print(output['servers'])
print('#################### TOTAL EBS SIZE ####################')
print(f'{output["total_ebs_size"]}GB')
