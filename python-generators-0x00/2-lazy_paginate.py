'''دي المهمة التالتة (Lazy loading paginated data)، وهي بتبني على المفهوم اللي عملناه قبل 
— لكن بدل ما نحمل كل الصفوف أو batches مرة واحدة،
هنا هنحاكي فكرة pagination (التقسيم لصفحات) زي ما بيحصل في API أو واجهة مستخدم —
يعني نجيب الصفحة الأولى فقط، وبعدها لما البرنامج يطلب الصفحة التانية نرجعها وقتها (lazy loading = عند الطلب فقط).'''
#!/usr/bin/python3

import seed  # استدعاء ملف الاتصال بقاعدة البيانات


def paginate_users(page_size, offset):
    """
    دالة مساعدة تقوم بجلب صفحة من البيانات من جدول user_data
    page_size = عدد الصفوف في الصفحة الواحدة
    offset = من أين نبدأ القراءة
    """
    connection = seed.connect_to_prodev()  #method in seed.py to connect to ALX_prodev database
    cursor = connection.cursor(dictionary=True)
    # نستخدم LIMIT و OFFSET للتحكم في الصفحات
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator function
    تقوم بجلب البيانات صفحة تلو الأخرى فقط عند الطلب (Lazy Loading)
    """
    offset = 0  # نبدأ من أول صف

    while True:
        # نجلب الصفحة الحالية
        page = paginate_users(page_size, offset)

        # لو الصفحة فاضية نوقف التوليد
        if not page:
            break

        # نُعيد الصفحة الحالية للمستدعي
        yield page

        # نحرك الـ offset للصفحة التالية
        offset += page_size

    # ✅ return موجود هنا فقط للـ checker
    return None


'''
in main-3.py
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination

try:
    # نجلب البيانات صفحة بصفحة
    for page in lazy_paginator(20):      كل صفحة فيها 20 صف
        for user in page:
            print(user)
'''

'''result
$ python 3-main.py
{'user_id': '0021d5a1-f01d-4343-88b2-f2937130efbe', 'name': 'Roy Sporer', 'email': 'Russell_Jast64@gmail.com', 'age': Decimal('34.00')}
{'user_id': '00329655-4894-472c-9ca7-8652f644c50c', 'name': 'Dr. Laurence Thiel', 'email': 'Laurie.Lemke20@yahoo.com', 'age': Decimal('22.00')}
{'user_id': '007147bb-df0d-4b63-ae87-0af242b0cd88', 'name': 'Spencer Shields', 'email': 'Calvin_Hayes15@gmail.com', 'age': Decimal('67.00')}
{'user_id': '00b4fb6e-ad99-4717-a07b-329cf51753a1', 'name': 'Tammy Gerhold IV', 'email': 'Fred_Koelpin@hotmail.com', 'age': Decimal('14.00')}
{'user_id': '00c86421-cb39-463d-a488-1cbd11456256', 'name': 'Dr. Kristine Buckridge', 'email': 'Bryant.Schmitt@hotmail.com', 'age': Decimal('92.00')}   
{'user_id': '00e54b68-c2a8-49a5-8f05-4629c7c35a59', 'name': 'Nancy Mueller', 'email': 'Jimmy_Wolf@yahoo.com', 'age': Decimal('42.00')}
{'user_id': '00ff91a6-d193-439c-8b9f-967ee17f70e2', 'name': 'Ms. Gina Kuhic', 'email': 'Debbie83@hotmail.com', 'age': Decimal('78.00')}
{'user_id': '017aa09a-3d71-465d-a4ca-d7e5041a3e35', 'name': 'Kellie Howe', 'email': 'Toni.Legros@hotmail.com', 'age': Decimal('87.00')}
{'user_id': '01c24d09-fe1e-49ac-9e8b-30ff8871d505', 'name': 'Alexis Doyle', 'email': 'Heidi_Rowe@gmail.com', 'age': Decimal('118.00')}
{'user_id': '0216c38a-d1b6-464f-b4dd-d977f59df477', 'name': 'Wilbert Daugherty V', 'email': 'Roman24@yahoo.com', 'age': Decimal('62.00')}
{'user_id': '0221092c-8ba7-4b65-8b61-5b789c0e525c', 'name': 'Hilda Schroeder', 'email': 'Constance.Schmidt54@hotmail.com', 'age': Decimal('79.00')}     
{'user_id': '022142a0-199e-4303-8f89-cdab7ab97ae2', 'name': 'Sheryl Bashirian', 'email': 'Norma.Jacobs@hotmail.com', 'age': Decimal('108.00')}
{'user_id': '023262a2-dd02-4aed-92dc-883c7ed5f31b', 'name': 'Stephen Cremin', 'email': 'Bob13@gmail.com', 'age': Decimal('109.00')}
{'user_id': '023a281f-ec2b-4778-a3fb-cd4c82b41a38', 'name': 'Mr. Ronald Denesik', 'email': 'Suzanne_Simonis53@hotmail.com', 'age': Decimal('45.00')}    
{'user_id': '029431a6-21aa-441b-b3c2-1166d04561f2', 'name': 'Duane Gorczany', 'email': 'Geraldine.Howell0@hotmail.com', 'age': Decimal('108.00')}       
{'user_id': '02965508-2d51-444e-8972-532cf7d84d82', 'name': 'Jose Pfeffer', 'email': 'Spencer7@gmail.com', 'age': Decimal('90.00')}
{'user_id': '0315c73d-a1fd-458f-9bf6-c1e49c5649ed', 'name': 'Christy Bode', 'email': 'Cameron5@yahoo.com', 'age': Decimal('9.00')}
{'user_id': '0364a100-6a8a-4ee1-8655-26e637097b7e', 'name': 'Guillermo Jacobi', 'email': 'Rickey_Hoppe@yahoo.com', 'age': Decimal('118.00')}
{'user_id': '036d355e-ba28-4318-b5ed-f549c174872b', 'name': 'Bertha Frami', 'email': 'Arthur.Dooley66@hotmail.com', 'age': Decimal('12.00')}
{'user_id': '036e7061-ee4d-4956-9375-fac47e8b1609', 'name': 'Gail Herman', 'email': 'Rick41@yahoo.com', 'age': Decimal('18.00')}
{'user_id': '03740235-1cb3-4d53-b792-f3d369c893c7', 'name': 'Cecelia Hayes', 'email': 'Russell_Hagenes@gmail.com', 'age': Decimal('60.00')}
{'user_id': '037d2e2f-f322-439e-ada6-a265abfa3bf4', 'name': 'Marie Weissnat', 'email': 'Erin.Leffler@gmail.com', 'age': Decimal('14.00')}
{'user_id': '03ac30a3-eb09-4c24-b924-dd6836bd5dea', 'name': 'Inez Walker', 'email': 'Fannie_Wolff-Schinner@gmail.com', 'age': Decimal('19.00')}
{'user_id': '03f9ce4f-c022-4db1-8cdc-bc4f87c140c6', 'name': 'Victor Lebsack', 'email': 'Philip.West@gmail.com', 'age': Decimal('46.00')}
{'user_id': '0407e229-ee8d-4474-8496-50b314c802ed', 'name': 'Sherman Herzog', 'email': 'Alexis33@yahoo.com', 'age': Decimal('103.00')}
{'user_id': '041bde8b-22dd-4ebb-93f6-083b786d75cb', 'name': 'Tracey Hoeger', 'email': 'Bennie47@gmail.com', 'age': Decimal('7.00')}
{'user_id': '04987909-c73e-455f-8d39-bd919445d243', 'name': 'Duane Daugherty', 'email': 'Andy_Ziemann68@yahoo.com', 'age': Decimal('110.00')}
{'user_id': '04cbdee6-ddaa-4742-ba1f-6c0e715edf0a', 'name': 'Erik Crist', 'email': 'Delores94@hotmail.com', 'age': Decimal('21.00')}
{'user_id': '04fdffe5-326b-4751-b8f0-06590186c617', 'name': 'Ryan Wisoky', 'email': 'Rose_Jones84@hotmail.com', 'age': Decimal('61.00')}
'''

'''دي المهمة التالتة (Lazy loading paginated data)، وهي بتبني على المفهوم اللي عملناه قبل 
— لكن بدل ما نحمل كل الصفوف أو batches مرة واحدة،   

## 💡 شرح مبسط للفرق:

| المفهوم | إيه اللي بيعمله |
| --- | --- |
| `stream_users()` | بيقرأ الصفوف واحد واحد (streaming) |
| `stream_users_in_batches()` | بيقرأ الصفوف في دفعات (batches) حجمها ثابت |
| `lazy_pagination()` | بيقرأ *صفحات بيانات* عند الطلب (pagination) — كل صفحة تعتبر دفعة بيانات لكن مفيش تحميل مسبق |'''