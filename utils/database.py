import mysql.connector
from mysql.connector import errorcode

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            user='root', 
            password='12345678',
            host='localhost',
            database='enigma_bot_db'
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está mal con tu usuario o contraseña")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(err)
    return None

def create_tables():
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INT AUTO_INCREMENT PRIMARY KEY,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            history_id INT AUTO_INCREMENT PRIMARY KEY,
            session_id INT,
            role VARCHAR(10),
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
        """)
        conn.commit()
        cursor.close()
        conn.close()

create_tables()
