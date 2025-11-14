# Export users of Iam and AWS
This script enumerates all IAM users in AWS, lists them, and exports them to a CSV file and a JSON file.

#### Framework, library, package and other
Python with Boto3.

#### Requirements to run the script
Aws cli and boto3 installed.

#### Run script
```
py export-users.py
```

#### Files that it exports
1. Csv result: iam_users_result.csv
2. Json result: iam_users_result.json

#### Structure of the exported files
1. Csv result: iam_users_result.csv
```
UserName,Groups,UserPolicies,GroupPermissions,TagProject,TagProjectStatus,TagProjectService,TagProjectDescription
```

2. Json result: iam_users_result.json
```
[
    {
        "UserName": "user@test.com",
        "Groups": "Dev",
        "UserPolicies": "AmazonAPIGatewayAdministrator, AWSLambda_FullAccess",
        "GroupPermissions": "AmazonAPIGatewayAdministrator",
        "TagProject": "",
        "TagProjectStatus": "",
        "TagProjectService": "",
        "TagProjectDescription": ""
    }
]
```