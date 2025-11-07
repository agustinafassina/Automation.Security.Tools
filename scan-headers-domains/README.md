# Scan headers in the domains
Lists the AWS domains and scans them.

#### Framework, library, package and other
Python with Boto3 and bash.

#### Requirements to run the script
Aws cli, boto3 installed and bash.

#### Run script
```
# get domains from aws
py get-domains.py

# scan domain headers (multiple domains)
bash scan-header-multiple-domain.sh
```

#### Files that it exports
1. Csv result: verified_headers_results.csv
2. Json result: verified_headers_results.json

#### Structure of the exported files
1. Csv result: verified_headers_results.csv
```
Domain,IP,X-Content-Type-Options,X-Frame-Options,Content-Security-Policy,HSTS
```

2. Json result: verified_headers_results.json
```
[
    {
        "domain": "",
        "ip": "",
        "xContentTypeOptions": "no⛔",
        "xFrameOptions": "no⛔",
        "contentSecurityPolicy": "no⛔",
        "hsts": "no⛔"
    }
]
```