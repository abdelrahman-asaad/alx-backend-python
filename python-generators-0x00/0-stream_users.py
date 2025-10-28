import mysql.connector

def stream_users():
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YysmJaNG#%pWMRf4",
            database="ALX_prodev"
        )

        # استخدم cursor بميزة buffered
        cursor = connection.cursor(dictionary=True, buffered=True)

        # نفّذ الاستعلام
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        # استخدم yield لإرجاع صف واحد كل مرة
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        # اتأكد إن الاتصال بيتقفل بعد ما الجينريتور يخلص
        if cursor:
            cursor.close()
        if connection:
            connection.close()

'''
result
{'user_id': '0021d5a1-f01d-4343-88b2-f2937130efbe', 'name': 'Roy Sporer', 'email': 'Russell_Jast64@gmail.com', 'age': Decimal('34.00')}
{'user_id': '00329655-4894-472c-9ca7-8652f644c50c', 'name': 'Dr. Laurence Thiel', 'email': 'Laurie.Lemke20@yahoo.com', 'age': Decimal('22.00')}
{'user_id': '007147bb-df0d-4b63-ae87-0af242b0cd88', 'name': 'Spencer Shields', 'email': 'Calvin_Hayes15@gmail.com', 'age': Decimal('67.00')}
{'user_id': '00b4fb6e-ad99-4717-a07b-329cf51753a1', 'name': 'Tammy Gerhold IV', 'email': 'Fred_Koelpin@hotmail.com', 'age': Decimal('14.00')}
{'user_id': '00c86421-cb39-463d-a488-1cbd11456256', 'name': 'Dr. Kristine Buckridge', 'email': 'Bryant.Schmitt@hotmail.com', 'age': Decimal('92.00')}   
{'user_id': '00e54b68-c2a8-49a5-8f05-4629c7c35a59', 'name': 'Nancy Mueller', 'email': 'Jimmy_Wolf@yahoo.com', 'age': Decimal('42.00')}

شرح سريع:
main-1.py ➜ الملف اللي بيستخدم الفنكشن.stream_users ➜ الفنكشن اللي بتعمل streaming للبيانات.
# islice جلب أول 6 مستخدمين ➜ بنستخدم عشان نجيب أول 6 صفوف بس.

mysql.connector.connect ➜ يفتح اتصال بقاعدة البيانات.

cursor(dictionary=True) ➜ يخلي الصفوف تطلع في شكل dict بدل tuple.

for row in cursor: ➜ ده اللوب الوحيد اللي بيعمل streaming صف واحد في المرة.

yield row ➜ بيرجع الصف الحالي بدون تحميل كل البيانات في الذاكرة (وده الفرق بين generator و list).

استخدام yield هنا بيخلي الكود يستهلك الذاكرة تدريجيًا بدل ما يحمل كل البيانات مرة واحدة.

this is a generator function ➜ الفنكشن دي بتولد قيم واحدة واحدة بدل ما ترجع كل القيم مرة واحدة.
this is memory efficient ➜ لأنها بتستخدم ذاكرة أقل لما بتتعامل مع بيانات كبيرة.
this is useful for large datasets ➜ مفيدة لما يكون عندك بيانات كتير في قاعدة البيانات.
this avoids loading everything into memory at once ➜ بتجنب تحميل كل حاجة في الذاكرة مرة واحدة.
this ensures connections are closed properly ➜ ده بيضمن إن الاتصالات بتتقفل بشكل صحيح بعد الاستخدام.
this handles database errors gracefully ➜ ده بيتعامل مع أخطاء قاعدة البيانات بشكل لطيف.
this allows iteration over database rows one at a time ➜ ده بيسمح بالتكرار على صفوف قاعدة البيانات واحد واحد.
instead of fetching all rows at once ➜ بدل ما تجيب كل الصفوف مرة واحدة.
using buffered cursor ➜ باستخدام cursor بميزة buffered.
this is important for generators ➜ ده مهم للجينريتورز.
used in the context of streaming database results ➜ بيستخدم في سياق streaming لنتائج قاعدة البيانات.
and fetching rows one by one ➜ وجلب الصفوف واحد واحد.




🎯 الفكرة العامة

لما تكتب كود عادي زي ده:

cursor.execute("SELECT * FROM user_data")
rows = cursor.fetchall()


فـ fetchall() بتـ تجيب كل الصفوف مرة واحدة من قاعدة البيانات وتحطها في الذاكرة (RAM).
يعني لو عندك 100 ألف صف، كلهم بيتحملوا في الميموري قبل ما تبدأ تتعامل معاهم.

🧠 النتيجة:

سريع في الحالات الصغيرة ✅

لكن مع البيانات الكبيرة → بيستهلك ذاكرة ضخمة جدًا ❌

⚙️ إنما الـ Generator بيغيّر ده تمامًا

لما نعمل كده:

def stream_users():
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row


فكل مرة تستخدم next() على المولد (اللي بيحصل ضمنيًا في الـ for loop)،
بيتم قراءة صف واحد فقط من قاعدة البيانات وإرجاعه.

يعني:

مافيش تحميل كامل لكل الصفوف.

بيجيب صف واحد في كل دورة → يستخدمه → بعدين يجيب اللي بعده.

🧩 مثال توضيحي

تخيل عندك جدول فيه 1,000,000 صف.

الطريقة القديمة (fetchall):

البرنامج هيستنى قاعدة البيانات ترجع المليون صف كلهم.

هيتخزنوا في قائمة ضخمة في RAM.

بعدين يبدأ يعالجهم واحد واحد.

الطريقة بالمولد (generator):

البرنامج بياخد صف واحد، يعالجه، بعدين يطلب الصف اللي بعده.

الذاكرة مش بتتراكم.

البرنامج ممكن يشتغل بشكل “streaming” حتى لو الجدول حجمه كبير جدًا.

💡 الميزة الفعلية
المعيار	fetchall()	generator (yield)
الأداء مع البيانات الصغيرة	أسرع شوية	مماثل تقريبًا
الأداء مع البيانات الكبيرة	بطئ جدًا بسبب الذاكرة	سريع وثابت
استهلاك الذاكرة	ضخم جدًا	شبه صفر
وقت البداية	لازم يستنى كل النتائج	يبدأ فورًا
🔥 مثال عملي على الفرق
السيناريو	عدد الصفوف	استهلاك الذاكرة
fetchall()	1,000,000	ممكن يوصل 500MB أو أكتر
generator	1,000,000	أقل من 10MB
🧠 الخلاصة

استخدام generator في التعامل مع البيانات من قاعدة البيانات هو نوع من الـ streaming
اللي بيخلي الكود:

أسرع في البداية

أخف على الذاكرة

وأكثر كفاءة خاصة لما تكون البيانات كبيرة جدًا
'''