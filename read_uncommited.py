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


def read_uncommited_demo():
    """
    Shows how READ UNCOMMITED isolation level works.
    Shows dirty read.
    :return: void
    """
    connection1 = create_connection()
    connection2 = create_connection()

    cursor1 = None
    cursor2 = None

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        # Transaction 1: Read Uncommitted
        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='READ UNCOMMITTED')
        cursor1.execute("UPDATE accounts SET balance = 9999 WHERE name = 'Alice'")

        # Transaction 2: Read Uncommitted
        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='READ UNCOMMITTED')
        cursor2.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        balance_dirty_read = cursor2.fetchone()[0]

        print(f"Dirty Read (READ UNCOMMITTED): Alice's balance = {balance_dirty_read}")

        print(f"Transaction 1 rollback(): {datetime.now()}")
        connection1.rollback()

        print(f"Transaction 2 commit(): {datetime.now()}")
        connection2.commit()

    except Error as e:
        print(f"Error: {e}")
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
    read_uncommited_demo()