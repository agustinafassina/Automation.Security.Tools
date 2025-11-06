#!/usr/bin/bash#!/bin/bash
sudo apt-get install -y jq

domain="domainToReplace"

headers=$(curl -sI "$domain")

echo "$headers"

if echo "$headers" | grep -i "x-content-type-options: nosniff" > /dev/null; then
  echo "✓ x-content-type-options ✅"
else
  echo "✗ x-content-type-options ⛔"
fi

if echo "$headers" | grep -i "x-frame-options: deny" > /dev/null; then
  echo "✓ x-frame-options ✅"
else
  echo "✗ x-frame-options ⛔"
fi

if echo "$headers" | grep -i "content-security-policy" > /dev/null; then
  echo "✓ content-security-policy ✅"
else
  echo "✗ content-security-policy ⛔"
fi

if echo "$headers" | grep -i "strict-transport-security" > /dev/null; then
  echo "✓ HSTS ✅"
else
  echo "✗ HSTS ⛔"
fi