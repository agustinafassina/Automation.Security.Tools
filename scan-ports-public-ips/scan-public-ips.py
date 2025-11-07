import json
import socket
import concurrent.futures
from datetime import datetime
import csv

PORTS_TO_SCAN = [22, 80, 443, 21, 25, 53, 110, 143, 993, 995, 3389, 3306, 5432, 5900, 8080, 8443]

def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((ip, port))
    sock.close()
    return port, result == 0

def scan_ip(ip):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check_port, ip, port) for port in PORTS_TO_SCAN]
        for future in concurrent.futures.as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
    return open_ports

with open('record_public_ip.json', 'r') as f:
    data = json.load(f)

results = []

for entry in data:
    ip_public = entry['Public_IP']
    name = entry.get('Name', '')
    private_ip = entry.get('Private_IP', 'N/A')
    region = entry.get('Region', 'N/A')

    print(f"Scanning {ip_public} ({name})...")
    open_ports = scan_ip(ip_public)
    scan_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    results.append({
        'Public_IP': ip_public,
        'Private_IP': private_ip,
        'Region': region,
        'Name': name,
        'Open_Ports': open_ports,
        'Scan_Time': scan_time
    })

with open('scan_publicips_result.json', 'w') as f:
    json.dump(results, f, indent=4)

csv_file = 'scan_publicips_result.csv'
with open(csv_file, 'w', newline='') as csvf:
    writer = csv.DictWriter(csvf, fieldnames=['Public_IP', 'Private_IP', 'Region', 'Name', 'Open_Ports', 'Scan_Time'])
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"Complete scan. Results saved to 'scan_publicips_result.json' and '{csv_file}'")