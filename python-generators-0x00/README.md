0. Getting started with python generators
mandatory
Objective: create a generator that streams rows from an SQL database one by one.

Instructions:

Write a python script that seed.py:

Set up the MySQL database, ALX_prodev with the table user_data with the following fields:
user_id(Primary Key, UUID, Indexed)
name (VARCHAR, NOT NULL)
email (VARCHAR, NOT NULL)
age (DECIMAL,NOT NULL)
Populate the database with the sample data from this user_data.csv
Prototypes:
def connect_db() :- connects to the mysql database server
def create_database(connection):- creates the database ALX_prodev if it does not exist
def connect_to_prodev() connects the the ALX_prodev database in MYSQL
def create_table(connection):- creates a table user_data if it does not exists with the required fields
def insert_data(connection, data):- inserts data in the database if it does not exist
faithokoth@ubuntu:python-generators-0x00 % cat 0-main.py
#!/usr/bin/python3

seed = __import__('seed')

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print(f"connection successful")

    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')
        cursor = connection.cursor()
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present ")
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()

faithokoth@ubuntu:python-generators-0x00 % ./0-main.py
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119), ('006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49), ('00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'Ronnie Bechtelar', 'Sandra19@yahoo.com', 22), ('00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'Alma Bechtelar', 'Shelly_Balistreri22@hotmail.com', 102)]

faithokoth@h@ubuntu:python-generators-0x00 % 

Repo:

GitHub repository: alx-backend-python
Directory: python-generators-0x00
File: seed.py, README.md

$ python 0-main.py

_________________________--
1. generator that streams rows from an SQL database
mandatory
Objective: create a generator that streams rows from an SQL database one by one.

Instructions:

In 0-stream_users.py write a function that uses a generator to fetch rows one by one from the user_data table. You must use the Yield python generator

Prototype: def stream_users()
Your function should have no more than 1 loop
(venv)faithokoth@Faiths-MacBook-Pro python-generators-0x00 % cat 1-main.py 

#!/usr/bin/python3
from itertools import islice
stream_users = __import__('0-stream_users')

# iterate over the generator function and print only the first 6 rows

for user in islice(stream_users(), 6):
    print(user)

(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 %./1-main.py

{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
{'user_id': '006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'name': 'Daniel Fahey IV', 'email': 'Delia.Lesch11@hotmail.com', 'age': 49}
{'user_id': '00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'name': 'Ronnie Bechtelar', 'email': 'Sandra19@yahoo.com', 'age': 22}
{'user_id': '00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'name': 'Alma Bechtelar', 'email': 'Shelly_Balistreri22@hotmail.com', 'age': 102}
{'user_id': '01187f09-72be-4924-8a2d-150645dcadad', 'name': 'Jonathon Jones', 'email': 'Jody.Quigley-Ziemann33@yahoo.com', 'age': 116}

(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 %

Repo:

GitHub repository: alx-backend-python
Directory: python-generators-0x00
File: 0-stream_users.py, README.md

pyhon 1-main.py

_________________________
2. Batch processing Large Data
mandatory
Objective: Create a generator to fetch and process data in batches from the users database

Instructions:

Write a function stream_users_in_batches(batch_size) that fetches rows in batches

Write a function batch_processing() that processes each batch to filter users over the age of25`

You must use no more than 3 loops in your code. Your script must use the yield generator

Prototypes:

def stream_users_in_batches(batch_size)
def batch_processing(batch_size)
(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 % cat 2-main.py                
#!/usr/bin/python3
import sys
processing = __import__('1-batch_processing')

##### print processed users in a batch of 50
try:
    processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()

(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 % ./2-main.py | head -n 5 

{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}

{'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}

{'user_id': '006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'name': 'Daniel Fahey IV', 'email': 'Delia.Lesch11@hotmail.com', 'age': 49}

{'user_id': '00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'name': 'Alma Bechtelar', 'email': 'Shelly_Balistreri22@hotmail.com', 'age': 102}

{'user_id': '01187f09-72be-4924-8a2d-150645dcadad', 'name': 'Jonathon Jones', 'email': 'Jody.Quigley-Ziemann33@yahoo.com', 'age': 116}

(venv) faithokoth@Faiths-MacBook-Pro python-generators-0x00 % 

Repo:

GitHub repository: alx-backend-python
Directory: python-generators-0x00
File: 1-batch_processing.py

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

____________________________
