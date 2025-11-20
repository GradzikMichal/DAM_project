import psycopg2
import socket


class DB_connection:
    database_ip = socket.gethostbyname("postgres-db")

    def __init__(self, database, user, password, database_ip=database_ip):
        self.database = database
        self.user = user
        self.host = database_ip
        self.password = password
        self.cursor = None
        self.conn = None
        self.create_connection()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def create_connection(self):
        self.conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            host=self.host,
            password=self.password,
        )
        self.cursor = self.conn.cursor()

    def select_fields(self, fields, source="images", where_clause=None):
        if where_clause is not None:
            query = "SELECT " + fields + " FROM " + source + " WHERE " + where_clause + ";"
        else:
            query = "SELECT " + fields + " FROM " + source + ";"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        self.conn.commit()
        return results

    def insert_value(self, img_name, folder_path, u_id):
        query = "select add_image('" + img_name + "', '" + folder_path + "', '" + u_id + "');"
        self.cursor.execute(query)
        results = self.cursor.fetchall()[0][0]
        self.conn.commit()
        return results

