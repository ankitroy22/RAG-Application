import mysql.connector 
from mysql.connector import Error
from cryptography.fernet import Fernet
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Literal


app = FastAPI()

class UserSignUp(BaseModel):

    name: Annotated[str, Field(..., description="user Full Name")]
    designation : Annotated[Literal["Marketing", "Finance", "HR", "Engineering", "general", "C-level"], Field(..., description="user designation or team")]
    username : Annotated[str, Field(..., description="User username")]
    password : Annotated[str, Field(..., description="user password")]

class UserLogin(BaseModel):
    username : Annotated[str, Field(..., description="user username")]
    password : Annotated[str, Field(..., description="user password")]

def create_key():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    try:
        with open("encryption_key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        return create_key()
key = load_key()
cipher_suite = Fernet(key)

def encrypt_password(password, cipher_suite):
    encrypt_password_ = password.encode("utf-8")
    encrypted_password = cipher_suite.encrypt(encrypt_password_)
    return encrypted_password

def decrypt_password(encrypted_password, cipher_suite):
    decrypted_password_ = cipher_suite.decrypt(encrypted_password)
    return decrypted_password_.decode("utf-8")


def create_db(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS rag")
    except Error as e:
        print("Error occurred:", e)


def create_table_user(conn):
    try:
        cursor = conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS users (username VARCHAR(50) NOT NULL UNIQUE, 
                name VARCHAR(50) NOT NULL, designation VARCHAR(50) NOT NULL, 
                PRIMARY KEY (username));"""
        cursor.execute(query)
        conn.commit()
    except Error as e:
        print("Error occurred:", e)
    

def create_table_pass(conn):
    try:
        cursor = conn.cursor()
        query = """
                CREATE TABLE IF NOT EXISTS password (username VARCHAR(50) NOT NULL UNIQUE, password BLOB);
                """
        cursor.execute(query)
        conn.commit()
    except Error as e:
        print("Error occurred:", e)

@app.post("/signup")
def sign_up(data: UserSignUp):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            encrypted_password = encrypt_password(data.password, cipher_suite)
            cursor.execute("SELECT username FROM users WHERE username=%s", (data.username,))
            result = cursor.fetchone()
        
            if result:
                return JSONResponse(status_code=409, content={"detail": "User alreday exists"})

            else:

                query1 = """
                        INSERT INTO  users (username, name, designation)
                        VALUES (%s, %s, %s)
                        """
                param1 =(data.username, data.name, data.designation)
                cursor.execute(query1, param1)
                query2= """
                        INSERT INTO password (username, password)
                        VALUES (%s, %s)
                        """
                param2 = (data.username, encrypted_password)
                cursor.execute(query2, param2)
                conn.commit()
                return JSONResponse(status_code=200, content={"detail": "user registration successfully"})
    
        except Error as e:
            print("Error Occured ", e)
            JSONResponse(status_code=500, content={"detail": "Server error"})
        
        finally:
            if conn:
                conn.close()

@app.post("/login")
def login(data: UserLogin):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
                SELECT password FROM password WHERE username = %s
                """
        param = (data.username,)
        cursor.execute(query, param)
        encrypted_password = cursor.fetchone()
        
        
        if encrypted_password:
            encrypted_password = encrypted_password[0]
            decrypted_password = decrypt_password(encrypted_password, cipher_suite)
            if data.password == decrypted_password:
                return JSONResponse(status_code=200, content={"detail": "login successfully"})
            else:
                return JSONResponse(status_code=401, content={"detail":"wrong credential"})
        else:
            return JSONResponse(status_code=401, content={"detail":"wrong credential"})
            
    except Error as e:
        print("Error occurred:", e)
        return JSONResponse(status_code=500, content={"detail": "server error"})

    finally:
        if conn:
            conn.close()

def get_designation(conn, username):
    cursor = conn.cursor()
    query = """
            SELECT designation FROM users WHERE username = %s
            """
    cursor.execute(query, (username,))
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_name(conn, username):
    cursor = conn.cursor()
    query = """
            SELECT name FROM users WHERE username = %s
            """
    cursor.execute(query, (username,))
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_connection():
    conn = mysql.connector.connect(
            host = "localhost",
            port = 3306,
            username= "root",
            password = "ankit22",
            database = "rag"
        )
    return conn


if __name__ == "__main__":
    conn = mysql.connector.connect(
        host = "localhost",
        port = 3306,
        username = "root",
        password = "ankit22"
    )
    cursor = conn.cursor()
    conn = create_db()
    create_table_pass(conn)
    create_table_user(conn)




