import mysql.connector

def stream_users():
    """Generator that streams rows from user_data table one by one"""
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YysmJaNG#%pWMRf4",      # ضع الباسورد لو عندك
            database="alx_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        # Yield each row one by one
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

'''شرح سريع:
main-1.py ➜ الملف اللي بيستخدم الفنكشن.stream_users ➜ الفنكشن اللي بتعمل streaming للبيانات.
# islice جلب أول 6 مستخدمين ➜ بنستخدم عشان نجيب أول 6 صفوف بس.

mysql.connector.connect ➜ يفتح اتصال بقاعدة البيانات.

cursor(dictionary=True) ➜ يخلي الصفوف تطلع في شكل dict بدل tuple.

for row in cursor: ➜ ده اللوب الوحيد اللي بيعمل streaming صف واحد في المرة.

yield row ➜ بيرجع الصف الحالي بدون تحميل كل البيانات في الذاكرة (وده الفرق بين generator و list).'''