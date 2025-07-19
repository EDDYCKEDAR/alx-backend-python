#!/usr/bin/env python3
"""GitHub organization client module."""

from functools import cached_property
from typing import List, Dict, Any, Optional
from utils import get_json


class GithubOrgClient:
    """A client for accessing GitHub organization data."""
    
    def __init__(self, org_name: str):
        """Initialize the client with organization name."""
        self.org_name = org_name
    
    @cached_property
    def org(self) -> Dict[Any, Any]:
        """Get organization data from GitHub API."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)
    
    @property
    def _public_repos_url(self) -> str:
        """Get the public repos URL for the organization."""
        return self.org["repos_url"]
    
    def public_repos(self, license: Optional[str] = None) -> List[str]:
        """Get list of public repositories, optionally filtered by license."""
        repos_data = get_json(self._public_repos_url)
        
        if license:
            return [
                repo["name"] for repo in repos_data
                if self.has_license(repo, license)
            ]
        
        return [repo["name"] for repo in repos_data]
    
    @staticmethod
    def has_license(repo: Dict[Any, Any], license_key: str) -> bool:
        """Check if repository has the specified license."""
        repo_license = repo.get("license")
        if repo_license is None:
            return False
        return repo_license.get("key") == license_key
