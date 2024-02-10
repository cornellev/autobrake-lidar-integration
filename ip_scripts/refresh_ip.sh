#!/bin/bash

# Move working directory to this file
cd "${0%/*}"

# Function to get current IP address from 'ip a' output
get_ip_address() {
    ip_address=$(ip a | awk '/wlan0/ && /inet/ {gsub(/\/.*/, "", $2); print $2}')
    echo "$ip_address"
}

# Function to check internet connectivity
check_internet() {
    ping -c 1 google.com > /dev/null 2>&1
    return $?
}

# Main script

# Check if there is internet access
while ! check_internet; do
    echo "No internet access, waiting..."
    sleep 10
done

# Get current IP address
current_ip=$(get_ip_address)

# Check if IP address is empty
if [ -z "$current_ip" ]; then
    echo "Failed to retrieve IP address. Exiting..."
    exit 1
fi

# Write IP address to file
echo "$current_ip" > ip.txt

# Commit and push to git
git add ip.txt
git commit -m "Update IP address"
git push origin main
