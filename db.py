import sqlite3
from response import Response

db_file = 'db.sqlite'
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
