import boto3
import json

file_name = 'records.json'


def list_a_records(client, zone_id):
    paginator = client.get_paginator('list_resource_record_sets')
    records = []

    for page in paginator.paginate(HostedZoneId=zone_id):
        for record in page['ResourceRecordSets']:
            if record['Type'] == 'A':
                records.append({
                    'Name': record['Name'].rstrip('.'),
                    'Type': record['Type'],
                    'TTL': record.get('TTL'),
                    'Values': [r['Value'] for r in record.get('ResourceRecords', [])]
                })

    return records


def main():
    client = boto3.client('route53', region_name='us-east-1')
    paginator = client.get_paginator('list_hosted_zones')

    all_domains = []

    for page in paginator.paginate():
        for zone in page['HostedZones']:
            zone_name = zone['Name']
            zone_id = zone['Id']

            # Private zones only resolve inside their VPCs, so an external scan can't reach them.
            if zone.get('Config', {}).get('PrivateZone'):
                print(f"Skipping private zone: {zone_name} (ID: {zone_id})")
                continue

            print(f"Listing records for zone: {zone_name} (ID: {zone_id})")

            all_domains.append({
                'ZoneId': zone_id,
                'ZoneName': zone_name,
                'Records': list_a_records(client, zone_id)
            })

    with open(file_name, 'w') as f:
        json.dump(all_domains, f, indent=4)

    print(f"A records have been saved to '{file_name}'")


if __name__ == '__main__':
    main()
