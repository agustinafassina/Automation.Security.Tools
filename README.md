# Security Tools for Automation ⚙️
This repository contains scripts and tools for automating data extraction and analysis from AWS. The main goal is to facilitate the collection of information from various AWS services and apply different security, quality, or compliance scanners to detect vulnerabilities, inconsistencies, or risks in the data.

#### The repository has some implementations 🚀
1. [x] Export users list of Iam in AWS (export-iam-users)
2. [x] Scan open 1000 ports in the public IPs (scan-1000-ports-public-ips)
3. [x] Scan headers in the domains (apis or apps)
4. [x] Scan popular open ports in the public ips (scan-populars-ports-public-ips)
5. [x] Scan popular open ports in the domains (scan-populars-ports-domains)
6. [x] Scan TLS/SSL (scan-tls-domains)

#### Types of data fetched from AWS📄
- IAM: Policies, users, roles, and permissions.
- EC2 and Public IP: Instance inventory, open ports and more.
- Route53: inventory of domains to scan later.

#### Tools used 🛠️
- Robo3 (python)
- Bash
- Aws cli

#### What do you need for the scripts to work? 🦾
You need to have aws-cli installed because the framework we use from Python needs access to our AWS account (with permissions 🔐)

#### Scripts, details and JSON structures 📝
1. Export users list of Iam in AWS
    - Script folder: ./export-iam-users
    - Readme detail: ./export-iam-users/README.md
    - Export files:
    - 1. Csv result: iam_users_results.csv
    - 2. Json result: iam_users_results.json

2. Scan public IPs and open ports (1000)
    - Script folder: ./scan-1000-ports-public-ips
    - Readme detail: ./scan-1000-ports-public-ips/README.md
    - Export files:
    - 1. Csv result: scan_publicips_results.csv
    - 2. Json result: scan_publicips_results.json

3. Scan headers in the domains
    - Script folder: ./scan-headers-domains
    - Readme detail: ./scan-headers-domains/README.md
    - Export files:
    - 1. Csv result: verified_headers_results.csv
    - 2. Json result: verified_headers_results.json

4. Scan popular open ports in the public ips
    - Script folder: ./scan-populars-ports-public-ips
    - Readme detail: ./scan-populars-ports-public-ips/README.md
    - Export files:
    - 1. Csv result: scan_publicips_results.csv
    - 2. Json result: scan_publicips_results.json

5. Scan for open ports in the domains
    - Script folder: ./scan-populars-ports-domains
    - Readme detail: ./scan-populars-ports-domains/README.md
    - Export files:
    - 1. Csv result: scan_port_domains_results.csv
    - 2. Json result: scan_port_domains_results.json

6. Scan TLS and SSL in the domains
    - Script folder: ./scan-tls-ssl-domains
    - Readme detail: ./scan-tls-ssl-domains/README.md
    - Export files:
    - 1. Html files result: /scan-tls-ssl-domains/reports

