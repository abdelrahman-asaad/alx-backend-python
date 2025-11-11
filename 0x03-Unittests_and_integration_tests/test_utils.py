#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map  # دالة المفروض موجودة في utils.py


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        # nested_map    ,       path, expected_result
    ])
    def test_access_nested_map(self, nested_map, path, expected): #starts with test_method 
        """Test that access_nested_map returns the expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

#@parameterized.expand is a decorator that allows you to run a test_method multiple times with different
# sets of parameters.

'''@parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ({"a": {"b": 2}}, ("a", "b"), 2),
])
كل tuple بتتحول تلقائيًا إلى مجموعة من الباراميترات اللي هتتبعت للدالة test_access_nested_map.

يعني:

python
نسخ الكود
def test_access_nested_map(self, nested_map, path, expected):
أول قيمة في tuple → nested_map

ثاني قيمة → path

ثالث قيمة → expected'''
#___________________
#!/usr/bin/env python3
"""Unit tests for utils.get_json using mock HTTP calls."""

import unittest
from unittest.mock import patch, Mock
from utils import get_json


class TestGetJson(unittest.TestCase):
    """Test case for utils.get_json function."""

    def test_get_json(self):
        """Test that get_json returns the expected payload using mocked requests.get."""
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_cases:
            with patch("utils.requests.get") as mock_get:
                mock_response = Mock()
                mock_response.json.return_value = test_payload
                mock_get.return_value = mock_response

                result = get_json(test_url)

                # Check that requests.get was called exactly once with the test_url
                mock_get.assert_called_once_with(test_url)

                # Check that get_json returns the mocked payload
                self.assertEqual(result, test_payload)

#payload is the data you get back from an API call, usually in JSON format
# like {"key": "value"}
#{payload: True} is just an example of such data
#assert_called_once_with is a method provided by the unittest.mock library in Python.
# It is used to verify that a mocked method was called exactly one time with the specified arguments