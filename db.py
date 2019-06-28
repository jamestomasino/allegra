import sqlite3
from response import Response
import os

my_path = os.path.abspath(os.path.dirname(__file__))
db_file = os.path.join(my_path, './db.sqlite')

def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

class DB():

    def getResponses(self, set_name):
        """
        Query messages by set name
        :param conn: the Connection object
        :param set_name:
        :return:
        """
        conn = create_connection()
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM messages WHERE set_name=?", (set_name,))
            rows = cur.fetchall()
            responses = []
            for row in rows:
                responses.append(Response(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            return responses

    def getState(self, set_name):
        """
        Query messages by set name
        :param conn: the Connection object
        :param set_name:
        :return:
        """
        conn = create_connection()
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM states WHERE set_name=?", (set_name,))
            rows = cur.fetchall()
            state = {}
            for row in rows:
                if row[2]:
                    default_states = row[2].split(',')
                    for s in default_states:
                        state[s] = True
            return state
