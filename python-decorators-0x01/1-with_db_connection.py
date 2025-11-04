import sqlite3
import functools

# 🔹 Decorator to automatically manage database connections
def with_db_connection(func):
    """
    This decorator:
    1. Opens a connection to the database before running the function.
    2. Passes the connection object (conn) to the wrapped function.
    3. Closes the connection after the function finishes executing.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # ✅ Step 1: Open a new database connection
        conn = sqlite3.connect("users.db")
        try:
            # ✅ Step 2: Pass the connection as the first argument to the wrapped function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # ✅ Step 3: Always close the connection — even if an error occurs
            conn.close()
            print("Database connection closed.")

    return wrapper


# 🔹 Example function using the decorator
@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetch a user record from the 'users' table by user_id.
    The connection (conn) is provided automatically by the decorator.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# 🔹 Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)



'''💡 شرح مختصر:

with_db_connection هو ديكوريتور (decorator) بيهتم بإدارة الاتصال بالـ database.

بيعمل:

فتح الاتصال بـ sqlite3.connect("users.db").

يمرر الاتصال تلقائيًا كأول باراميتر للـ function.

يغلق الاتصال في النهاية مهما حصل (بـ finally:).

لما تستدعي get_user_by_id(user_id=1)،
مش محتاج تفتح أو تقفل الاتصال يدويًا — الديكوريتور بيهتم بده بالكامل.'''