import time
import sqlite3
import functools

# 🧠 ذاكرة (Cache) لتخزين نتائج الاستعلامات حسب نص الاستعلام (query string)
query_cache = {}

def with_db_connection(func):
    """Decorator: مسؤول عن فتح وإغلاق الاتصال بقاعدة البيانات تلقائيًا"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")  # إنشاء الاتصال بملف قاعدة البيانات
        try:
            result = func(conn, *args, **kwargs)  # استدعاء الدالة وتمرير الاتصال
            return result
        finally:
            conn.close()  # إغلاق الاتصال بعد الانتهاء (حتى في حال حدوث خطأ)
    return wrapper


def cache_query(func):
    """Decorator: يقوم بتخزين نتيجة الاستعلام في cache لتجنب إعادة التنفيذ"""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # 🔍 إذا كانت نتيجة هذا الاستعلام موجودة مسبقًا في cache → استخدمها مباشرة
        if query in query_cache:
            print("✅ Using cached result for query:", query)
            return query_cache[query]

        # ⚙️ لو مش موجود → نفذ الاستعلام فعليًا
        print("🕒 Executing new query:", query)
        result = func(conn, query, *args, **kwargs)

        # 💾 خزّن النتيجة في القاموس (cache)
        query_cache[query] = result

        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """تجلب المستخدمين من قاعدة البيانات"""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# ✅ أول استدعاء → هيُنفذ الاستعلام ويحفظ النتيجة في الكاش
users = fetch_users_with_cache(query="SELECT * FROM users")

# ✅ ثاني استدعاء بنفس الاستعلام → هيستخدم الكاش بدل ما ينفذ SQL فعليًا
users_again = fetch_users_with_cache(query="SELECT * FROM users")
