#!/usr/bin/python3
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination

try:
    # نجلب البيانات صفحة بصفحة
    for page in lazy_paginator(20):
        for user in page:
            print(user)

except BrokenPipeError:
    sys.stderr.close()
