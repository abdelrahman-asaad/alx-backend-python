import sqlite3
import functools
from datetime import datetime  # to store the time of query

# 🔹 decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # to store the time of query
        if query:
            print(f"[{timestamp}] Executing SQL Query: {query}")
        else:
            print(f"[{timestamp}] No SQL query provided.")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor() # to create database object to excute database queyries
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# 🔹 fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")


''' 🔍 الشرح

استخدمنا functools.wraps للحفاظ على اسم ووصف الدالة الأصلية.

الديكوريتر log_queries:

يطبع الاستعلام (SQL Query) قبل تنفيذه.

بعد الطباعة، ينفذ الدالة الأصلية fetch_all_users.

لو ما كانش فيه query، بيطبع رسالة توضيحية.'''