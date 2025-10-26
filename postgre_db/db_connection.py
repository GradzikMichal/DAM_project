import psycopg2

if __name__ == "__main__":
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        host="localhost:5432",
        password="123",
    )

    cursor = conn.cursor()
