import json

import boto3
import pytest
from moto import mock_aws

from src.app import server_explorer


@mock_aws
@pytest.mark.parametrize(
    "event, expected_total_ebs_size",
    [
        ({'server_name': '*'}, 204),
        ({'server_name': 'server-1'}, 38),
        ({'server_name': 'server-'}, 146),
        ({'server_name': 'blabla'}, 0),
    ],
)
def test_server_explorer(event, expected_total_ebs_size):
    # Arrange
    ec2 = boto3.resource('ec2', region_name='eu-central-1')

    instance_1 = ec2.create_instances(ImageId='ami-0abcdef1234567890', MinCount=1, MaxCount=1)[0]
    instance_1.create_tags(Tags=[{'Key': 'Name', 'Value': 'jenkins'}])

    volume = ec2.create_volume(Size=50, AvailabilityZone='eu-central-1a')
    volume.attach_to_instance(InstanceId=instance_1.id, Device='/dev/sdf')

    instance_2 = ec2.create_instances(ImageId='ami-0abcdef1234567890', MinCount=1, MaxCount=1)[0]
    instance_2.create_tags(Tags=[{'Key': 'Name', 'Value': 'server-1'}])

    volume = ec2.create_volume(Size=30, AvailabilityZone='eu-central-1a')
    volume.attach_to_instance(InstanceId=instance_2.id, Device='/dev/sdf')

    instance_3 = ec2.create_instances(ImageId='ami-0abcdef1234567890', MinCount=1, MaxCount=1)[0]
    instance_3.create_tags(Tags=[{'Key': 'Name', 'Value': 'server-2'}])

    volume = ec2.create_volume(Size=100, AvailabilityZone='eu-central-1a')
    volume.attach_to_instance(InstanceId=instance_3.id, Device='/dev/sdf')

    # Act
    response = server_explorer(event, None)

    # Assert
    assert response['statusCode'] == 200
    assert json.loads(response['body'])['total_ebs_size'] == expected_total_ebs_size
