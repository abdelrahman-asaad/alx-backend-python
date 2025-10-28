import mysql.connector
import csv
import uuid
import os

# 1️⃣ Connect to MySQL server (بدون تحديد قاعدة بيانات)
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YysmJaNG#%pWMRf4"  # لو عندك باسورد ضيفها هنا
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None


# 2️⃣ Create database ALX_prodev if it doesn’t exist
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("✅ Database ALX_prodev created or already exists.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")


# 3️⃣ Connect to the ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YysmJaNG#%pWMRf4",  # نفس الباسورد هنا
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None


# 4️⃣ Create user_data table if not exists
def create_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("✅ Table user_data created successfully.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")


# 5️⃣ Insert data from a local CSV file
def insert_data(connection, csv_filename):
    try:
        if not os.path.exists(csv_filename):
            print(f"❌ File {csv_filename} not found.")
            return

        cursor = connection.cursor()
        with open(csv_filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                # Skip duplicates by email
                cursor.execute("SELECT email FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone():
                    continue

                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, age))
                count += 1

        connection.commit()
        print(f"✅ Inserted {count} new records from {csv_filename}.")
        cursor.close()

    except Exception as e:
        print(f"Error inserting data: {e}")

