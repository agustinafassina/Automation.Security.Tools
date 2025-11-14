#!/bin/bash
sudo apt-get install -y jq
sudo apt-get install -y nmap

json_file="records.json"
domains_file="domains.txt"
result_csv="scan_port_domains_results.csv"
result_json="scan_port_domains_results.json"

ports_to_scan="21,22,23,25,53,80,110,143,443,993,995,3389,3306,5432,5900,8080,8443"

jq -r '.[] | .Records[]?.Name' "$json_file" > "$domains_file"

echo "Domain,OpenPorts,ScanTime" > "$result_csv"

declare -a json_results=()

while IFS= read -r domain
do
  echo "Scanning $domain..."
  ports=$(nmap --script ssl-enum-ciphers,ssl-cert -p "$ports_to_scan" "$domain" | grep 'open' | awk '{print $1}' | tr '\n' ',' | sed 's/,$//')

  if [ -z "$ports" ]; then
    ports="None"
  fi

  scan_time=$(date '+%Y-%m-%d %H:%M:%S')

  echo "$domain,\"$ports\",$scan_time" >> "$result_csv"

  json_results+=("{\"Domain\":\"$domain\",\"OpenPorts\":\"$ports\",\"ScanTime\":\"$scan_time\"}")
done < "$domains_file"

json_output=$(printf "%s\n" "${json_results[@]}" | jq -s '.')

echo "$json_output" > "$result_json"

echo "Completed scan. Results in $result_csv and $result_json"