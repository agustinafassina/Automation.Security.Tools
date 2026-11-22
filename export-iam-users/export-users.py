import boto3
import pandas as pd
import json
from functools import lru_cache

iam = boto3.client('iam')


def paginate(operation, result_key, **kwargs):
    paginator = iam.get_paginator(operation)
    items = []
    for page in paginator.paginate(**kwargs):
        items.extend(page[result_key])
    return items


def get_user_tags(user_name):
    tags = paginate('list_user_tags', 'Tags', UserName=user_name)
    return {tag['Key']: tag['Value'] for tag in tags}


def get_user_policies(user_name):
    attached = paginate('list_attached_user_policies', 'AttachedPolicies', UserName=user_name)
    inline = paginate('list_user_policies', 'PolicyNames', UserName=user_name)
    return [policy['PolicyName'] for policy in attached] + inline


@lru_cache(maxsize=None)
def get_group_permissions(group_name):
    attached = paginate('list_attached_group_policies', 'AttachedPolicies', GroupName=group_name)
    inline = paginate('list_group_policies', 'PolicyNames', GroupName=group_name)
    return tuple([policy['PolicyName'] for policy in attached] + inline)


def get_iam_users():
    users = []
    for user in paginate('list_users', 'Users'):
        user_name = user['UserName']

        groups = [
            group['GroupName']
            for group in paginate('list_groups_for_user', 'Groups', UserName=user_name)
        ]

        group_permissions = []
        for group in groups:
            group_permissions.extend(get_group_permissions(group))

        tags = get_user_tags(user_name)

        users.append({
            'UserName': user_name,
            'Groups': ', '.join(groups),
            'UserPolicies': ', '.join(get_user_policies(user_name)),
            'GroupPermissions': ', '.join(sorted(set(group_permissions))),
            'TagProject': tags.get('Project', ''),
            'TagProjectStatus': tags.get('ProjectStatus', ''),
            'TagProjectService': tags.get('ProjectService', ''),
            'TagProjectDescription': tags.get('ProjectDescription', '')
        })

    return users


def main():
    users_data = get_iam_users()

    df = pd.DataFrame(users_data)

    csv_filename = 'iam_users_results.csv'
    df.to_csv(csv_filename, index=False)

    json_filename = 'iam_users_results.json'
    with open(json_filename, 'w') as json_file:
        json.dump(users_data, json_file, indent=4)

    print(f"Files exported successfully:\n- {csv_filename}\n- {json_filename}")


if __name__ == '__main__':
    main()
