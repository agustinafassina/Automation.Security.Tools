#!/usr/bin/env bash
set -uo pipefail

file_json="records.json"
reports_dir="./reports"

# Path to the testssl.sh executable. Defaults to a plain `git clone` of the repo in this folder.
TESTSSL="${TESTSSL:-./testssl.sh/testssl.sh}"

for tool in jq nikto; do
  if ! command -v "$tool" > /dev/null; then
    echo "Missing dependency: $tool. Install it and run again." >&2
    exit 1
  fi
done

if [[ ! -f "$TESTSSL" ]]; then
  echo "testssl.sh not found at $TESTSSL" >&2
  echo "Clone it with: git clone --depth 1 https://github.com/drwetter/testssl.sh.git" >&2
  echo "or set TESTSSL=/path/to/testssl.sh" >&2
  exit 1
fi

mkdir -p "$reports_dir"

# Wildcard records come back from Route 53 as "\052.domain" and can't be scanned directly.
domains=$(jq -r '.[] | .Records[]?.Name | rtrimstr(".") | select(startswith("\\052") | not)' "$file_json" | sort -u)

for domain in $domains; do
  echo "============================="
  echo "Analyzing: $domain"

  safe_domain=$(echo "$domain" | sed 's/[^a-zA-Z0-9_-]/_/g')

  echo "[+] Running Nikto..."
  nikto -h "http://$domain" -output "$reports_dir/${safe_domain}_nikto.html" 2> /dev/null \
    || echo "Error running nikto on $domain"

  echo "[+] Running testssl.sh..."
  bash "$TESTSSL" --quiet --jsonfile "$reports_dir/${safe_domain}_testssl.json" --timeout 300 "$domain" || {
    echo "Error running testssl.sh on $domain"
    continue
  }

  echo "Results saved in:"
  echo " - $reports_dir/${safe_domain}_nikto.html"
  echo " - $reports_dir/${safe_domain}_testssl.json"
  echo "============================="
  echo ""
done
