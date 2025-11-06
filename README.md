# Security Tools for Automation
The goal of this repository is to automate some security tests, such as domain scanning and port checking.

#### The repository has some implementations
- [x] Scan open multiple ports in the domains (scan-port-domains)
- [x] Scan open multiple ports in the public IPs (scan-public-ips)
- [ ] Scan TLS/SSL (scan-tls-domains)
- [x] Scan headers in the domains (apis or apps)

### What do you need for the scripts to work?
You need to have aws-cli installed because the framework we use from Python needs access to our AWS account.
- Aws account with permissions 🔐

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

#### Scripts, details and JSON structures 📝
- Domain Scan Test: the idea is to list all AWS and Route 53 domains and run a command that scans them, displays the results in the console, and saves them to a CSV file.
- Open ports scan: the idea is to list the IPs and scan them to see if they have the SSH port open.
- export-iam-users: ./export-iam-users/README.md
