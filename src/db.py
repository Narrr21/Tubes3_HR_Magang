import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="resume_db"  # ganti sesuai database Kaggle-mu
    )
