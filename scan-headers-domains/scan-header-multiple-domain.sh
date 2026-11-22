#!/usr/bin/env bash
set -uo pipefail

for tool in jq curl dig; do
  if ! command -v "$tool" > /dev/null; then
    echo "Missing dependency: $tool. Install it and run again." >&2
    exit 1
  fi
done

json_file="records.json"
result_json="verified_headers_results.json"
result_csv="verified_headers_results.csv"

declare -a results_json=()
declare -a results_csv=()

# Headers of the final response after following redirects. Tries HTTPS first, then HTTP.
fetch_headers() {
  local domain="$1"
  local scheme raw
  for scheme in https http; do
    if raw=$(curl -sS -I -L --max-time 15 "$scheme://$domain" 2> /dev/null) && [[ -n "$raw" ]]; then
      printf '%s\n' "$raw" | tr -d '\r' | awk '/^HTTP\//{block=""} {block=block $0 "\n"} END{printf "%s", block}'
      return 0
    fi
  done
  return 1
}

has_header() {
  grep -qiE "$2" <<< "$1"
}

check_headers() {
  local domain="$1"
  local ip="$2"
  local headers status

  echo "Checking: $domain (IP: $ip)"
  if ! headers=$(fetch_headers "$domain"); then
    echo "No HTTP(S) response from $domain"
    echo "------------------------"
    return
  fi
  status=$(head -n 1 <<< "$headers")
  echo "$headers"

  local xcto="no⛔" xfo="no⛔" csp="no⛔" hsts="no⛔"
  has_header "$headers" '^x-content-type-options:[[:space:]]*nosniff' && xcto="yes✅"
  has_header "$headers" '^x-frame-options:[[:space:]]*(deny|sameorigin)' && xfo="yes✅"
  has_header "$headers" '^content-security-policy:' && csp="yes✅"
  has_header "$headers" '^strict-transport-security:' && hsts="yes✅"

  results_json+=("$(jq -cn \
    --arg domain "$domain" --arg ip "$ip" --arg status "$status" \
    --arg xcto "$xcto" --arg xfo "$xfo" --arg csp "$csp" --arg hsts "$hsts" \
    '{Domain: $domain, Ip: $ip, FinalStatus: $status, xContentTypeOptions: $xcto, xFrameOptions: $xfo, ContentSecurityPolicy: $csp, Hsts: $hsts}')")

  results_csv+=("\"$domain\",\"$ip\",\"$status\",\"$xcto\",\"$xfo\",\"$csp\",\"$hsts\"")

  echo "x-content-type-options: $xcto"
  echo "x-frame-options: $xfo"
  echo "content-security-policy: $csp"
  echo "Hsts: $hsts"
  echo "------------------------"
}

# Wildcard records come back from Route 53 as "\052.domain" and can't be requested directly.
domains=$(jq -r '.[] | .Records[]?.Name | rtrimstr(".") | select(startswith("\\052") | not)' "$json_file" | sort -u)

for domain in $domains; do
  ip=$(dig +short "$domain" | tail -n 1)
  if [[ -n "$ip" ]]; then
    check_headers "$domain" "$ip"
  else
    echo "It could not be resolved: $domain"
  fi
done

if (( ${#results_json[@]} )); then
  printf '%s\n' "${results_json[@]}" | jq -s '.' > "$result_json"
else
  echo '[]' > "$result_json"
fi

echo "Domain,Ip,FinalStatus,X-Content-Type-Options,X-Frame-Options,Content-Security-Policy,Hsts" > "$result_csv"
for row in "${results_csv[@]}"; do
  echo "$row" >> "$result_csv"
done

echo "Results saved in $result_csv and $result_json"
