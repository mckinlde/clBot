#!/bin/bash

# Update the package list and install Git
sudo yum update -y
sudo yum install git -y

# Verify Git installation
git --version

# Configure Git
git config --global user.name "mckinlde"
git config --global user.email "douglas.e.mckinley@gmail.com"

# Generate SSH key for GitHub
ssh-keygen -t ed25519 -C "douglas.e.mckinley@gmail.com" -f ~/.ssh/id_ed25519 -N ""

# Add the generated SSH key to the authorized keys
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys

# Display the SSH key so you can add it to GitHub
echo "Your new SSH key (copy this to GitHub):"
cat ~/.ssh/id_ed25519.pub

# Clone the GitHub repository
git clone git@github.com:mckinlde/clBot.git
