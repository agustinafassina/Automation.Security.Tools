#!/usr/bin/env bash
set -uo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: bash scan-header-one-domain.sh <domain>" >&2
  exit 1
fi

if ! command -v curl > /dev/null; then
  echo "Missing dependency: curl. Install it and run again." >&2
  exit 1
fi

domain="$1"

# Headers of the final response after following redirects. Tries HTTPS first, then HTTP.
headers=""
for scheme in https http; do
  if raw=$(curl -sS -I -L --max-time 15 "$scheme://$domain" 2> /dev/null) && [[ -n "$raw" ]]; then
    headers=$(printf '%s\n' "$raw" | tr -d '\r' | awk '/^HTTP\//{block=""} {block=block $0 "\n"} END{printf "%s", block}')
    break
  fi
done

if [[ -z "$headers" ]]; then
  echo "No HTTP(S) response from $domain" >&2
  exit 1
fi

echo "$headers"

check() {
  local label="$1" pattern="$2"
  if grep -qiE "$pattern" <<< "$headers"; then
    echo "✓ $label ✅"
  else
    echo "✗ $label ⛔"
  fi
}

check "x-content-type-options" '^x-content-type-options:[[:space:]]*nosniff'
check "x-frame-options" '^x-frame-options:[[:space:]]*(deny|sameorigin)'
check "content-security-policy" '^content-security-policy:'
check "HSTS" '^strict-transport-security:'
