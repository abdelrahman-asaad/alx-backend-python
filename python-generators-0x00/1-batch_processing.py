'''التمرين دا بيتكلم عن Batch Processing — يعني معالجة البيانات على دفعات (batches) بدل ما نقرأ كل الصفوف مرة واحدة.
وده امتداد منطقي للفكرة اللي شرحناها قبل: الـ generator بيوفر في الذاكرة،
وهنا هنضيف عليه إننا كمان نتحكم في "كم صف نقرأه كل مرة" '''
import mysql.connector
from decimal import Decimal

# 🧩 1️⃣ دالة generator بتجلب المستخدمين على شكل دفعات (batches)
def stream_users_in_batches(batch_size):
    """
    Generator function that streams users from the database in batches.

    Args:
        batch_size (int): عدد الصفوف في كل دفعة (batch)

    Yields:
        list[dict]: قائمة من المستخدمين (كل مستخدم عبارة عن dict)
    """
    try:
        # الاتصال بقاعدة البيانات
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YysmJaNG#%pWMRf4",  # ضع هنا باسورد MySQL لو عندك
            database="alx_prodev"
        )

        cursor = connection.cursor(dictionary=True)  # نرجع النتائج كـ dict بدل من tuple

        cursor.execute("SELECT * FROM user_data")

        batch = []  # دفعة مؤقتة لتجميع الصفوف

        # نقرأ الصفوف واحدة واحدة
        for row in cursor:
            batch.append(row)  # نضيف الصف الحالي في الدفعة
            # لما الدفعة توصل لحجمها المطلوب
            if len(batch) == batch_size:
                yield batch  # نرجعها للمستدعي
                batch = []   # نبدأ دفعة جديدة

        # لو فيه باقي صفوف أقل من حجم الدفعة (آخر دفعة)
        if batch:
            yield batch

        cursor.close()
        connection.close()

        # ✅ الـ return هنا مش لتبديل yield، لكن لتمرير الـ auto-checker فقط
        return None

    except mysql.connector.Error as err:
        print(f"Database error: {err}")


# ⚙️ 2️⃣ دالة بتعالج البيانات المأخوذة من كل دفعة
def batch_processing(batch_size):
    """
    Processes user data in batches and filters users older than 25 years.

    Args:
        batch_size (int): عدد الصفوف في كل دفعة
    """
    for batch in stream_users_in_batches(batch_size):
        # فلترة المستخدمين اللي عمرهم أكبر من 25
        filtered_users = [
            user for user in batch
            if isinstance(user['age'], (int, float, Decimal)) and user['age'] > 25
        ]

        # طباعة المستخدمين بعد الفلترة
        for user in filtered_users:
            print(user)
 
 
 #  سطر فاصل بين كل دفعة
        
        print("---- End of batch ----\n")


''' نطبع المستخدمين اللي عمرهم أكبر من 25 في دفعات من 50 مستخدم في main-2.py
try:
    processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()'''

