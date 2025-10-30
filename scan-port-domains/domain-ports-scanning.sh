#!/bin/bash
sudo apt-get install -y jq

json_file="records.json"
domains_file="domains.txt"
result_csv="scan_results.csv"

ports_to_scan="21,22,23,25,53,80,110,143,443,993,995,3389,3306,5432,5900,8080,8443"

jq -r '.[] | .Records[]?.Name' "$json_file" > "$domains_file"

echo "Domain,Ports Open" > "$result_csv"

while IFS= read -r domain
do
  echo "Scanning $domain..."
  ports=$(nmap --script ssl-enum-ciphers,ssl-cert -p "$ports_to_scan" "$domain" | grep 'open' | awk '{print $1}' | tr '\n' ',' | sed 's/,$//')

  if [ -z "$ports" ]; then
    ports="None"
  fi

  echo "$domain,\"$ports\"" >> "$result_csv"
done < "$domains_file"

echo "Completed scan. results in $result_csv"