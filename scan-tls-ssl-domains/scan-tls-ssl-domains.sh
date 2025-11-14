#!/usr/bin/bash
file_json="records.json"
reports_dir="./reports"
mkdir -p "$reports_dir"

TESTSSL_PATH="./testssl.sh/testssl.sh"

domains=$(jq -r '.[] | .Records[] | .Name' "$file_json" | sort -u)

for domain in $domains; do
  echo "============================="
  echo "Analyzing: $domain"

  safe_domain=$(echo "$domain" | sed 's/[^a-zA-Z0-9_-]/_/g')

  echo "[+] Running Nikto..."
  nikto -h "http://$domain" -output "$reports_dir/${safe_domain}_nikto.html" 2>/dev/null

  echo "[+] Running testssl.sh..."
  bash "$TESTSSL_PATH/testssl.sh" --quiet --jsonfile "$reports_dir/${safe_domain}_testssl.json" --timeout 300 "$domain" || {
    echo "Error running testssl.sh in $domain"
    continue
  }

  echo "Results saved in:"
  echo " - $reports_dir/${safe_domain}_nikto.html"
  echo " - $reports_dir/${safe_domain}_testssl.json"
  echo "============================="
  echo ""
done