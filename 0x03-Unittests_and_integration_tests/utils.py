#!/usr/bin/env python3
def access_nested_map(nested_map, path):
    for key in path:
        nested_map = nested_map[key]
    return nested_map

#ex
nested_map = {"a":1}
path = ("a",)

print(access_nested_map(nested_map, path))  # should return nested_map["a"] which is 1
# output: 1

print(access_nested_map({"a": {"b": 2}}, ("a",)))  
# output: {'b': 2}


print(access_nested_map({"a": {"b": 2},"b":3 }, ("a","b"))) 
# output: 2 
#         nested_map["a"] is {"b": 2} >> so the nested_map becomes {"b": 2} 
#         then in second iteration key is "b" >> so nested_map["b"] is 2

print(access_nested_map({"a": {"b": 2}}, ("a", "b"))) #should return nested_map["b"] which is 2
# output: 2

#explanation:
# in first iteration key is "a", so nested_map becomes 1 >> then in second iteration there is no second 
# iteration as path has only one element.



#________
def access_nested_mapp(nested_map, path):
    for key in path:
        nested_mapp = nested_map[key]
        print(nested_mapp)
    


access_nested_mapp({"a": {"b": 2},"b":3 }, ("a","b"))
# output: {'b': 2}
#          3
#________________________________
#!/usr/bin/env python3
"""Generic utilities for HTTP requests and memoization."""

import requests
from functools import wraps
from typing import Callable, Dict


def get_json(url: str) -> Dict:

    response = requests.get(url)
    return response.json()

    """Get JSON content from a remote URL.

    Parameters
    ----------
    url : str
        The URL to send the GET request to.

    Returns
    -------
    Dict
        The JSON response converted to a dictionary.
    """
    
#________________________________________

def memoize(fn: Callable) -> Callable:
    '''Decorator to memoize a method's return value.'''

    
    attr_name = "_{}".format(fn.__name__) 
    #if fn.__name__ is "a_method", attr_name will be "_a_method"
    #to ensure that the memoized function retains the original function's metadata


    #@wraps(fn)
    def memoized(self):
        """Wrapper that caches the result of the method."""
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self)) #excute fn(self) and store the result in attr_name
        return getattr(self, attr_name)

    return property(memoized)
#property is a built-in decorator that allows you to define methods in a class that can be accessed like
#  attributes.

#wraps is a built-in decorator from functools module that preserves the original function's 
# metadata like its name and docstring when it is decorated.

#مثال كامل مع النتيجة

class MyClass:
    @memoize
    def a_method(self): 
        print("a_method called")
        return 42

obj = MyClass()

# أول مرة
print(obj.a_method) #it doesn't have attribute _a_method yet
# Output:
# a_method called (printed because it's the first call)
# 42                (the return value)

# ثاني مرة
print(obj.a_method)
# Output:
# 42   (دون طباعة لأن القيمة محفوظة في الكاش)
# ويحفظ القيمة 42 في attr_name اللي هو "_a_method" 

#شرح الكود:
#attr_name = "_a_method"
#setattr(self, attr_name, 42)       # تخزن القيمة 42 في self._a_method
#result = getattr(self, attr_name)  # ترجع القيمة اللي مخزنة → 42

# so that attr_name becomes "_a_method" which equals 42 when fn(self) is called.


'''✅ النتيجة النهائية:

attr_name = "_a_method" (string)

self._a_method = 42 (actual cached value)

getattr(self, attr_name) → 42  '''

#المسار الداخلي:

#obj.a_method → يستدعي memoized(self=obj).

#hasattr(obj, "_a_method") → False → ينفذ fn(self) → يحسب 42 → يخزن في _a_method.

#يعيد القيمة المخزنة.

#المرات القادمة → hasattr(obj, "_a_method") → True → يرجع مباشرة _a_method.
#_______________________________________
#ex
from functools import wraps

# نعرف decorator باسم greet_decorator
def greet_decorator(fn):
    @wraps(fn)
    def wrapper():
        print("Calling function")
        return fn()
    return wrapper

# نستخدمه على دالة greet
@greet_decorator
def greet():
    """Print a greeting"""
    print("Hello")

greet()
print(greet.__name__)  # greet
print(greet.__doc__)   # Print a greeting
#_________________
#ex
#🔍 مثال عملي يوضح الفرق
#بدون @wraps

from functools import wraps

def my_decorator(fn):
    def wrapper():
        """This is the wrapper docstring"""
        print("قبل")
        fn()
        print("بعد")
    return wrapper

@my_decorator
def say_hi():
    """This says hi"""
    print("Hi")

print(say_hi.__name__)  # ❌ يطبع wrapper
print(say_hi.__doc__)   # ❌ يطبع "This is the wrapper docstring"

#_______________

#مع @wraps

from functools import wraps

def my_decorator(fn):
    @wraps(fn)  # <-- هنا بنحافظ على الاسم والـ docstring
    def wrapper():
        print("قبل التنفيذ")
        fn()
        print("بعد التنفيذ")
    return wrapper


@my_decorator  # <-- دي الصح
def say_hi():
    """This says hi"""
    print("Hi")


print(say_hi.__name__)  # يطبع: say_hi ✅
print(say_hi.__doc__)   # يطبع: This says hi ✅
say_hi()
# قبل التنفيذ
# Hi
# بعد التنفيذ
