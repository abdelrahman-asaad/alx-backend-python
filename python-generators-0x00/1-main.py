#!/usr/bin/python3
import importlib.util
from itertools import islice

# Load the module dynamically
spec = importlib.util.spec_from_file_location("stream_users", "./0-stream_users.py")
stream_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stream_module)

# استخدم الفنكشن من الموديول
for user in islice(stream_module.stream_users(), 6): # جلب أول 6 مستخدمين
    print(user)
