# Scan domains and open ports.
Lists the AWS domains and scans them.

#### Framework, library, package and other
Python with Boto3 and bash.

#### Requirements to run the script
Aws cli, boto3 installed and bash.

#### Run script
```
# get domains from aws
py get-domains.py

# scan domain and open port (only some ports)
bash scan-ports-domains.sh
```

#### Files that it exports
1. Csv result: scan_port_domains_results.csv
2. Json result: scan_port_domains_results.json

#### Structure of the exported files
1. Csv result: scan_port_domains_results.csv
```
Domain,OpenPorts,ScanTime
```

2. Json result: scan_port_domains_results.json
```
[
    {
        "Domain": "api.domain.ar.",
        "OpenPorts": "53/tcp,443/tcp",
        "ScanTime": "2025-01-01 19:00:00"
    }
]
```