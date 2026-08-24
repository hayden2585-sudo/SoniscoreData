#!/bin/bash
# SoniscoreData - Push to GitHub Script
# This script will help you push the completed project to GitHub

echo "======================================"
echo "SoniscoreData - GitHub Push Helper"
echo "======================================"
echo ""
echo "The project is ready to push to GitHub!"
echo ""
echo "You have 4 options:"
echo ""
echo "1. GitHub CLI (easiest)"
echo "   - Run: gh auth login"
echo "   - Then: ./PUSH_TO_GITHUB.sh"
echo ""
echo "2. Personal Access Token (recommended for automation)"
echo "   - Go to: https://github.com/settings/tokens"
echo "   - Generate new token with 'repo' scope"
echo "   - Run: ./PUSH_TO_GITHUB.sh token <YOUR_TOKEN>"
echo ""
echo "3. SSH Key (most secure)"
echo "   - Add SSH key to GitHub: https://github.com/settings/ssh/new"
echo "   - Run: ./PUSH_TO_GITHUB.sh ssh"
echo ""
echo "4. Manual Git commands"
echo "   - See SETUP_GUIDE.md for manual instructions"
echo ""
echo "Current status:"
echo "  - Local commits: $(git log --oneline | wc -l)"
echo "  - Files ready: $(find . -type f ! -path './.git/*' ! -path './.gitignore' | wc -l)"
echo "  - Git remote: $(git remote get-url origin)"
echo ""

# Check if token was provided
if [ "$1" = "token" ] && [ -n "$2" ]; then
    TOKEN="$2"
    echo "Using provided token..."
    git remote set-url origin "https://hayden2585-sudo:${TOKEN}@github.com/hayden2585-sudo/SoniscoreData.git"
    git push origin main
    if [ $? -eq 0 ]; then
        echo "✓ Successfully pushed to GitHub!"
        echo "  Repository: https://github.com/hayden2585-sudo/SoniscoreData"
    else
        echo "✗ Failed to push. Check your token and try again."
    fi
elif [ "$1" = "ssh" ]; then
    echo "Switching to SSH..."
    git remote set-url origin git@github.com:hayden2585-sudo/SoniscoreData.git
    git push origin main
    if [ $? -eq 0 ]; then
        echo "✓ Successfully pushed to GitHub!"
        echo "  Repository: https://github.com/hayden2585-sudo/SoniscoreData"
    else
        echo "✗ Failed to push. Make sure your SSH key is added to GitHub."
    fi
else
    echo "No authentication method specified."
    echo ""
    echo "Please choose one of the options above."
    echo ""
    echo "Quick start (if you have GitHub CLI):"
    echo "  gh auth login"
    echo "  ./PUSH_TO_GITHUB.sh"
    echo ""
    echo "Or with token:"
    echo "  ./PUSH_TO_GITHUB.sh token YOUR_TOKEN_HERE"
    echo ""
    echo "Or with SSH:"
    echo "  ./PUSH_TO_GITHUB.sh ssh"
fi