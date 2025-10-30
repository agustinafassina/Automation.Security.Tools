import boto3
import json

def listar_subdominios(zone_id):
    client = boto3.client('route53', region_name='us-east-1')

    paginator = client.get_paginator('list_resource_record_sets')
    response_iterator = paginator.paginate(HostedZoneId=zone_id)
    registros = []

    for response in response_iterator:
        for record in response['ResourceRecordSets']:

            if record['Type'] == 'A':
                registros.append({
                    'Name': record['Name'],
                    'Type': record['Type'],
                    'TTL': record.get('TTL'),
                    'Values': [r['Value'] for r in record.get('ResourceRecords', [])]
                })

    return registros

def main():
    client = boto3.client('route53', region_name='us-east-1')
    zones_response = client.list_hosted_zones()

    all_domains = []

    for zone in zones_response['HostedZones']:
        zone_name = zone['Name']
        zone_id = zone['Id']

        print(f"List registers for zone: {zone_name} (ID: {zone_id})")

        registros = listar_subdominios(zone_id)

        all_domains.append({
            'ZoneId': zone_id,
            'ZoneName': zone_name,
            'Records': registros
        })

    with open('records.json', 'w') as f:
        json.dump(all_domains, f, indent=4)

    print("A records have been saved to 'records.json'")

if __name__ == '__main__':
    main()