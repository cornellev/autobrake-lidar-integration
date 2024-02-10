#!/bin/bash

# Function to retrieve IP address from GitHub
get_ip_address() {
    ip_address=$(curl -s https://raw.githubusercontent.com/cornellev/autobrake-lidar-integration/main/ip_scripts/ip.txt)
    echo "$ip_address"
}

# Main script

# Get IP address from GitHub
remote_ip=$(get_ip_address)

# Check if IP address is empty
if [ -z "$remote_ip" ]; then
    echo "Failed to retrieve IP address from GitHub. Exiting..."
    exit 1
fi

# SSH connect to the retrieved IP address
echo "Connecting to $remote_ip..."
ssh ubuntu@$remote_ip
