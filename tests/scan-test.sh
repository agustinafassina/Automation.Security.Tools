#!/bin/bash

domain=""

if [ ! -d "testssl.sh" ]; then
  git clone --depth 1 https://github.com/drwetter/testssl.sh.git
fi

./testssl.sh/testssl.sh --jsonfile result.json "$domain"

wait

tls_versions=$(jq -r '.["test results"][] | select(.tls != null) | .tls' result.json | grep -o "TLS [0-9.]*" | sort -u)

echo "Supported TLS versions:"
echo "$tls_versions"

if echo "$tls_versions" | grep -q "TLS 1.2" && echo "$tls_versions" | grep -q "TLS 1.3"; then
  echo "TLS 1.2 and TLS 1.3 supported correctly."
else
  echo "Warning: TLS 1.2 o TLS 1.3 not supported."
fi

weak_ciphers=$(jq -r '.["test results"][] | select(.cipher != null) | .cipher' result.json | grep -i "weak" )

if [ -n "$weak_ciphers" ]; then
  echo "Debile ciphers detected:"
  echo "$weak_ciphers"
else
  echo "No weak ciphers detected."
fi