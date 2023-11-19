import sqlite3
from sqlite3 import Error
from datetime import datetime

# CONSTANTS
FILE = "messages.db"
MESSAGES_TABLE = "Messages"

class DataBase:
    """
    Used to connect, write to, and read from a local sqlite3 database.
    """
    def __init__(self):
        """
        Try to connect to the file and create a cursor.
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(FILE)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self._create_table()

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()

    def _create_table(self):
        """
        Create a new database table if one doesn't exist.
        """
        query = f"""CREATE TABLE IF NOT EXISTS {MESSAGES_TABLE}
                    (name TEXT, content TEXT, time DATE, id INTEGER PRIMARY KEY AUTOINCREMENT)"""
        self.cursor.execute(query)
        self.conn.commit()

    def get_all_messages(self, limit=100, name=None):
        """
        Retrieve all messages from the Messages table.

        :param limit: int, Maximum number of messages to retrieve (default is 100)
        :param name: str, Optional filter for messages by a specific user (default is None)
        :return: list[dict], List of messages as dictionaries
        """
        if not name:
            # If no specific user is provided, retrieve all messages
            query = f"SELECT * FROM {MESSAGES_TABLE} LIMIT ?"
            self.cursor.execute(query, (limit,))
        else:
            # If a specific user is provided, retrieve messages for that user
            query = f"SELECT * FROM {MESSAGES_TABLE} WHERE name = ? LIMIT ?"
            self.cursor.execute(query, (name, limit))

        result = self.cursor.fetchall()

        # Format the messages as dictionaries
        results = []
        for r in sorted(result, key=lambda x: x[2], reverse=True)[:limit]:
            name, content, date, _id = r
            data = {"name": name, "message": content, "time": str(date)}
            results.append(data)

        return list(reversed(results))

    def get_messages_by_name(self, name, limit=100):
        """
        Gets a list of messages by user name.

        :param name: str, User name
        :param limit: int, Maximum number of messages to retrieve (default is 100)
        :return: list[dict], List of messages as dictionaries
        """
        return self.get_all_messages(limit, name)

    def save_message(self, name, msg):
        """
        Save the given message in the Messages table.

        :param name: str, User name
        :param msg: str, Message content
        """
        query = f"INSERT INTO {MESSAGES_TABLE} VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (name, msg, datetime.now(), None))
        self.conn.commit()
