import sqlite3
import functools

# 🔹 decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # استخرج الاستعلام من الـ arguments
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        if query:
            print(f"Executing SQL Query: {query}")
        else:
            print("No SQL query provided.")
        # نفذ الدالة الأصلية
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
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