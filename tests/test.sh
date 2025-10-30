#!/usr/bin/bash
domain=""

echo "Run scan http-enum in $domain..."
nmap -p 80,443 --script http-enum "$domain"