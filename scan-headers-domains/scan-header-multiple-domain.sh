#!/usr/bin/bash
sudo apt-get install -y jq

json_file="records.json"

declare -a results_json=()
declare -a results_csv=()

check_headers() {
  local domain="$1"
  local ip="$2"
  echo "Checking: $domain (IP: $ip)"
  headers=$(curl -sI "$domain")
  echo "$headers"
  echo ""

  xcto="no⛔"
  xfo="no⛔"
  csp="no⛔"
  hsts="no⛔"

  if echo "$headers" | grep -i "x-content-type-options: nosniff" > /dev/null; then
    xcto="yes✅"
  fi

  if echo "$headers" | grep -i "x-frame-options: deny" > /dev/null; then
    xfo="yes✅"
  fi

  if echo "$headers" | grep -i "content-security-policy" > /dev/null; then
    csp="yes✅"
  fi

  if echo "$headers" | grep -i "strict-transport-security" > /dev/null; then
    hsts="yes✅"
  fi

  results_json+=("{\"Domain\":\"$domain\",\"Ip\":\"$ip\",\"xContentTypeOptions\":\"$xcto\",\"xFrameOptions\":\"$xfo\",\"ContentSecurityPolicy\":\"$csp\",\"Hsts\":\"$hsts\"}")

  results_csv+=("\"$domain\",\"$ip\",\"$xcto\",\"$xfo\",\"$csp\",\"$hsts\"")

  echo "x-content-type-options: $xcto "
  echo "x-frame-options: $xfo"
  echo "content-security-policy: $csp"
  echo "Hsts: $hsts"
  echo "------------------------"
}

domains=$(jq -r '.[] | .Records[] | .Name' "$json_file" | sort -u)

for domain in $domains; do
  ip=$(dig +short "$domain" | head -n 1)
  if [[ -n "$ip" ]]; then
    check_headers "$domain" "$ip"
  else
    echo "It could not be resolved: $domain"
  fi
done

json_output=$(printf "%s\n" "${results_json[@]}" | jq -s '.')

echo "$json_output" > verified_headers_results.json

csv_header="Domain,Ip,X-Content-Type-Options,X-Frame-Options,Content-Security-Policy,Hsts"
echo "$csv_header" > verified_headers_results.csv
for row in "${results_csv[@]}"; do
  echo "$row" >> verified_headers_results.csv
done