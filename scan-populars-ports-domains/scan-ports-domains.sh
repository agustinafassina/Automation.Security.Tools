#!/usr/bin/env bash
set -uo pipefail

for tool in jq nmap; do
  if ! command -v "$tool" > /dev/null; then
    echo "Missing dependency: $tool. Install it and run again." >&2
    exit 1
  fi
done

json_file="records.json"
domains_file="domains.txt"
result_csv="scan_port_domains_results.csv"
result_json="scan_port_domains_results.json"

ports_to_scan="21,22,23,25,53,80,110,143,443,993,995,3389,3306,5432,5900,8080,8443"

# Wildcard records come back from Route 53 as "\052.domain" and can't be scanned directly.
jq -r '.[] | .Records[]?.Name | rtrimstr(".") | select(startswith("\\052") | not)' "$json_file" | sort -u > "$domains_file"

echo "Domain,OpenPorts,ScanTime" > "$result_csv"

declare -a json_results=()

while IFS= read -r domain; do
  [[ -z "$domain" ]] && continue
  echo "Scanning $domain..."

  # Grepable output lists each port as "<port>/<state>/<proto>/...", so only real open ports match.
  ports=$(nmap --open -p "$ports_to_scan" -oG - "$domain" < /dev/null \
    | grep -oE '[0-9]+/open/' | cut -d/ -f1 | paste -sd, -)

  if [[ -z "$ports" ]]; then
    ports="None"
  fi

  scan_time=$(date '+%Y-%m-%d %H:%M:%S')

  echo "\"$domain\",\"$ports\",\"$scan_time\"" >> "$result_csv"

  json_results+=("$(jq -cn --arg domain "$domain" --arg ports "$ports" --arg time "$scan_time" \
    '{Domain: $domain, OpenPorts: $ports, ScanTime: $time}')")
done < "$domains_file"

if (( ${#json_results[@]} )); then
  printf '%s\n' "${json_results[@]}" | jq -s '.' > "$result_json"
else
  echo '[]' > "$result_json"
fi

echo "Completed scan. Results in $result_csv and $result_json"
