import mysql.connector
from database import load_key, create_db, create_table_user, create_table_pass, get_connection
from cryptography.fernet import Fernet

# database connection
key = load_key()
cipher_suite = Fernet(key)
conn = mysql.connector.connect(
        host = "localhost",
        port = 3306,
        username = "root",
        password = "ankit22"
        )
cursor = conn.cursor()
create_db(conn)
conn = get_connection()
create_table_pass(conn)
create_table_user(conn)