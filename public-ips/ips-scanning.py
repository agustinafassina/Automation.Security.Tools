import json
import csv
import socket

def check_port_22(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)  # timeout 2 seconds
    result = sock.connect_ex((ip, 22))
    sock.close()
    return result == 0

with open('record_public_ip.json', 'r') as f:
    data = json.load(f)

ips_info = [{'IP': entry['Public_IP'], 'Name': entry.get('Name', 'Sin nombre')} for entry in data]

scan_results = []

for item in ips_info:
    ip = item['IP']
    name = item['Name']
    print(f"Verifying {ip} ({name})...")
    if check_port_22(ip):
        open_status = 'Open'
    else:
        open_status = 'Closed or not responeding'

    scan_results.append({
        'IP': ip,
        'Name': name,
        'Port 22': open_status
    })

with open('port_22_scan_result.csv', 'w', newline='') as csvfile:
    fieldnames = ['IP', 'Name', 'Port 22']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in scan_results:
        writer.writerow(row)

print("Verifycation completed. Results saved in 'port_22_scan_result.csv'.")