# Chat_with_Databases
Chat with Databases using NSQL from Numberstations and LLama-2

# Chat_with_Databases
Chat with Databases using NSQL from Numberstations and LLama-2


## Summary of the various scripts in your application:

1. **db_connectors.py** :
   - Contains classes for connecting to databases such as PostgreSQL, SQLite, and MySQL.
   - Uses SQLAlchemy to manage the connection and the execution of SQL queries.
   - Provides methods for retrieving tables, schemas, and executing SQL queries.

2. **programm_formatters.py** :
   - Defines template classes (Pydantic) to represent columns, foreign keys, and tables.
   - Implements a `RajkumarFormatter` class which formats tables into a string, builds SQL queries based on those tables, and formats the generated model results.

3. **Database_manager.py**:
   - The `DatabaseManager` class supports managing the connection to a database, initializing a natural language model, and executing SQL queries.
   - Uses the database connector classes from `db_connectors.py`.
   - Uses the `RajkumarFormatter` class to format tables and queries.

4. **Main.py**:
   - Provides a command-line user interface to interact with the Text-to-SQL application.
   - Allows the user to specify the database type, connection information, and enter queries.
   - Uses the `DatabaseManager` class to manage the application's business logic.
   - Handles errors when connecting to the database and when generating queries.


