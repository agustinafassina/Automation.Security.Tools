import boto3
import json

regions = [
    'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
    'ap-south-1', 'ap-northeast-1',
    'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1',
    'ap-southeast-2', 'ca-central-1',
    'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3',
    'eu-north-1', 'sa-east-1'
]


def instance_name(instance):
    for tag in instance.get('Tags', []):
        if tag['Key'] == 'Name':
            return tag['Value']
    return None


def main():
    all_ips = []
    skipped = 0

    for region in regions:
        try:
            ec2 = boto3.client('ec2', region_name=region)
            paginator = ec2.get_paginator('describe_instances')
            pages = paginator.paginate(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
            )
            for page in pages:
                for reservation in page['Reservations']:
                    for instance in reservation['Instances']:
                        public_ip = instance.get('PublicIpAddress')
                        if not public_ip:
                            skipped += 1
                            continue
                        all_ips.append({
                            'Region': region,
                            'Name': instance_name(instance),
                            'PublicIp': public_ip,
                            'PrivateIp': instance.get('PrivateIpAddress')
                        })
        except Exception as e:
            print(f"Error in the region {region}: {e}")

    with open('record_public_ip.json', 'w') as f:
        json.dump(all_ips, f, indent=4)

    print(
        f"{len(all_ips)} running instances with a public IP saved to 'record_public_ip.json' "
        f"({skipped} without a public IP skipped)"
    )


if __name__ == '__main__':
    main()
