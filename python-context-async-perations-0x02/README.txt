0. custom class based context manager for Database connection
mandatory
Objective: create a class based context manager to handle opening and closing database connections automatically

Instructions:

Write a class custom context manager DatabaseConnection using the __enter__ and the __exit__ methods

Use the context manager with the with statement to be able to perform the query SELECT * FROM users. Print the results from the query.

Repo:

GitHub repository: alx-backend-python
Directory: python-context-async-perations-0x02
File: 0-databaseconnection.py
______
1. Reusable Query Context Manager
mandatory
Objective: create a reusable context manager that takes a query as input and executes it, managing both connection and the query execution

Instructions:

Implement a class based custom context manager ExecuteQuery that takes the query: ”SELECT * FROM users WHERE age > ?” and the parameter 25 and returns the result of the query

Ensure to use the__enter__() and the __exit__() methods

Repo:

GitHub repository: alx-backend-python
Directory: python-context-async-perations-0x02
File: 1-execute.py