# Scan popular open ports in the public Ip in Aws
Scan AWS public IPs, taking into account the most popular ports.

### Ports that are taken into account
* 21 (FTP)
* 22 (SSH)
* 23 (Telnet)
* 25 (SMTP)
* 53 (DNS)
* 80 (HTTP)
* 110 (POP3)
* 143 (IMAP)
* 443 (HTTPS)
* 993 (IMAPS)
* 995 (POP3S)
* 3389 (RDP)
* 3306 (MySQL)
* 5432 (PostgreSQL)
* 5900 (VNC)
* 8080 (HTTP alternativo)
* 8443 (HTTPS alternativo)

#### Framework, library, package and other
Python and Boto3

#### Requirements to run the script
Aws cli, python and boto3 installed.

#### Run script
```
# get public ips
py get-publics-ips.py

# scan ips
py scan-public-ips.py
```

#### Files that it exports
1. Csv result: scan_publicips_result.csv
2. Json result: scan_publicips_result.json

#### Structure of the exported files
1. Csv result: scan_publicips_result.csv
```
Public_IP,Private_IP,Region,Name,Open_Ports,Scan_Time
```

2. Json result: scan_publicips_result.json
```
[
    {
        "Public_IP": "xx.xxx.xxx.xxx",
        "Private_IP": "xxx.xx.xx.xx",
        "Region": "us-east-1",
        "Name": "xx-xx-xx",
        "Open_Ports": [
            53,
            80,
            443
        ],
        "Scan_Time": "2025-11-13 17:55:19"
    }
]
```