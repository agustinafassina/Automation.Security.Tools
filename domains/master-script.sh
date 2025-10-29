#!/usr/bin/bash
# Master script to run all setup scripts in order

script_get_domains_path="C:\Users\AgustinaFassinaENG\Desktop\ReposEng\Other\Other\In Progresss\Automation.Security.Tools\domains\get-domains.py"
script_domain_scanning_path="C:\Users\AgustinaFassinaENG\Desktop\ReposEng\Other\Other\In Progresss\Automation.Security.Tools\domains\domain-scanning.sh"

py "$script_get_domains_path"

if [ $? -eq 0 ]; then
    echo "Run scanning script..."
    bash "$script_domain_scanning_path"
fi