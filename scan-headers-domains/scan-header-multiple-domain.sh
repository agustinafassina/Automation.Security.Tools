#!/usr/bin/bash
sudo apt-get install -y jq

domains=(
  ""
  ""
  ""
)

declare -a results=()

check_headers() {
  local domain="$1"
  echo "Verifying: $domain"
  headers=$(curl -sI "$domain")
  echo "$headers"
  echo ""

  xcto="no"
  xfo="no"
  csp="no"
  hsts="no"

  if echo "$headers" | grep -i "x-content-type-options: nosniff" > /dev/null; then
    xcto="yes"
  fi

  if echo "$headers" | grep -i "x-frame-options: deny" > /dev/null; then
    xfo="yes"
  fi

  if echo "$headers" | grep -i "content-security-policy" > /dev/null; then
    csp="yes"
  fi

  if echo "$headers" | grep -i "strict-transport-security" > /dev/null; then
    hsts="yes"
  fi

  results+=("{\"domain\":\"$domain\",\"xContentTypeOptions\":\"$xcto\",\"xFrameOptions\":\"$xfo\",\"contentSecurityPolicy\":\"$csp\",\"hsts\":\"$hsts\"}")

  echo "x-content-type-options: $xcto ✅"
  echo "x-frame-options: $xfo ✅"
  echo "content-security-policy: $csp ✅"
  echo "HSTS: $hsts ✅"
  echo "------------------------"
}

# Ejecutar por cada dominio
for domain in "${domains[@]}"; do
  check_headers "$domain"
done


json_output=$(printf "%s\n" "${results[@]}" | jq -s '.')

echo "$json_output" > verified_headers_results.json