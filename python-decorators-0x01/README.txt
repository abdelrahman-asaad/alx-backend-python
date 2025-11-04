0. Logging database Queries
mandatory
Objective: create a decorator that logs database queries executed by any function

Instructions:

Complete the code below by writing a decorator log_queries that logs the SQL query before executing it.

Prototype: def log_queries()

import sqlite3
import functools

#### decorator to lof SQL queries

 """ YOUR CODE GOES HERE"""

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
Repo:

GitHub repository: alx-backend-python
Directory: python-decorators-0x01
File: 0-log_queries.py
____________________
1. Handle Database Connections with a Decorator
mandatory
Objective: create a decorator that automatically handles opening and closing database connections

Instructions:

Complete the script below by Implementing a decorator with_db_connection that opens a database connection, passes it to the function and closes it afterword
import sqlite3 
import functools

def with_db_connection(func):
    """ your code goes here""" 

@with_db_connection 
def get_user_by_id(conn, user_id): 
cursor = conn.cursor() 
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)
Repo:

GitHub repository: alx-backend-python
Directory: python-decorators-0x01
File: 1-with_db_connection.py