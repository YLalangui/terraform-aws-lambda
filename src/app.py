import json

import boto3
from prettytable import PrettyTable


def server_explorer(event, context, *args, **kwargs):
    ec2_resource = boto3.resource('ec2')
    ec2_client = boto3.client('ec2')

    server_name = event.get('server_name', '*')

    #### Get all instances ####
    if server_name != '*':
        instances = ec2_resource.instances.filter(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [f'{server_name}*', f'{server_name}'],
                }
            ]
        )
    else:
        instances = ec2_resource.instances.all()

    instance_details = []
    total_ebs_size = 0

    #### List all instances and sort them by total EBS size ####
    for instance in instances:
        instance_ebs_size = 0
        volumes = ec2_client.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance.id]}])
        for volume in volumes['Volumes']:
            instance_ebs_size += volume['Size']

        total_ebs_size += instance_ebs_size

        instance_details.append(
            {
                'instance-name': instance.tags[0]['Value'],
                'instance-id': instance.id,
                'instance-type': instance.instance_type,
                'status': instance.state['Name'],
                'private-ip': instance.private_ip_address,
                'public-ip': instance.public_ip_address or 'N/A',
                'total-size-ebs-volumes': instance_ebs_size,
            }
        )

    sorted_instance_details = sorted(instance_details, key=lambda x: x['total-size-ebs-volumes'])

    table = PrettyTable()
    table.field_names = [
        'instance-name',
        'instance-id',
        'instance-type',
        'status',
        'private-ip',
        'public-ip',
        'total-size-ebs-volumes',
    ]

    #### Add instances to the table ####
    for instance in sorted_instance_details:
        table.add_row(
            [
                instance['instance-name'],
                instance['instance-id'],
                instance['instance-type'],
                instance['status'],
                instance['private-ip'],
                instance['public-ip'],
                instance['total-size-ebs-volumes'],
            ]
        )

    table_string = table.get_string()

    return {'statusCode': 200, 'body': json.dumps({'servers': table_string, 'total_ebs_size': total_ebs_size})}
