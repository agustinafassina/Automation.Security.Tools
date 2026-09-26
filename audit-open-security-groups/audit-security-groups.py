import boto3
import pandas as pd
import json

regions = [
    'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
    'ap-south-1', 'ap-northeast-1',
    'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1',
    'ap-southeast-2', 'ca-central-1',
    'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3',
    'eu-north-1', 'sa-east-1'
]

OPEN_CIDRS = {'0.0.0.0/0', '::/0'}

# Admin, remote access, and data ports. An open range that includes any of these is high risk.
HIGH_RISK_PORTS = {
    21, 22, 23, 25, 110, 135, 139, 143, 445,
    1433, 1521, 2375, 3306, 3389, 5432, 5900,
    6379, 9200, 11211, 27017,
}

COLUMNS = [
    'Region', 'GroupId', 'GroupName', 'VpcId',
    'Protocol', 'FromPort', 'ToPort', 'Cidr',
    'RuleDescription', 'Risk'
]


def risk_for(protocol, from_port, to_port):
    if protocol in ('-1', 'all') or from_port is None or to_port is None:
        return 'critical'
    if from_port == 0 and to_port == 65535:
        return 'critical'
    if protocol in ('icmp', 'icmpv6'):
        return 'medium'
    if any(from_port <= port <= to_port for port in HIGH_RISK_PORTS):
        return 'high'
    return 'medium'


def open_cidrs(permission):
    cidrs = []
    for ip_range in permission.get('IpRanges', []):
        cidr = ip_range.get('CidrIp')
        if cidr in OPEN_CIDRS:
            cidrs.append((cidr, ip_range.get('Description', '')))
    for ip_range in permission.get('Ipv6Ranges', []):
        cidr = ip_range.get('CidrIpv6')
        if cidr in OPEN_CIDRS:
            cidrs.append((cidr, ip_range.get('Description', '')))
    return cidrs


def format_port(protocol, port):
    if protocol in ('-1', 'all') or port is None:
        return 'all'
    return port


def findings_for_region(region):
    ec2 = boto3.client('ec2', region_name=region)
    paginator = ec2.get_paginator('describe_security_groups')
    findings = []

    for page in paginator.paginate():
        for group in page['SecurityGroups']:
            for permission in group.get('IpPermissions', []):
                protocol = permission.get('IpProtocol', '')
                from_port = permission.get('FromPort')
                to_port = permission.get('ToPort')

                for cidr, description in open_cidrs(permission):
                    findings.append({
                        'Region': region,
                        'GroupId': group.get('GroupId', ''),
                        'GroupName': group.get('GroupName', ''),
                        'VpcId': group.get('VpcId', ''),
                        'Protocol': 'all' if protocol == '-1' else protocol,
                        'FromPort': format_port(protocol, from_port),
                        'ToPort': format_port(protocol, to_port),
                        'Cidr': cidr,
                        'RuleDescription': description,
                        'Risk': risk_for(protocol, from_port, to_port),
                    })

    return findings


def main():
    findings = []

    for region in regions:
        try:
            region_findings = findings_for_region(region)
            findings.extend(region_findings)
            print(f"{region}: {len(region_findings)} open rules")
        except Exception as e:
            print(f"Error in the region {region}: {e}")

    findings.sort(key=lambda row: (
        {'critical': 0, 'high': 1, 'medium': 2}.get(row['Risk'], 3),
        row['Region'],
        row['GroupId'],
    ))

    df = pd.DataFrame(findings, columns=COLUMNS)
    csv_filename = 'open_security_groups_results.csv'
    df.to_csv(csv_filename, index=False)

    json_filename = 'open_security_groups_results.json'
    with open(json_filename, 'w') as json_file:
        json.dump(findings, json_file, indent=4)

    by_risk = df['Risk'].value_counts().to_dict() if not df.empty else {}
    print(
        f"Files exported successfully:\n- {csv_filename}\n- {json_filename}\n"
        f"Open rules: {len(findings)} "
        f"(critical={by_risk.get('critical', 0)}, "
        f"high={by_risk.get('high', 0)}, "
        f"medium={by_risk.get('medium', 0)})"
    )


if __name__ == '__main__':
    main()
