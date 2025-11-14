import boto3
import pandas as pd
import json

iam = boto3.client('iam')

def get_user_tags(user_name):
    response = iam.list_user_tags(UserName=user_name)
    return {tag['Key']: tag['Value'] for tag in response['Tags']}

def get_user_policies(user_name):
    policies = []
    response = iam.list_attached_user_policies(UserName=user_name)
    for policy in response['AttachedPolicies']:
        policies.append(policy['PolicyName'])

    inline_response = iam.list_user_policies(UserName=user_name)
    policies.extend(inline_response['PolicyNames'])
    return policies

def get_group_permissions(group_name):
    permissions = []
    response = iam.list_attached_group_policies(GroupName=group_name)
    for policy in response['AttachedPolicies']:
        permissions.append(policy['PolicyName'])
    inline_response = iam.list_group_policies(GroupName=group_name)
    permissions.extend(inline_response['PolicyNames'])
    return permissions

def get_iam_users():
    users = []
    paginator = iam.get_paginator('list_users')
    for page in paginator.paginate():
        for user in page['Users']:
            user_name = user['UserName']

            groups_response = iam.list_groups_for_user(UserName=user_name)
            groups = [group['GroupName'] for group in groups_response['Groups']]

            user_policies = get_user_policies(user_name)

            group_permissions = []
            for group in groups:
                group_permissions.extend(get_group_permissions(group))

            tags = get_user_tags(user_name)
            project_name = tags.get('Project', '')
            project_status = tags.get('ProjectStatus', '')
            project_service = tags.get('ProjectService', '')
            project_description = tags.get('ProjectDescription', '')

            users.append({
                'UserName': user_name,
                'Groups': ', '.join(groups),
                'UserPolicies': ', '.join(user_policies),
                'GroupPermissions': ', '.join(set(group_permissions)),
                'TagProject': project_name,
                'TagProjectStatus': project_status,
                'TagProjectService': project_service,
                'TagProjectDescription': project_description
            })

    return users

users_data = get_iam_users()

df = pd.DataFrame(users_data)

csv_filename = 'iam_users_results.csv'
df.to_csv(csv_filename, index=False)

json_filename = 'iam_users_results.json'
with open(json_filename, 'w') as json_file:
    json.dump(users_data, json_file, indent=4)

print(f"Files exported successfully:\n- {csv_filename}\n- {json_filename}")