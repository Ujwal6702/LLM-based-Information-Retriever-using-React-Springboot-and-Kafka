import mysql.connector

password = "root"

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
            password VARCHAR(100) NOT NULL
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

def insert_into_history_table( user_id, topic, history):
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
        insert_query = f"""
        INSERT INTO TABLE chat_history VALUES (
            {user_id},
            {topic},
            {history}
        )
        """

        # Executing the SQL query
        cursor.execute(insert_query)

    except mysql.connector.Error as error:
        print("Failed to insert data to History table: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_chat_history( chat_id, user_id, history):
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
        update_query = f"""
            UPDATE chat_history SET history = {history}
            WHERE user_id = {user_id} AND chat_id = {chat_id}
        """

        # Executing the SQL query
        cursor.execute(update_query)

    except mysql.connector.Error as error:
        print("Failed to update record in History table: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def getChatHistory( chat_id, user_id ):
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
        select_query = f"""
            SELECT history FROM chat_history WHERE user_id = {user_id} AND chat_id = {chat_id} LIMIT 1
        """

        # Executing the SQL query
        cursor.execute(select_query)
        result = cursor.fetchone()

        # Extracting history from the result
        history = result[0]
        return history

    except mysql.connector.Error as error:
        print("Failed to update record in History table: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
