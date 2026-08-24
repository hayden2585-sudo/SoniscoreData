#!/usr/bin/env python3
"""
GitHub Authentication Helper for SoniscoreData
Uses GitHub API to create a Personal Access Token and authenticate.
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path


def check_github_token():
    """Check if GitHub token is available in environment."""
    # Check common environment variables
    for env_var in ['GITHUB_TOKEN', 'GH_TOKEN', 'GITHUB_AUTH']:
        token = os.environ.get(env_var)
        if token:
            print(f"Found GitHub token in {env_var}")
            return token
    return None


def test_github_token(token):
    """Test if a GitHub token is valid."""
    headers = {'Authorization': f'token {token}'}
    try:
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        if response.status_code == 200:
            user = response.json()
            print(f"✓ Token valid! Logged in as: {user.get('login')}")
            return True
        elif response.status_code == 401:
            print("✗ Token is invalid or expired")
            return False
        else:
            print(f"✗ GitHub API returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Network error: {e}")
        return False


def setup_git_credentials(token, username='hayden2585-sudo'):
    """Set up Git credentials with the token."""
    repo_dir = Path(__file__).parent
    os.chdir(repo_dir)
    
    # Update git remote with token
    remote_url = f"https://{username}:{token}@github.com/{username}/SoniscoreData.git"
    print(f"Updating Git remote with token...")
    subprocess.run(['git', 'remote', 'set-url', 'origin', remote_url], check=True)
    
    # Configure git credentials
    subprocess.run(['git', 'config', 'credential.helper', 'store'], check=True)
    
    print("Git credentials configured successfully!")
    return True


def push_changes():
    """Push changes to GitHub."""
    repo_dir = Path(__file__).parent
    os.chdir(repo_dir)
    
    print("\nPushing changes to GitHub...")
    
    # Try to push
    result = subprocess.run(['git', 'push', 'origin', 'main'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Successfully pushed changes to GitHub!")
        return True
    else:
        print("✗ Failed to push changes:")
        print(result.stderr)
        return False


def main():
    """Main function."""
    print("SoniscoreData GitHub Authentication Helper")
    print("=" * 50)
    
    # Check for existing token
    token = check_github_token()
    
    if token:
        print("\nTesting token...")
        if test_github_token(token):
            print("\nSetting up Git credentials...")
            setup_git_credentials(token)
            print("\nPushing changes...")
            push_changes()
        else:
            print("\nToken is invalid. Please create a new token.")
    else:
        print("\nNo GitHub token found in environment variables.")
        print("\nPlease create a GitHub Personal Access Token:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Click 'Generate new token' → 'Generate new token (classic)'")
        print("3. Set expiration to 90 days")
        print("4. Add note: 'SoniscoreData project access'")
        print("5. Select scopes: repo, workflow")
        print("6. Click 'Generate token'")
        print("7. Copy the token")
        print("\nThen set it as an environment variable:")
        print("  export GITHUB_TOKEN=<TOKEN>")
        print("\nOr run this command directly:")
        print("  git remote set-url origin https://<TOKEN>@github.com/hayden2585-sudo/SoniscoreData.git")


if __name__ == '__main__':
    main()