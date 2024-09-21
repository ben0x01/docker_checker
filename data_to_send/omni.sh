#!/bin/bash

# Update and upgrade the system
sudo apt update && sudo apt upgrade -y

# Install the Omni CLI
echo "Installing Omni CLI..."
curl -sSfL https://raw.githubusercontent.com/omni-network/omni/main/scripts/install_omni_cli.sh | bash -s

# Initialize Geth and Halo nodes with Omni
echo "Initializing Geth and Halo nodes..."
omni operator init-nodes --network=omega --moniker=foo --clean

# Navigate to the Omega configuration directory
cd ~/.omni/omega

# Start Geth and Halo using Docker Compose in detached mode
echo "Starting Geth and Halo using Docker Compose..."
docker-compose up -d  # Start in detached mode

# Function to check the status of the containers
check_docker_status() {
    # Check if the container is running (you can specify the container name if needed)
    if docker-compose ps | grep "Up"; then
        echo "Docker containers are running."
    else
        echo "Docker containers are not running. Restarting..."
        docker-compose restart  # Restart the containers if they are not running
    fi
}

# Monitoring loop to keep checking the status of Docker containers
while true; do
    check_docker_status
    sleep 120  # Check every 2 minutes
done
