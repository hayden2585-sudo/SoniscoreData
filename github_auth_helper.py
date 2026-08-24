#!/usr/bin/env python3
"""
GitHub Authentication Helper for SoniscoreData
Helps set up GitHub authentication and push changes.
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path


def check_git_installed():
    """Check if git is installed."""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_gh_cli():
    """Check if GitHub CLI is installed."""
    try:
        subprocess.run(['gh', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_gh_auth():
    """Check if GitHub CLI is authenticated."""
    if not check_gh_cli():
        return False
    
    result = subprocess.run(['gh', 'auth', 'status'], 
                          capture_output=True, text=True)
    return result.returncode == 0


def install_gh_cli():
    """Install GitHub CLI."""
    print("Installing GitHub CLI...")
    
    # Check operating system
    if sys.platform == 'darwin':  # macOS
        print("Detected macOS. Installing GitHub CLI via Homebrew...")
        if check_git_installed():
            subprocess.run(['brew', 'install', 'gh'], check=True)
            return True
        else:
            print("Error: Homebrew not found. Please install GitHub CLI manually:")
            print("https://github.com/cli/cli#installation")
            return False
    elif sys.platform == 'linux':
        print("Detected Linux. Installing GitHub CLI...")
        # Try apt-get first
        subprocess.run(['sudo', 'apt-get', 'update'], check=False)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'gh'], check=False)
        return check_gh_cli()
    else:
        print("Unknown operating system. Please install GitHub CLI manually:")
        print("https://github.com/cli/cli#installation")
        return False


def setup_gh_auth():
    """Set up GitHub CLI authentication."""
    if not check_gh_cli():
        if not install_gh_cli():
            return False
    
    print("Starting GitHub CLI authentication...")
    print("Please follow the prompts to authenticate.")
    
    # Run gh auth login
    result = subprocess.run(['gh', 'auth', 'login'], check=False)
    return result.returncode == 0


def create_github_token():
    """Create a GitHub Personal Access Token."""
    print("\nCreating GitHub Personal Access Token...")
    print("1. Go to: https://github.com/settings/tokens")
    print("2. Click 'Generate new token' → 'Generate new token (classic)'")
    print("3. Set expiration to 90 days")
    print("4. Add note: 'SoniscoreData project access'")
    print("5. Select scopes: repo, workflow")
    print("6. Click 'Generate token'")
    print("7. Copy the token and save it securely")
    print("\nOnce you have the token, run:")
    print("  git remote set-url origin https://<TOKEN>@github.com/hayden2585-sudo/SoniscoreData.git")
    return True


def test_github_connection():
    """Test connection to GitHub."""
    print("\nTesting GitHub connection...")
    
    # Test GitHub API
    try:
        response = requests.get('https://api.github.com/user', timeout=10)
        if response.status_code == 200:
            print("✓ GitHub API connection successful")
            user = response.json()
            print(f"  Logged in as: {user.get('login')}")
            return True
        elif response.status_code == 401:
            print("✗ Not authenticated with GitHub")
            return False
        else:
            print(f"✗ GitHub API returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Network error: {e}")
        return False


def update_git_remote(token=None):
    """Update Git remote with authentication."""
    repo_dir = Path(__file__).parent
    os.chdir(repo_dir)
    
    if token:
        # Use token in URL
        remote_url = f"https://{token}@github.com/hayden2585-sudo/SoniscoreData.git"
        print(f"Updating Git remote with token...")
        subprocess.run(['git', 'remote', 'set-url', 'origin', remote_url], check=True)
    else:
        print("No token provided. Using existing Git configuration.")
    
    print(f"Current remote: {subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True).stdout.strip()}")


def push_changes():
    """Push changes to GitHub."""
    repo_dir = Path(__file__).parent
    os.chdir(repo_dir)
    
    print("\nPushing changes to GitHub...")
    
    # Check if there are changes to push
    status = subprocess.run(['git', 'status', '--porcelain'], 
                          capture_output=True, text=True)
    
    if not status.stdout.strip():
        print("No changes to push.")
        return True
    
    # Try to push
    result = subprocess.run(['git', 'push', 'origin', 'main'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Successfully pushed changes to GitHub!")
        return True
    else:
        print("✗ Failed to push changes:")
        print(result.stderr)
        print("\nPlease ensure you are authenticated with GitHub.")
        return False


def main():
    """Main function."""
    print("SoniscoreData GitHub Authentication Helper")
    print("=" * 50)
    
    # Check current status
    print("\n1. Checking current status...")
    
    git_installed = check_git_installed()
    print(f"  Git installed: {'✓' if git_installed else '✗'}")
    
    gh_installed = check_gh_cli()
    print(f"  GitHub CLI installed: {'✓' if gh_installed else '✗'}")
    
    gh_authenticated = check_gh_auth() if gh_installed else False
    print(f"  GitHub authenticated: {'✓' if gh_authenticated else '✗'}")
    
    # Test GitHub connection
    github_connected = test_github_connection()
    
    if not github_connected and not gh_authenticated:
        print("\n2. Setting up authentication...")
        
        print("\nChoose authentication method:")
        print("  1. Use GitHub CLI (recommended)")
        print("  2. Create Personal Access Token")
        print("  3. Use SSH keys")
        print("  4. Skip authentication (read-only)")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            if not gh_installed:
                install_gh_cli()
            setup_gh_auth()
        elif choice == '2':
            create_github_token()
        elif choice == '3':
            print("\nSSH key setup:")
            print(f"  Public key: {Path.home()/.ssh/id_ed25519.pub}")
            print("  Add this key to: https://github.com/settings/ssh/new")
        elif choice == '4':
            print("\nProceeding with read-only access.")
        else:
            print("Invalid choice. Proceeding with read-only access.")
    
    # Try to push changes
    print("\n3. Pushing changes to GitHub...")
    
    if github_connected or gh_authenticated:
        push_changes()
    else:
        print("\nAuthentication required to push changes.")
        print("Please set up authentication and try again.")
        print("\nTo manually push:")
        print(f"  cd {Path(__file__).parent}")
        print("  git push origin main")


if __name__ == '__main__':
    main()