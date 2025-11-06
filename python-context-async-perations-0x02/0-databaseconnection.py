import sqlite3

class DatabaseConnection:
    """Custom context manager to handle database connections automatically"""
    
    def __init__(self, database_name):
        # 🔹 هنا بنحدد اسم قاعدة البيانات اللي هنتصل بيها
        self.db_name = database_name
        self.conn = None

    def __enter__(self):
        """Executed when entering the 'with' block"""
        # 🔹 فتح الاتصال بقاعدة البيانات
        self.conn = sqlite3.connect(self.db_name)
        # 🔹 نرجّع الاتصال عشان نستخدمه داخل بلوك with
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Executed when exiting the 'with' block"""
        # 🔹 لو حصل استثناء (خطأ)، اطبعه — ممكن نضيف rollback هنا لو عايزين
        if exc_type:
            print(f"An error occurred: {exc_value}")
        # 🔹 في النهاية، اقفل الاتصال دايمًا
        if self.conn:
            self.conn.close()
        # 🔹 برجع False عشان لو حصل خطأ، ما يتمش تجاهله تلقائيًا
        return False


# ✅ استخدام الـ context manager لتنفيذ استعلام SQL
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
