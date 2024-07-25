import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables
load_dotenv()

# Connection settings
HOST = os.getenv('host')
USER = os.getenv('user')
PASSWORD = os.getenv('password')
DATABASE = os.getenv('database')


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='GoodOmens2018',
            database='practice'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

def read_committed_demo():
    connection1 = create_connection()
    connection2 = create_connection()

    cursor1 = None
    cursor2 = None

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='READ COMMITTED')
        cursor1.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")

        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='READ COMMITTED')
        cursor2.execute("SELECT * FROM accounts WHERE id = 1")

        print("READ COMMITTED result:", cursor2.fetchall())

        connection1.commit()  # Ensure the transaction is committed
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1:
            connection1.rollback()  # Rollback if not committed
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2:
            connection2.close()

if __name__ == "__main__":
    read_committed_demo()
