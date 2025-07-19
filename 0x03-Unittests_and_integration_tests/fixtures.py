#!/usr/bin/env python3
"""Test fixtures for GitHub organization client tests."""

# Sample test payload for integration tests
TEST_PAYLOAD = [
    (
        # org_payload
        {
            "login": "google",
            "id": 1342004,
            "url": "https://api.github.com/orgs/google",
            "repos_url": "https://api.github.com/orgs/google/repos",
            "name": "Google",
            "description": "Google ❤️ Open Source"
        },
        # repos_payload  
        [
            {
                "id": 7697149,
                "name": "episodes.dart",
                "full_name": "google/episodes.dart",
                "private": False,
                "license": {
                    "key": "bsd-3-clause",
                    "name": "BSD 3-Clause \"New\" or \"Revised\" License"
                }
            },
            {
                "id": 8566972,
                "name": "kratu",
                "full_name": "google/kratu", 
                "private": False,
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0"
                }
            },
            {
                "id": 7776515,
                "name": "build-debian-cloud",
                "full_name": "google/build-debian-cloud",
                "private": False,
                "license": {
                    "key": "apache-2.0", 
                    "name": "Apache License 2.0"
                }
            }
        ],
        # expected_repos
        ["episodes.dart", "kratu", "build-debian-cloud"],
        # apache2_repos
        ["kratu", "build-debian-cloud"]
    )
]
