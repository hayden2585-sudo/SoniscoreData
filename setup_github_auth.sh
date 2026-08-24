#!/bin/bash
# GitHub Authentication Setup Script for SoniscoreData

echo "GitHub Authentication Setup for SoniscoreData"
echo "==========================================="
echo ""
echo "This script will help you authenticate with GitHub."
echo ""

# Check if gh CLI is available
if command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) is installed."
    if gh auth status &> /dev/null; then
        echo "You are already authenticated with GitHub!"
        gh auth status
    else
        echo "Please authenticate using GitHub CLI:"
        gh auth login
    fi
else
    echo "GitHub CLI (gh) is not installed."
    echo "You can install it from: https://github.com/cli/cli#installation"
    echo ""
    echo "Alternatively, you can create a Personal Access Token:"
    echo "1. Go to https://github.com/settings/tokens"
    echo "2. Click 'Generate new token' → 'Generate new token (classic)'"
    echo "3. Set expiration to 90 days"
    echo "4. Select scopes: repo, workflow"
    echo "5. Click 'Generate token' and copy it"
    echo ""
    echo "Then run this command to authenticate:"
    echo "git remote set-url origin https://<TOKEN>@github.com/hayden2585-sudo/SoniscoreData.git"
fi

echo ""
echo "Repository location: $(pwd)"
echo ""
echo "After authentication, you can push changes with:"
echo "git push origin main"