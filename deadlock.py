import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import datetime
import time
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


def deadlock():
    """
    Demonstrates a deadlock scenario.
    """
    connection1 = create_connection()
    connection2 = create_connection()

    cursor1 = None
    cursor2 = None

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        # Transaction 1: Update Alice
        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='READ COMMITTED')
        cursor1.execute("UPDATE accounts SET balance = balance - 100 WHERE name = 'Alice'")
        print(f"Transaction 1 updated Alice's balance")

        # Transaction 2: Update Bob
        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='READ COMMITTED')
        cursor2.execute("UPDATE accounts SET balance = balance + 100 WHERE name = 'Bob'")
        print(f"Transaction 2 updated Bob's balance")

        # Transaction 1 tries to update Bob
        print(f"Transaction 1 waiting for lock on Bob: {datetime.now()}")
        cursor1.execute("UPDATE accounts SET balance = balance - 100 WHERE name = 'Bob'")
        print(f"Transaction 1 updated Bob's balance")

        # Transaction 2 tries to update Alice
        print(f"Transaction 2 waiting for lock on Alice: {datetime.now()}")
        cursor2.execute("UPDATE accounts SET balance = balance + 100 WHERE name = 'Alice'")
        print(f"Transaction 2 updated Alice's balance")

        connection1.commit()
        connection2.commit()

    except Error as e:
        print(f"Error: {e}")
        if connection1:
            connection1.rollback()
        if connection2:
            connection2.rollback()
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()


if __name__ == "__main__":
    deadlock()
