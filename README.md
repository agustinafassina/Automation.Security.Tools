# Security Tools for Automation ⚙️
Scripts and tools for automating data extraction and analysis from AWS. The main goal is to facilitate the collection of information from various AWS services and apply security, quality, or compliance scanners to detect vulnerabilities, inconsistencies, or risks.

### Implementations 🚀
- [x] **Export users list of IAM in AWS** (`export-iam-users`)
- [x] **Scan open 1000 ports in public IPs** (`scan-1000-ports-public-ips`)
- [x] **Scan headers in domains** (APIs or apps) (`scan-headers-domains`)
- [x] **Scan popular open ports in public IPs** (`scan-populars-ports-public-ips`)
- [x] **Scan popular open ports in domains** (`scan-populars-ports-domains`)
- [x] **Scan TLS/SSL in domains** (`scan-tls-ssl-domains`)

### Data fetched from AWS 📄
- **IAM:** policies, users, roles, and permissions.
- **EC2 and Public IPs:** instance inventory, open ports, and more.
- **Route53:** domain inventory for later scanning.

### Prerequisites 🦾
- **AWS CLI** installed and configured (scripts need access to your AWS account with appropriate permissions 🔐).
- **Python 3** (for Python scripts).
- **Bash** (for shell scripts).

## Installation and Setup
### 1. Clone the repository
```bash
git clone <repository-url>
cd Automation.Security.Tools
```

### 2. Virtual environment and dependencies (Python)
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

### 3. Environment variables
Copy `.env.example` to `.env` and adjust the values:
```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS
```

Main variables in `.env`:
| Variable | Description |
|----------|-------------|
| `AWS_REGION` | AWS region (e.g., `us-east-1`) |
| `AWS_PROFILE` | AWS CLI profile |
| `OUTPUT_DIR` | Output directory (e.g., `./results`) |
| `LOG_LEVEL` | Log level (`INFO`, `DEBUG`, etc.) |

### Project Structure
```
Automation.Security.Tools/
├── src/
│   └── common/           # Shared code (AWS clients, config, utils)
├── export-iam-users/
├── scan-1000-ports-public-ips/
├── scan-headers-domains/
├── scan-populars-ports-public-ips/
├── scan-populars-ports-domains/
├── scan-tls-ssl-domains/
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

The `src/common` module provides:
- AWS clients (EC2, IAM, Route53)
- Configuration loaded from `.env`
- File utilities (JSON, CSV) and logging

## Tools Used 🛠️
- **Boto3** (Python) – AWS SDK
- **Bash** – Scanning scripts
- **AWS CLI** – Configuration and account access

## Scripts, Details, and Output Structures 📝
### 1. Export users list of IAM in AWS
- **Folder:** `./export-iam-users`
- **Details:** `./export-iam-users/README.md`
- **Output files:**
  - CSV: `iam_users_results.csv`
  - JSON: `iam_users_results.json`

### 2. Scan public IPs and open ports (1000)

- **Folder:** `./scan-1000-ports-public-ips`
- **Details:** `./scan-1000-ports-public-ips/README.md`
- **Output files:**
  - CSV: `scan_publicips_results.csv`
  - JSON: `scan_publicips_results.json`

### 3. Scan headers in domains

- **Folder:** `./scan-headers-domains`
- **Details:** `./scan-headers-domains/README.md`
- **Output files:**
  - CSV: `verified_headers_results.csv`
  - JSON: `verified_headers_results.json`

### 4. Scan popular open ports in public IPs

- **Folder:** `./scan-populars-ports-public-ips`
- **Details:** `./scan-populars-ports-public-ips/README.md`
- **Output files:**
  - CSV: `scan_publicips_results.csv`
  - JSON: `scan_publicips_results.json`

### 5. Scan open ports in domains

- **Folder:** `./scan-populars-ports-domains`
- **Details:** `./scan-populars-ports-domains/README.md`
- **Output files:**
  - CSV: `scan_port_domains_results.csv`
  - JSON: `scan_port_domains_results.json`

### 6. Scan TLS/SSL in domains

- **Folder:** `./scan-tls-ssl-domains`
- **Details:** `./scan-tls-ssl-domains/README.md`
- **Output files:**
  - HTML: `./scan-tls-ssl-domains/reports`
