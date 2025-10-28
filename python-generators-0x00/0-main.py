#!/usr/bin/python3
import seed

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print("✅ Connection successful")

    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')

        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES LIKE 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print("✅ Database ALX_prodev is present.")
        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        print(cursor.fetchall())
        cursor.close()
        connection.close()

