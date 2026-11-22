# Scan TLS and SSL in the domains
List the AWS domains and analyze the TLS and SSL protocols

#### Framework, library, package and other📦
Python with Boto3 and bash.

#### Requirements to run the script📋
Aws cli, boto3 installed, bash, `jq`, `nikto`, and a checkout of [testssl.sh](https://github.com/drwetter/testssl.sh):
```
git clone --depth 1 https://github.com/drwetter/testssl.sh.git
```
To use a copy somewhere else, set `TESTSSL=/path/to/testssl.sh`.

#### Run script🚀
```
# get domains from aws
py get-domains.py

# analyze the TLS and SSL protocols in the domains
bash scan-tls-ssl-domains.sh
```

#### Files that it exports: in /reports
One Nikto report and one testssl.sh report per domain:
1. DOMAIN_nikto.html
2. DOMAIN_testssl.json