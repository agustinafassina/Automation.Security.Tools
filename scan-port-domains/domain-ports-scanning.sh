#!/bin/bash
sudo apt-get install -y jq
sudo apt-get install -y nmap

json_file="records.json"
domains_file="domains.txt"
result_csv="scan_results.csv"

ports_to_scan="21,22,23,25,53,80,110,143,443,993,995,3389,3306,5432,5900,8080,8443"

jq -r '.[] | .Records[]?.Name' "$json_file" > "$domains_file"

echo "Domain,Ports Open,Scan Time" > "$result_csv"

while IFS= read -r domain
do
  echo "Scanning $domain..."
  ports=$(nmap --script ssl-enum-ciphers,ssl-cert -p "$ports_to_scan" "$domain" | grep 'open' | awk '{print $1}' | tr '\n' ',' | sed 's/,$//')

  if [ -z "$ports" ]; then
    ports="None"
  fi

  # Obtener la fecha y hora actual en formato legible
  scan_time=$(date '+%Y-%m-%d %H:%M:%S')

  # Escribir en el CSV incluyendo la hora
  echo "$domain,\"$ports\",$scan_time" >> "$result_csv"
done < "$domains_file"

echo "Completed scan. results in $result_csv"