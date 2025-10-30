import boto3
import json

REGIONS = [
    'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
    'ap-south-1', 'ap-northeast-1',
    'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1',
    'ap-southeast-2', 'ca-central-1',
    'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3',
    'eu-north-1', 'sa-east-1'
]

all_ips = []

for region in REGIONS:
    try:
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] == 'running':
                    public_ip = instance.get('PublicIpAddress')
                    private_ip = instance.get('PrivateIpAddress')

                    name = None
                    if 'Tags' in instance:
                        for tag in instance['Tags']:
                            if tag['Key'] == 'Name':
                                name = tag['Value']
                                break
                    all_ips.append({
                        'Region': region,
                        'Name': name,
                        'Public_IP': public_ip,
                        'Private_IP': private_ip
                    })
    except Exception as e:
        print(f"Error in the region {region}: {e}")

with open('record_public_ip.json', 'w') as f:
    json.dump(all_ips, f, indent=4)
