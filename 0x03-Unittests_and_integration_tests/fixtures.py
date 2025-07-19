#!/usr/bin/env python3
"""Test fixtures for GitHub organization client tests."""

TEST_PAYLOAD = [
    (
        {
            "login": "google",
            "id": 1342004,
            "url": "https://api.github.com/orgs/google",
            "repos_url": "https://api.github.com/orgs/google/repos",
            "name": "Google"
        },
        [
            {
                "id": 7697149,
                "name": "episodes.dart",
                "license": {
                    "key": "bsd-3-clause",
                    "name": "BSD 3-Clause"
                }
            },
            {
                "id": 8566972,
                "name": "kratu",
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0"
                }
            },
            {
                "id": 7776515,
                "name": "build-debian-cloud",
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0"
                }
            }
        ],
        ["episodes.dart", "kratu", "build-debian-cloud"],
        ["kratu", "build-debian-cloud"]
    )
]