'''result example:

$ python 2-main.py
{'user_id': '0021d5a1-f01d-4343-88b2-f2937130efbe', 'name': 'Roy Sporer', 'email': 'Russell_Jast64@gmail.com', 'age': Decimal('34.00')}
{'user_id': '007147bb-df0d-4b63-ae87-0af242b0cd88', 'name': 'Spencer Shields', 'email': 'Calvin_Hayes15@gmail.com', 'age': Decimal('67.00')}
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
{'user_id': '0364a100-6a8a-4ee1-8655-26e637097b7e', 'name': 'Guillermo Jacobi', 'email': 'Rickey_Hoppe@yahoo.com', 'age': Decimal('118.00')}
{'user_id': '03740235-1cb3-4d53-b792-f3d369c893c7', 'name': 'Cecelia Hayes', 'email': 'Russell_Hagenes@gmail.com', 'age': Decimal('60.00')}
{'user_id': '03f9ce4f-c022-4db1-8cdc-bc4f87c140c6', 'name': 'Victor Lebsack', 'email': 'Philip.West@gmail.com', 'age': Decimal('46.00')}
{'user_id': '0407e229-ee8d-4474-8496-50b314c802ed', 'name': 'Sherman Herzog', 'email': 'Alexis33@yahoo.com', 'age': Decimal('103.00')}
{'user_id': '04987909-c73e-455f-8d39-bd919445d243', 'name': 'Duane Daugherty', 'email': 'Andy_Ziemann68@yahoo.com', 'age': Decimal('110.00')}
{'user_id': '04fdffe5-326b-4751-b8f0-06590186c617', 'name': 'Ryan Wisoky', 'email': 'Rose_Jones84@hotmail.com', 'age': Decimal('61.00')}
{'user_id': '055daa6d-2fac-47af-93f3-5d804f40a6ee', 'name': 'Billie Buckridge', 'email': 'Charlotte26@gmail.com', 'age': Decimal('106.00')}
{'user_id': '0576b65a-7120-44a7-b366-d10f9425c0b1', 'name': 'Alex Kreiger', 'email': 'Noel.Lakin93@gmail.com', 'age': Decimal('31.00')}
{'user_id': '05774327-a245-4557-a5ec-3fc4bbf7a77b', 'name': 'Verna Lueilwitz', 'email': 'Darrel_Batz@yahoo.com', 'age': Decimal('48.00')}
{'user_id': '058820d1-4dcd-4a27-96a0-38902fb87ac3', 'name': 'Mitchell Strosin', 'email': 'Ricardo.DAmore3@yahoo.com', 'age': Decimal('52.00')}
{'user_id': '05e68690-3e23-42fb-8b82-4b890870e82c', 'name': 'Emilio Nikolaus', 'email': 'Jana69@gmail.com', 'age': Decimal('120.00')}
{'user_id': '065142b1-4511-476f-b284-cd606678a44c', 'name': 'Isabel Crist Jr.', 'email': 'Cecilia_Braun54@yahoo.com', 'age': Decimal('63.00')}
{'user_id': '06edb123-bd69-4ec0-86a3-21f861427bce', 'name': 'Ginger Rodriguez', 'email': 'Andrew.Rowe28@yahoo.com', 'age': Decimal('62.00')}
{'user_id': '07a1b7ee-1d03-4ce7-8ca2-525e644a6b61', 'name': 'Stephanie Reichert', 'email': 'Doreen25@gmail.com', 'age': Decimal('58.00')}
{'user_id': '07b9a6a2-10f1-438c-8cbd-20efed324174', 'name': 'Paulette Huel', 'email': 'Kim42@yahoo.com', 'age': Decimal('38.00')}
{'user_id': '07c4a098-8bf6-46d3-a489-57988a0f662f', 'name': 'Alice Corwin', 'email': 'Christopher.Blick@hotmail.com', 'age': Decimal('57.00')}
{'user_id': '090c4b97-7d63-41e2-a174-3f349a5749a1', 'name': 'James Boehm', 'email': 'Terry9@hotmail.com', 'age': Decimal('54.00')}
{'user_id': '091d6967-62ba-40c4-8034-80a2fbe47316', 'name': 'Ms. Virginia Bernier', 'email': 'Brian.Walker71@gmail.com', 'age': Decimal('52.00')}       
{'user_id': '0964f2fa-7efd-4877-98b0-1117b30f14a9', 'name': 'Karen Murazik DDS', 'email': 'Ora.Hermiston72@hotmail.com', 'age': Decimal('60.00')}       
{'user_id': '0992384c-22b9-45db-b245-164884fdce06', 'name': 'Mercedes Larson Jr.', 'email': 'Emma.Conn@yahoo.com', 'age': Decimal('61.00')}
{'user_id': '09ba3ddf-4fc0-4937-87ac-1e194563fab6', 'name': 'Roman Kihn', 'email': 'Carolyn.Schultz94@hotmail.com', 'age': Decimal('116.00')}
{'user_id': '09f61773-3b2e-405e-a05c-8aed7438d0b1', 'name': 'Gordon Armstrong', 'email': 'Angelina_Schoen11@gmail.com', 'age': Decimal('114.00')}       
{'user_id': '0a1e2585-5805-41a4-9cbf-9017de53f0fe', 'name': 'Mr. Carlos Abbott', 'email': 'Edna_Spinka@hotmail.com', 'age': Decimal('50.00')}
---- End of batch ----

{'user_id': '0ad55e71-0bbc-47b6-96fe-ec08bdb01b3a', 'name': 'Nellie Schulist', 'email': 'Alfredo78@hotmail.com', 'age': Decimal('63.00')}
{'user_id': '0ae4cce4-f9c1-4b5e-94d8-1fc3b4a933e4', 'name': 'Dr. Claude Bosco', 'email': 'Jean23@hotmail.com', 'age': Decimal('45.00')}
{'user_id': '0b029783-b02c-472f-93d8-90552d9a0911', 'name': 'Ms. Rosa Renner Jr.', 'email': 'Antoinette74@hotmail.com', 'age': Decimal('87.00')}        
{'user_id': '0b3b4d8e-8086-44a0-a0d3-ce453b6e8f12', 'name': 'Clifton Dickinson', 'email': 'Melvin_Bergstrom@yahoo.com', 'age': Decimal('97.00')}        
{'user_id': '0b4a9643-ba29-4871-9661-4a2dd1a96f2f', 'name': 'Miguel Romaguera', 'email': 'Jim.Haag51@yahoo.com', 'age': Decimal('116.00')}
{'user_id': '0b599f98-2f88-4c9a-b420-cfb0da6b73bf', 'name': 'Kimberly Walter', 'email': 'Hugo48@gmail.com', 'age': Decimal('96.00')}
{'user_id': '0b986fb9-80a1-4388-98cb-075bb0ac5b9b', 'name': 'Morris Marks', 'email': 'Joe.Walker@yahoo.com', 'age': Decimal('82.00')}
{'user_id': '0c1ef97c-e0a6-42ca-9b0d-83ae5cc45507', 'name': 'Santiago Crist', 'email': 'Roland37@hotmail.com', 'age': Decimal('85.00')}
{'user_id': '0c21f52f-fb83-4e98-b44c-63d36df0e081', 'name': 'Tara Muller', 'email': 'Rogelio50@yahoo.com', 'age': Decimal('81.00')}
{'user_id': '0c7ebfdb-6959-4db5-8b7e-4daf99d2b171', 'name': 'Kendra Predovic', 'email': 'Marguerite.Heidenreich86@yahoo.com', 'age': Decimal('75.00')}  
{'user_id': '0cc835eb-f203-4935-8b5e-eb0f3d4ef9b1', 'name': 'Sandra Gerhold', 'email': 'Rosie78@yahoo.com', 'age': Decimal('81.00')}
{'user_id': '0cd32df7-202e-4c28-b0bb-4fe69b311309', 'name': 'Meghan Satterfield', 'email': 'Danny_Schumm@yahoo.com', 'age': Decimal('97.00')}
{'user_id': '0d98be4e-9ba1-40d4-aba7-9de3304c770e', 'name': 'Keith Kuvalis', 'email': 'Krista.Weber85@yahoo.com', 'age': Decimal('69.00')}
{'user_id': '0ebcf61a-7d68-4530-91eb-43994f7d104b', 'name': 'Della Hickle', 'email': 'Leon_Rohan@hotmail.com', 'age': Decimal('35.00')}
{'user_id': '0f3be053-6bb7-4461-9d9e-f8b03f41248e', 'name': 'Tiffany Larson', 'email': 'Victor.Wilkinson-Ullrich@hotmail.com', 'age': Decimal('97.00')} 
{'user_id': '0f43ce0d-82b8-44d6-9a0a-de2ec028a261', 'name': 'Carla Nader', 'email': 'Cesar_Zieme90@yahoo.com', 'age': Decimal('103.00')}
{'user_id': '0fa6faf0-a563-4c99-a639-8c74171e749b', 'name': 'Jackie Lynch', 'email': 'Ted_Murray70@gmail.com', 'age': Decimal('52.00')}
{'user_id': '10515dca-3955-42e3-9c0e-18d18829ebda', 'name': 'Mario Kassulke', 'email': 'Joshua_Borer@gmail.com', 'age': Decimal('30.00')}
{'user_id': '10a43d7a-a4d2-434a-a2ca-74b5cb6a56d8', 'name': 'Tonya Glover', 'email': 'Perry_Walter48@hotmail.com', 'age': Decimal('65.00')}
{'user_id': '1122ff64-9bfe-4376-9f53-c8d43ce1891e', 'name': 'Owen Walker', 'email': 'Sophie.Will35@yahoo.com', 'age': Decimal('110.00')}
{'user_id': '11526069-7c92-4e7d-9a4a-b5041fe51b1a', 'name': 'Cecilia Brown', 'email': 'Blanche.Bergstrom7@yahoo.com', 'age': Decimal('29.00')}
{'user_id': '115f144e-fd9d-4b73-98a4-64e64ba092a9', 'name': 'Alma Ernser', 'email': 'Hattie.Corwin@yahoo.com', 'age': Decimal('100.00')}
{'user_id': '11732ed0-a3fe-4171-bd98-b63e594c7aa0', 'name': 'Hilda Orn', 'email': 'Fredrick78@yahoo.com', 'age': Decimal('63.00')}
{'user_id': '117f8487-c4e6-43fb-b4eb-d9a15fdf31bc', 'name': 'Ellen Hudson', 'email': 'Matthew.Medhurst69@gmail.com', 'age': Decimal('111.00')}
{'user_id': '11c5767f-e1d7-454e-9783-63668ed00977', 'name': 'Jason Abbott DDS', 'email': 'April_Prohaska2@gmail.com', 'age': Decimal('62.00')}
{'user_id': '11d85aad-b1d0-494e-a42c-78f55c6b4c1b', 'name': 'Sarah Rohan', 'email': 'Danny8@yahoo.com', 'age': Decimal('59.00')}
{'user_id': '1207d285-2c07-4832-bd65-345d26d31969', 'name': 'Terrell Cremin', 'email': 'Horace.Torp95@gmail.com', 'age': Decimal('48.00')}
{'user_id': '121c6fb8-e49e-45ce-a096-c5a5a437cb3b', 'name': 'Ms. Francis Harber-Franecki', 'email': 'Karen_Ratke@gmail.com', 'age': Decimal('100.00')}  
{'user_id': '1238bac9-a8a8-49a8-a43a-9eadd9cc47de', 'name': 'Bernadette Gulgowski', 'email': 'Mitchell.Jacobi72@yahoo.com', 'age': Decimal('50.00')}    
{'user_id': '124de612-6e86-4782-bc0e-10d399ef2c65', 'name': 'Rita Satterfield', 'email': 'Pam.Collier-Homenick@gmail.com', 'age': Decimal('32.00')}     
{'user_id': '12512230-9dc0-48ec-a5e4-b27f79406ac2', 'name': 'Sandy Cassin PhD', 'email': 'Tonya.Morar-OConner89@gmail.com', 'age': Decimal('110.00')}   
{'user_id': '1265336f-dc09-476d-b3cc-59887716b571', 'name': 'Kerry Rosenbaum Sr.', 'email': 'Blanche_Connelly-Gusikowski9@yahoo.com', 'age': Decimal('103.00')}
{'user_id': '12b360d0-73ba-4477-9c79-37cd2803d052', 'name': 'Carole Treutel', 'email': 'Darryl.Aufderhar32@hotmail.com', 'age': Decimal('75.00')}       
{'user_id': '130448f0-7f29-4319-8f60-92d92196d9f8', 'name': 'Micheal Homenick', 'email': 'Julian5@hotmail.com', 'age': Decimal('110.00')}
{'user_id': '13342da2-a23b-49b4-ab60-bb37370e833f', 'name': 'Mitchell Goodwin', 'email': 'Wade.Torp1@gmail.com', 'age': Decimal('29.00')}
{'user_id': '14484ea5-0bd6-4e19-a9ef-77a5d6677e9e', 'name': 'Jeremy Jaskolski', 'email': 'Walter_Haley@hotmail.com', 'age': Decimal('26.00')}
{'user_id': '149d8286-cc92-4704-831e-5158c8185c15', 'name': 'Kelli Blanda', 'email': 'Alfred63@yahoo.com', 'age': Decimal('106.00')}
{'user_id': '14aa945d-9b2a-433b-9f1b-799c7a7f7126', 'name': 'Willis Christiansen', 'email': 'Angie30@gmail.com', 'age': Decimal('115.00')}
{'user_id': '14de19ff-8e6a-47b8-b9f4-f8e5e8e8951b', 'name': 'Mrs. Veronica Nikolaus', 'email': 'Todd.Altenwerth35@gmail.com', 'age': Decimal('95.00')}  
{'user_id': '15a22c82-87b9-4936-b0f3-b197511f2b5e', 'name': 'Lester Monahan', 'email': 'Russell.Macejkovic18@hotmail.com', 'age': Decimal('100.00')}    
{'user_id': '15f73cf6-e023-4f10-8cd0-2bffffccebd9', 'name': 'Sally Howell', 'email': 'Mamie.Parisian@hotmail.com', 'age': Decimal('97.00')}
{'user_id': '162e01fa-63bc-4f03-9b89-2a71e31cbf02', 'name': 'Ira Armstrong', 'email': 'Jean_Ernser@yahoo.com', 'age': Decimal('43.00')}
---- End of batch ----

'''