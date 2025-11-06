import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        """
        db_name: اسم قاعدة البيانات (ملف SQLite)
        query: نص الاستعلام SQL
        params: القيم اللي هتتحط في الـ placeholders (لو فيه)
        """
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """هنا بنفتح الاتصال وننفذ الاستعلام"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print("✅ Database connected successfully")

        # تنفيذ الاستعلام
        self.cursor.execute(self.query, self.params)
        results = self.cursor.fetchall()

        return results  # بيرجع النتائج تلقائيًا داخل الـ "with"

    def __exit__(self, exc_type, exc_value, traceback):
        """إغلاق الاتصال بالقاعدة"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("🔒 Connection closed")

        # لو فيه خطأ، ممكن نرجع False عشان نسيبه يترافع
        if exc_type:
            print(f"⚠️ Error occurred: {exc_value}")
        return False  # False يعني ما تمشيش على الخطأ، خليه يظهر عادي


# ✅ Example usage:
if __name__ == "__main__": # to prevent execution when imported as a module , so that the code only runs when the script is executed directly.
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    # استخدام الـ context manager
    with ExecuteQuery("users.db", query, params) as results:
        print("👥 Users older than 25:")
        for row in results:
            print(row)
