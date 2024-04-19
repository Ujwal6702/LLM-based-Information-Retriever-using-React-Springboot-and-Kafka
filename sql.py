import mysql.connector

password = "MySqL@123"

def create_database():
    try:
        # Establishing connection to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password
        )

        # Creating a cursor object using the cursor() method
        cursor = connection.cursor()

        # Creating a database if it doesn't exist
        cursor.execute("DROP DATABASE IF EXISTS NexGenDB")
        cursor.execute("CREATE DATABASE IF NOT EXISTS NexGenDB")

        print("Database created successfully")

    except mysql.connector.Error as error:
        print("Failed to create database: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def create_table():
    try:
        # Establishing connection to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="NexGenDB"
        )

        # Creating a cursor object using the cursor() method
        cursor = connection.cursor()

        # SQL query to create a table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            auth VarChar(100) NOT NULL
        )
        """

        drop_table_query = """
        DROP TABLE IF EXISTS users
        """

        # Executing the SQL query
        cursor.execute(drop_table_query)
        cursor.execute(create_table_query)
        print("Table created successfully")

    except mysql.connector.Error as error:
        print("Failed to create table: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def create_chat_history_table():
    try:
        # Establishing connection to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="NexGenDB"
        )

        # Creating a cursor object using the cursor() method
        cursor = connection.cursor()

        # SQL query to create a table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS chat_history (
            chat_id INT AUTO_INCREMENT,
            user_id INT,
            topic VARCHAR(20),
            history TEXT,
            PRIMARY KEY(chat_id, user_id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """

        drop_table_query = """
        DROP TABLE IF EXISTS chat_history
        """

        # Executing the SQL query
        cursor.execute(drop_table_query)
        cursor.execute(create_table_query)
        print("Table created successfully")

    except mysql.connector.Error as error:
        print("Failed to create table: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    # Call the functions to create the database and the table
    create_database()
    create_table()
    create_chat_history_table()
