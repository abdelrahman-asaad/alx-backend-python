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
