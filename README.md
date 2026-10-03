# Security Tools for Automation
Scripts that pull inventory from an AWS account and check it for open ports, missing security headers, TLS issues, and security groups open to the internet.

## Requirements 📋
- Python 3
- AWS CLI configured for the account you want to scan (the scripts use that credential chain)
- Bash, for the shell scripts. On Windows, use Git Bash or WSL. Several of those scripts install packages with `apt`
- Extra tools used by some scans: `jq`, `curl`, `dig`, `nmap`, `nikto`, and [testssl.sh](https://github.com/drwetter/testssl.sh)

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On Linux or macOS, activate with `source .venv/bin/activate`.

`requirements.txt` installs `boto3` and `pandas`. Each tool writes its files in its own folder, so run the commands below from that folder.

## Layout 📂
```
Automation.Security.Tools/
├── export-iam-users/
├── scan-1000-ports-public-ips/
├── scan-populars-ports-public-ips/
├── scan-populars-ports-domains/
├── scan-headers-domains/
├── scan-tls-ssl-domains/
├── audit-open-security-groups/
├── src/common/
├── tests/
├── requirements.txt
└── README.md
```

`src/common/` holds shared AWS, config, and file helpers. The scripts in the tool folders do not import it. They call `boto3` directly.

## Run the tools
### export-iam-users
IAM users, with groups, attached policies, and project tags.
```bash
python export-users.py
```
Writes `iam_users_results.csv` and `iam_users_results.json`. More detail is in `export-iam-users/README.md`.

### scan-1000-ports-public-ips
Public IPs from running EC2 instances, then a wide port scan.
```bash
python get-public-ips.py
python scan-1000-ports-public-ips.py
```
The first command writes `record_public_ip.json`. The second writes `scan_publicips_results.csv` and `scan_publicips_results.json`. More detail is in `scan-1000-ports-public-ips/README.md`.

### scan-populars-ports-public-ips
Same inventory, scanned only on common ports (21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 3306, 5432, 5900, 8080, 8443).
```bash
python get-public-ips.py
python scan-public-ips.py
```
Writes `record_public_ip.json`, then `scan_publicips_results.csv` and `scan_publicips_results.json`. More detail is in `scan-populars-ports-public-ips/README.md`.

### scan-populars-ports-domains
Route 53 A records, then those same common ports via `nmap`. Needs `jq` and `nmap`.
```bash
python get-domains.py
bash scan-ports-domains.sh
```
Writes `records.json`, then `scan_port_domains_results.csv` and `scan_port_domains_results.json`. More detail is in `scan-populars-ports-domains/README.md`.

### scan-headers-domains
Route 53 A records, then checks `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`, and `Strict-Transport-Security`. Needs `jq`, `curl`, and `dig`.
```bash
python get-domains.py
bash scan-header-multiple-domain.sh
```
Writes `records.json`, then `verified_headers_results.csv` and `verified_headers_results.json`. More detail is in `scan-headers-domains/README.md`.

### scan-tls-ssl-domains
Route 53 A records, then `nikto` and `testssl.sh` per domain. Needs `jq`, `nikto`, and a `testssl.sh` checkout. The script runs `./testssl.sh/testssl.sh/testssl.sh`.
```bash
python get-domains.py
bash scan-tls-ssl-domains.sh
```
Writes `records.json`, plus `reports/<domain>_nikto.html` and `reports/<domain>_testssl.json`. More detail is in `scan-tls-ssl-domains/README.md`.

### audit-open-security-groups
Ingress rules open to `0.0.0.0/0` or `::/0`, tagged `critical`, `high`, or `medium`. Needs `ec2:DescribeSecurityGroups`.
```bash
python audit-security-groups.py
```
Writes `open_security_groups_results.csv` and `open_security_groups_results.json`.
