import json
import socket
import concurrent.futures
from datetime import datetime
import csv

specific_ports = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995,
    1723, 3306, 3389, 5900, 8080, 8009, 8180, 81, 300, 591, 593, 832, 981,
    1010, 1311, 2082, 2087, 2095, 2096, 2480, 3000, 3128, 3333, 4243, 4567,
    4711, 4712, 4993, 5000, 5104, 5108, 5800, 6543, 7000, 7396, 7474, 8000,
    8001, 8008, 8014, 8042, 8069, 8081, 8088, 8090, 8091, 8118, 8123, 8172,
    8222, 8243, 8280, 8281, 8333, 8443, 8500, 8834, 8880, 8888, 8983, 9000,
    9043, 9060, 9080, 9090, 9091, 9200, 9443, 9800, 9981, 12443, 16080, 18091,
    18092, 20720, 28017, 1, 3, 4, 6, 7, 9, 13, 17, 19, 20, 24, 26, 30, 32,
    33, 37, 42, 43, 49, 70, 78, 79, 82, 83, 84, 85, 88, 89, 90, 99, 100, 106,
    109, 113, 119, 125, 144, 146, 161, 163, 179, 199, 211, 212, 222, 254, 255,
    256, 259, 264, 280, 301, 306, 311, 340, 366, 389, 395, 406, 407, 416, 417,
    425, 427, 444, 458, 464, 465, 475, 481, 497, 500, 512, 513, 514, 515, 524,
    541, 543, 544, 545, 548, 554, 555, 563, 587, 616, 617, 625, 631, 636, 646,
    648, 666, 667, 668, 683, 687, 691, 700, 705, 709, 711, 714, 720, 722, 726,
    730, 731, 740, 749, 765, 777, 783, 787, 800, 801, 808, 843, 873, 880, 888,
    898, 900, 901, 902, 903, 911, 912, 987, 990, 992, 999, 1000, 1001, 1002,
    1007, 1009, 1011, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030,
    1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043,
    1044, 1045, 1046, 1047
]

additional_ranges = [
    range(1050, 1100),
    range(12000, 12500),
    range(20000, 20500),
    range(30000, 30500),
    range(51000, 51500),
    range(60000, 61000)
]

additional_ports = []
for r in additional_ranges:
    additional_ports.extend(r)

ports_to_scan = set(specific_ports + additional_ports)
ports_to_scan = sorted(ports_to_scan)

def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((ip, port))
    sock.close()
    return port, result == 0

def scan_ip(ip):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check_port, ip, port) for port in ports_to_scan]
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