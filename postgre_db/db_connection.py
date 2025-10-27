import psycopg2
import socket

database_ip = socket.gethostbyname("postgres-db")
#change it to class
# cursor, conn = con.create_connection()
# cursor.close()
# conn.close()
def create_connection():
    conn = psycopg2.connect(
        database="image_db",
        user="postgres",
        host=database_ip,
        password="postgres",
    )

    cursor = conn.cursor()
    return cursor, conn


def select_fields(cursor, conn, fields, source = "images", where_clause=None):
    if where_clause is not None:
        query = "SELECT " + fields + " FROM " + source + " WHERE " + where_clause + ";"
    else:
        query = "SELECT " + fields + " FROM " + source + ";"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.commit()
    return results


def insert_values(cursor, conn, img_name, folder_path, u_id):
    query = "select add_image('"+img_name+"', '"+folder_path+"', '"+u_id+"');"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.commit()
    return results
