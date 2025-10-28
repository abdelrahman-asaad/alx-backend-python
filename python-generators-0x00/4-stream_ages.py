#!/usr/bin/python3
"""
4-stream_ages.py
Objective: Stream user ages from the database efficiently and calculate average age
"""

import seed  # نستدعي الملف اللي فيه الاتصال بقاعدة البيانات


def stream_user_ages():
    """
    Generator function that yields user ages from the database one by one
    """
    connection = seed.connect_to_prodev() # method to connect to the database in seed.py
    cursor = connection.cursor()

    # نجلب فقط الأعمار من الجدول
    cursor.execute("SELECT age FROM user_data")

    # نجلب الصفوف واحدة واحدة (lazy loading)
    for (age,) in cursor:
        yield float(age)  # نرجع كل عمر كقيمة رقمية (float) >> returns a float value for each age

    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Uses the generator to calculate the average age without loading all data
    """
    total_age = 0
    count = 0

    # حلقة واحدة فقط لجمع القيم وعدها
    for age in stream_user_ages():
        total_age += age
        count += 1

    # نحسب المتوسط إذا كان فيه بيانات
    average_age = total_age / count if count > 0 else 0

    print(f"Average age of users: {average_age:.2f}")


# 📌 تشغيل الدالة الرئيسية
if __name__ == "__main__":
    calculate_average_age()

'''
شرح الفكرة:

stream_user_ages() → generator بياخد الأعمار من SQL واحدة واحدة.

calculate_average_age() → بيستخدم القيم دي لحساب المتوسط بدون ما يحمل كل الأعمار في memory.

مافيش SQL AVG() → لأنك بتعمل التجميع بنفسك داخل Python.

عدد الحلقات = 1 (فقط في حساب المتوسط).

🔍 مثال ناتج التشغيل:
$ python 4-stream_ages.py
Average age of users: 62.42
'''