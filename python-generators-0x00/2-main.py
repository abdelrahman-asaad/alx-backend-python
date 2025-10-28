#!/usr/bin/python3
import sys

# ✅ نستورد الملف رغم إن اسمه يبدأ برقم
processing = __import__('1-batch_processing')

# نطبع المستخدمين اللي عمرهم أكبر من 25 في دفعات من 50 مستخدم
try:
    processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()
