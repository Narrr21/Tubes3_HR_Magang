import mysql.connector
import dotenv
import os

dotenv.load_dotenv()  # Load environment variables from .env file
DB_HOST = os.getenv("DB_HOST") 
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD") 
DB_NAME = os.getenv("DB_NAME")

def seed_database():
    with open("src/database/tubes3_seeding.sql", 'r', encoding='utf-8') as f:
        sql_commands = f.read()

    # Koneksi ke database MySQL
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=True
    )
    cursor = conn.cursor()

    for command in sql_commands.split(';'):
        command = command.strip()
        if command:
            try:
                cursor.execute(command)
            except mysql.connector.Error as err:
                print(f"Error executing: {command[:30]}... → {err}")

    cursor.close()
    conn.close()
    print("SQL seeding selesai.")