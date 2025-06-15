import mysql.connector
import dotenv
import os
from encryption.encryption import encrypt_ecc, encrypt_spn
import traceback

dotenv.load_dotenv()  # Load environment variables from .env file
DB_HOST = os.getenv("DB_HOST") 
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD") 
DB_NAME = os.getenv("DB_NAME")

def encrypt_seed():
    conn = None  
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        read_cursor = conn.cursor(dictionary=True)
        write_cursor = conn.cursor()

        read_cursor.execute("SELECT * FROM ApplicantProfilePlain")
        all_applicants = read_cursor.fetchall()

        for applicant in all_applicants:
            applicant_id = applicant['app_id']

            key = os.urandom(32)

            first_name_encrypted = encrypt_spn(applicant['first_name'], key)
            last_name_encrypted = encrypt_spn(applicant['last_name'], key)
            dob_encrypted = encrypt_spn(str(applicant['date_of_birth']), key)
            address_encrypted = encrypt_spn(applicant['address'], key)
            phone_encrypted = encrypt_spn(applicant['phone_number'], key)

            (C1_x, C1_y), encrypted_key = encrypt_ecc(key)

            sql_insert_profile = """
                INSERT INTO ApplicantProfile 
                (applicant_id, first_name, last_name, date_of_birth, address, phone_number) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            profile_data = (
                applicant_id, first_name_encrypted, last_name_encrypted,
                dob_encrypted, address_encrypted, phone_encrypted
            )
            write_cursor.execute(sql_insert_profile, profile_data)

            sql_insert_params = """
                INSERT INTO EncryptionParameters (applicant_id, C1_x, C1_y, SPN_key) 
                VALUES (%s, %s, %s, %s)
            """
            params_data = (applicant_id, C1_x.to_bytes(32, "big"), C1_y.to_bytes(32, "big"), encrypted_key)
            write_cursor.execute(sql_insert_params, params_data)
        conn.commit()

        read_cursor.close()
        write_cursor.close()
        conn.close()
    except Exception as e:
        traceback.print_exc()

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
    encrypt_seed()

    with open("src/database/application_seed.sql", 'r', encoding='utf-8') as f:
        sql_commands = f.read()

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