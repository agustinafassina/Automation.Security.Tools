# Scan TLS and SSL in the domains
List the AWS domains and analyze the TLS and SSL protocols

#### Framework, library, package and other
Python with Boto3 and bash.

#### Requirements to run the script
Aws cli, boto3 installed and bash.

#### Run script
```
# get domains from aws
py get-domains.py

# analyze the TLS and SSL protocols in the domains
bash scan-tls-ssl-domains.sh
```

#### Files that it exports: in /reports
Result: The result is exported in an html by domain
1. DOMAIN.html