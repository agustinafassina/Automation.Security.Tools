#!/bin/bash
json_file="a_records.json"
domains_file="domains.txt"
result_csv="scan_results.csv"

jq -r '.[] | .Records[]?.Name' "$json_file" > "$domains_file"

echo "Domain,Ports Open" > "$result_csv"

while IFS= read -r domain
do
  echo "Scanning $domain..."
  ports=$(nmap -p 1-100 --open -sS "$domain" | grep "^([0-9]*)/" | awk '{print $1}' | tr '\n' ';' | sed 's/;$//')

  if [ -z "$ports" ]; then
    ports="None"
  fi

  echo "$domain,\"$ports\"" >> "$result_csv"
done < "$domains_file"

echo "Completed scan. results in $result_csv"