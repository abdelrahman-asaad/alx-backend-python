#!/usr/bin/env python3
"""Module for testing the GithubOrgClient class methods.
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_result, mock_get_json):
        """
        Tests that GithubOrgClient.org returns the correct value,
        and that utils.get_json is called once with the expected URL.
        """
        # Configure the mock object to return the expected dictionary
        # The mock is the patched client.get_json
        mock_get_json.return_value = expected_result

        # Create an instance of GithubOrgClient
        client = GithubOrgClient(org_name)

        # Call the method under test
        result = client.org

        # Assert that the result matches the expected organization dictionary
        self.assertEqual(result, expected_result)

        # Construct the expected URL that get_json should have been called with
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Assert that get_json was called exactly once with the expected URL
        mock_get_json.assert_called_once_with(expected_url)

        # Note on mock_get_json: Since we are using @patch as a decorator
        # and providing a return_value, we ensure that the actual get_json
        # (which might perform an HTTP call) is never executed, fulfilling
        # the "no external HTTP calls should be made" requirement.


if __name__ == '__main__':
    unittest.main()
    
# ===== TASK 5 =====
class TestGithubOrgClientPublicReposUrl(unittest.TestCase):
    """Test cases for GithubOrgClient._public_repos_url - Task 5"""

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test GithubOrgClient._public_repos_url"""
        test_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
        mock_org.return_value = test_payload

        client = GithubOrgClient("test")
        result = client._public_repos_url

        self.assertEqual(result, test_payload["repos_url"])


# ===== TASK 6 =====
class TestGithubOrgClientPublicRepos(unittest.TestCase):
    """Test cases for GithubOrgClient.public_repos - Task 6"""

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos"""
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/test/repos"
        ) as mock_url:
            client = GithubOrgClient("test")
            result = client.public_repos()

            expected_repos = ["repo1", "repo2"]
            self.assertEqual(result, expected_repos)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once()


# ===== TASK 7 =====
class TestGithubOrgClientHasLicense(unittest.TestCase):
    """Test cases for GithubOrgClient.has_license - Task 7"""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


# ===== TASK 8 =====
@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient - Task 8"""

    @classmethod
    def setUpClass(cls):
        """Set up class for integration tests"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Side effect for requests.get mock"""
            class MockResponse:
                def __init__(self, json_data):
                    self.json_data = json_data

                def json(self):
                    return self.json_data

            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)
            return MockResponse({})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class after integration tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos integration"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license integration"""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
