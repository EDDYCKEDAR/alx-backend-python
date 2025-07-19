#!/usr/bin/env python3
"""Unit tests for client module."""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        # Set up mock return value
        expected_payload = {"name": org_name, "id": 123}
        mock_get_json.return_value = expected_payload

        # Create client instance and call org
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert get_json was called once with expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Assert result is as expected
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url property."""
        # Define known payload with repos_url
        known_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        # Patch org property to return known payload
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = known_payload

            # Create client and test _public_repos_url
            client = GithubOrgClient("google")
            result = client._public_repos_url

            # Assert result matches expected repos_url
            self.assertEqual(result, known_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos method."""
        # Define test payload for repos
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]
        mock_get_json.return_value = test_repos_payload

        # Define expected repos_url
        expected_repos_url = "https://api.github.com/orgs/google/repos"

        # Patch _public_repos_url property
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = expected_repos_url

            # Create client and test public_repos
            client = GithubOrgClient("google")
            result = client.public_repos()

            # Expected result should be list of repo names
            expected_result = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_result)

            # Assert _public_repos_url property was accessed once
            mock_repos_url.assert_called_once()

            # Assert get_json was called once with expected URL
            mock_get_json.assert_called_once_with(expected_repos_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license method."""
        client = GithubOrgClient("google")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test cases for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up class method to start patcher."""
        def get_json_side_effect(url):
            """Side effect function for mocked requests.get().json()"""
            if url == "https://api.github.com/orgs/google":
                return cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                return cls.repos_payload
            else:
                return {}

        # Start patcher for requests.get
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Configure mock to use side_effect
        mock_response = Mock()
        mock_response.json.side_effect = get_json_side_effect
        cls.mock_get.return_value = mock_response

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos method."""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with license filter."""
        client = GithubOrgClient("google")
        repos = client.public_repos("apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
