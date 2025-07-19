#!/usr/bin/env python3
"""GitHub organization client module."""
import requests

def get_json(url):
    """Get JSON data from URL."""
    response = requests.get(url)
    return response.json()

class GithubOrgClient:
    """A client for accessing GitHub organization data."""
    
    def __init__(self, org_name):
        """Initialize the client with organization name."""
        self.org_name = org_name
        self._org_cache = None
    
    @property
    def org(self):
        """Return the organization data from the GitHub API for the specified organization name."""
        if self._org_cache is None:
            url = f"https://api.github.com/orgs/{self.org_name}"
            self._org_cache = get_json(url)
        return self._org_cache
    
    @property
    def _public_repos_url(self):
        """Get the public repos URL for the organization."""
        return self.org["repos_url"]
    
    def public_repos(self, license=None):
        """Get list of public repositories, optionally filtered by license."""
        repos_data = get_json(self._public_repos_url)
        
        if license:
            return [
                repo["name"] for repo in repos_data
                if self.has_license(repo, license)
            ]
    
        return [repo["name"] for repo in repos_data]
    
    @staticmethod
    def has_license(repo, license_key):
        """Check if repository has the specified license."""
        repo_license = repo.get("license")
        if repo_license is None:
            return False
        return repo_license.get("key") == license_key
