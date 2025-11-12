#!/usr/bin/env python3
"""
Test module for utils functions
"""

#!/usr/bin/env python3
"""
Test module for utils functions
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct value"""
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main()


class TestGetJson(unittest.TestCase):
    """Test cases for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_requests_get):
        """
        Test that get_json returns the expected result and makes the correct HTTP call
        """
        # Configure the mock to return a response with the test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_requests_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Test that the mocked get method was called exactly once with test_url
        mock_requests_get.assert_called_once_with(test_url)
        
        # Test that the output of get_json is equal to test_payload
        self.assertEqual(result, test_payload)


if __name__ == '__main__':
    unittest.main()

#_____________________    
'''#!/usr/bin/env python3
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

if __name__ == "__main__":
    unittest.main()        

#@parameterized.expand is a decorator that allows you to run a test_method multiple times with different
# sets of parameters.'''

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
"""
Test module for utils.get_json function
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json


class TestGetJson(unittest.TestCase):
    """Test cases for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test that get_json returns the expected result and makes the correct HTTP call
        """
        # Create a mock response object not to perform real HTTP requests
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Patch requests.get to return our mock response >> to replace the real requests.get with a mock
        with patch('utils.requests.get', return_value=mock_response) as mock_get:
            # Call the function
            result = get_json(test_url)

            # Test that requests.get was called exactly once with test_url
            mock_get.assert_called_once_with(test_url)
            
            # Test that the result equals test_payload
            self.assertEqual(result, test_payload)


if __name__ == '__main__':
    unittest.main()

   #______________________
    '''أمثلة تنفيذية (ماذا يحدث فعلاً لكل تكرار)

تكرار 1:

test_url = "http://example.com"

test_payload = {"payload": True}

patch يجعل requests.get("http://example.com") يرجع mock_response

get_json يرجع {"payload": True}

نتحقق mock_get.assert_called_once_with("http://example.com")

assertEqual(result, {"payload": True}) → ينجح

تكرار 2:

نفس الشيء مع "http://holberton.io" و{"payload": False}'''
#________________________________
#!/usr/bin/env python3
"""
Test module for memoize decorator
"""

import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result of a_method."""

        class TestClass:
            """Inner class to test memoization."""

            def a_method(self):
                """Method to be mocked."""
                return 42

            @memoize
            def a_property(self):
                """Method decorated with memoize."""
                return self.a_method()

        # Create instance of the class
        obj = TestClass()

        # Mock a_method
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            # First call should call a_method
            result1 = obj.a_property
            # Second call should get from cache
            result2 = obj.a_property

            # Verify the result is the same value
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Verify a_method was called only once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()