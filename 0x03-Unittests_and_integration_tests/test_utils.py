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

#@parameterized.expand is a decorator that allows you to run a test method multiple times with different
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
