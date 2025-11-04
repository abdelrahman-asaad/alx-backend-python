import sqlite3
import functools

# ===============================
# 🔹 Decorator 1: إدارة الاتصال بقاعدة البيانات
# ===============================
def with_db_connection(func):
    """
    Decorator لإنشاء اتصال بقاعدة البيانات وتمريره للفنكشن
    - يفتح الاتصال قبل التنفيذ
    - يغلق الاتصال بعد التنفيذ
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # فتح الاتصال بقاعدة البيانات (users.db)
        conn = sqlite3.connect('users.db')
        try:
            # تمرير الاتصال للفنكشن
            result = func(conn, *args, **kwargs) #function calling with passing 'conn' argument to it and store its value in 'result'
            return result
        
        
        finally: #after executing the function within its whole decorators مهمة جداً
            # إغلاق الاتصال بعد الانتهاء (حتى لو حصل خطأ)
            conn.close()
    return wrapper


# ===============================
# 🔹 Decorator 2: إدارة المعاملات (Transactions)
# ===============================
def transactional(func):
    """
    Decorator لإدارة الـ transaction (عملية قاعدة البيانات)
    - يعمل COMMIT لو العملية نجحت
    - يعمل ROLLBACK لو حصل خطأ أثناء التنفيذ
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # تنفيذ الدالة (العملية على قاعدة البيانات)
            result = func(conn, *args, **kwargs) #calling function and storing its value in 'result'
            
            # ✅ لو نجحت العملية → نحفظ التغييرات
            conn.commit()
            return result
        
        except Exception as e:
            # ❌ لو حصل خطأ → نلغي التغييرات
            conn.rollback()
            print(f"Transaction failed! Rolled back due to: {e}")
        
    return wrapper


# ===============================
# 🔹 استخدام الـ Decorators معًا
# ===============================
@with_db_connection               #excuted first till 'finally'        # it passes 'conn' as an argument to function 
@transactional                    #excuted second then continue to 'finally' in @with_db_connection
def update_user_email(conn, user_id, new_email):
    """
    دالة لتحديث إيميل المستخدم في قاعدة البيانات.
    بتستخدم:
    - with_db_connection لفتح وغلق الاتصال تلقائيًا
    - transactional لضمان تنفيذ آمن للـ transaction
    """
    cursor = conn.cursor()  # إنشاء كائن cursor لتنفيذ أوامر SQL
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"✅ Email updated successfully for user ID: {user_id}")


# ===============================
# 🔹 تنفيذ التحديث
# ===============================
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')




'''💡 شرح مبسط للتدفق:

finally بتتنفذ بعد ما الدالة تخلص تنفيذ كل الديكيروترز

الترتيب كده:

with_db_connection يبدأ → يفتح الاتصال.

transactional يبدأ → ينفذ الكويري.

بعد التنفيذ، transactional يعمل:

commit() أو rollback()

ويدخل في finally بتاعه.

بعد ما يخلص، with_db_connection يدخل في finally بتاعه → يقفل الاتصال.

'''