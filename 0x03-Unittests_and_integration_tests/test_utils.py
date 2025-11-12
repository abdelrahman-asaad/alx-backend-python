#!/usr/bin/env python3
"""
Test module for utils functions
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path,
                                         expected_exception_message):
        """
        Test that access_nested_map raises KeyError with expected message
        for invalid paths
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        # Verify the exception message matches exactly
        self.assertEqual(str(context.exception), expected_exception_message)


class TestGetJson(unittest.TestCase):
    """Test cases for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test that get_json returns the expected result
        and makes correct HTTP call
        """
        # Create a mock response object with the json method
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Patch requests.get to return our mock response
        with patch('utils.requests.get',
                   return_value=mock_response) as mock_get:
            # Call the function
            result = get_json(test_url)

            # Test that mocked get was called exactly once with test_url
            mock_get.assert_called_once_with(test_url)

            # Test that the output of get_json is equal to test_payload
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test cases for memoize decorator"""

    def test_memoize(self):
        """Test that memoize decorator caches the result properly"""
        class TestClass:
            """Test class for memoization testing"""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Create an instance of TestClass
        test_instance = TestClass()

        # Mock the a_method using patch
        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_method:
            # First call to a_property
            result1 = test_instance.a_property()

            # Second call to a_property
            result2 = test_instance.a_property()

            # Test that the correct result is returned both times
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Test that a_method was called only once
            mock_method.assert_called_once()
            