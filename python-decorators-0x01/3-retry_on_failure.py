import time
import sqlite3
import functools

# ---------------------------------------
# 🧩 Decorator 1: handle database connection automatically
# ---------------------------------------
def with_db_connection(func):
    """Opens a database connection before running the function,
    passes it as an argument, and closes it afterward."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # connect to the SQLite DB file
        try:
            result = func(conn, *args, **kwargs)  # pass connection to the function
            return result
        finally:
            conn.close()  # ensure connection is closed even if error occurs
    return wrapper

# ---------------------------------------
# 🧩 Decorator 2: retry_on_failure
# ---------------------------------------
def retry_on_failure(retries=3, delay=2):
    """Retries the wrapped function if it fails due to an exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    print(f"Attempt {attempt} of {retries}...")
                    return func(*args, **kwargs)  # try to execute the function and exit the for loop because of'return'
                except Exception as e:
                    print(f"❌ Error: {e}")
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)  # wait before retrying
                    else:
                        print("All retry attempts failed.")
                        raise  # re-raise last exception after final failure
        return wrapper
    return decorator

# ---------------------------------------
# 🧩 Using both decorators
# ---------------------------------------
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """Fetch all users from the database, with automatic retry on failure."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# ---------------------------------------
# 🚀 Run function
# ---------------------------------------
try:
    users = fetch_users_with_retry()
    print("✅ Users fetched successfully:")
    print(users)
except Exception as e:
    print(f"❌ Operation failed after retries: {e}")
