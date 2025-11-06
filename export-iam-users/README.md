# Export users of Iam and AWS
This script enumerates all IAM users in AWS, lists them, and exports them to a CSV file and a JSON file.

1. Csv result: iam_users_permissions_results.csv
```
UserName,Groups,UserPolicies,GroupPermissions,TagProject,TagProjectStatus,TagProjectService,TagProjectDescription
```

2. Json result: iam_users_permissions_result.json
```
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
```