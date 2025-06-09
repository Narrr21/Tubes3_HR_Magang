import random
from typing import List
import mysql.connector
import fitz 
import re
import os
from faker import Faker
from dotenv import load_dotenv
import os

class SummaryData():
    def __init__(self, nama: str, email: str, phone: str, address: str, skills: List[str], experience: List[str], education: List[str], summary: str):
        self.nama = nama
        self.email = email
        self.phone = phone
        self.address = address
        self.skills = skills
        self.experience = experience
        self.education = education
        self.summary = summary
# ------------------------------ EXTRACT TEXT FROM PDF ------------------------------

def extract_text_from_pdf(file_path: str) -> str:
    """
    Mengekstrak teks dari file PDF menjadi satu string panjang menggunakan PyMuPDF.
    
    :param file_path: Path ke file PDF
    :return: Teks hasil ekstraksi
    """
    full_text = []

    with fitz.open(file_path) as doc:
        for page in doc:
            text = page.get_text()
            if text:
                full_text.append(text.strip())

    return "\n".join(full_text)

def clean_text(text):
    text = text.strip().replace("\n", " ").replace("\r", "").replace("Â", "").replace("ï¼", "")  # Remove unwanted characters
    text = re.sub(r'\s+', ' ', text)  
    return text

def extract_resume_info(text):
    name = None
    email = None
    phone = None
    
    name_match = re.match(r'^[A-Za-z]+\s[A-Za-z]+\s[A-Za-z]+', text)
    if name_match:
        name = name_match.group(0)
    
    
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    if email_match:
        email = email_match.group(0)
    
    
    phone_match = re.search(r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', text)
    if phone_match:
        phone = phone_match.group(0)

    return name, email, phone

def extract_detailed_info(text):
    #name_pattern = re.findall(r'([A-Z][a-z]+(?: [A-Z][a-z]+)+)', text)
    #name_pattern = re.findall(r'(Name)(.*?)', text)
    #name = name_pattern[0] if name_pattern else 'Unknown'
    name = ''
    # Summary
    summary_matches = list(re.finditer(r'(Summary|Objective)(.*?)(Certifications|Skills|Experience|$)', text, flags=re.DOTALL))
    if summary_matches:
        summary = "\n".join([m.group(2).strip() for m in summary_matches if m.group(2).strip()])
    else:
        summary = 'No summary available'


    # Skills & Highlight
    skills_matches = list(re.finditer(r'(Skills|Highlight)(.*?)(Experience|Education|Projects|Skills|$)', text, flags=re.DOTALL))
    if skills_matches:
        skills = "\n".join([m.group(2).strip() for m in skills_matches if m.group(2).strip()])
    else:
        skills = 'No skills available'

    # Experience
    experience_matches = list(re.finditer(r'(Experience|Work History)(.*?)(Education|Skills|$)', text, flags=re.DOTALL))
    if experience_matches:
        experience = "\n".join([m.group(2).strip() for m in experience_matches if m.group(2).strip()])
    else:
        experience = 'No experience listed'

    # Education
    education_matches = list(re.finditer(r'(Education|Academic Background)(.*?)(Skills|Experience|$)', text, flags=re.DOTALL))
    if education_matches:
        education = "\n".join([m.group(2).strip() for m in education_matches if m.group(2).strip()])
    else:
        education = 'No education listed'

    return SummaryData(
        nama=None, # ini seeding ????
        email=None,  # ini seeding ????
        phone=None,  # ini seeding ????
        address=None,  # ini seeding ????
        skills=[s.strip() for s in skills.split('\n') if s.strip()], # ini ekstrak
        experience=[e.strip() for e in experience.split('\n') if e.strip()], # ini ekstrak
        education=[e.strip() for e in education.split('\n') if e.strip()], # ini ekstrak
        summary=summary
    )

def extract_summary_data_from_pdf(file_path: str) -> SummaryData:
    """
    Mengekstrak data dari file PDF dan mengembalikannya dalam bentuk SummaryData.
    :param file_path: Path ke file PDF
    :return: SummaryData
    """
    extracted_text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(extracted_text)
    summary_data = extract_detailed_info(cleaned_text)
    return summary_data


# ==================================== PDF TO MYSQL ====================================
# def get_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="tubes3stima_db"
#     )

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    temp_conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    temp_cursor = temp_conn.cursor()
    temp_cursor.execute("CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    temp_conn.commit()
    temp_cursor.close()
    temp_conn.close()

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

def reset_tables():
    """
    Menghapus semua data dari tabel ApplicantProfile dan ApplicationDetail.
    Perlu diurutkan karena ApplicationDetail bergantung pada ApplicantProfile (FK).
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Hapus data anak (ApplicationDetail) dulu karena FK
    cursor.execute("DELETE FROM ApplicationDetail")
    cursor.execute("DELETE FROM ApplicantProfile")

    cursor.execute("ALTER TABLE ApplicationDetail AUTO_INCREMENT = 1")
    cursor.execute("ALTER TABLE ApplicantProfile AUTO_INCREMENT = 1")

    conn.commit()
    cursor.close()
    conn.close()
    print("Semua data dalam tabel telah dihapus.")


def create_tables_if_not_exist():
    """
    Membuat tabel ApplicantProfile dan ApplicationDetail jika belum ada di database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ApplicantProfile (
            applicant_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) DEFAULT NULL,
            last_name VARCHAR(50) DEFAULT NULL,
            date_of_birth DATE DEFAULT NULL,
            address VARCHAR(255) DEFAULT NULL,
            phone_number VARCHAR(20) DEFAULT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ApplicationDetail (
            detail_id INT AUTO_INCREMENT PRIMARY KEY,
            applicant_id INT NOT NULL,
            application_role VARCHAR(100) DEFAULT NULL,
            cv_path TEXT,
            FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    print("Tabel sudah dipastikan ada di database.")

def insert_folder_pdfs_to_mysql(folder_path: str, application_role: str = None):
    fake = Faker("id_ID")
    conn = get_connection()
    cursor = conn.cursor()

    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            print(f"Memproses file: {filename} ==================================")
            file_path = os.path.join(folder_path, filename)

            # Step 1: Buat profil dummy
            first_name = fake.first_name()
            last_name = fake.last_name()
            address = fake.address().replace('\n', ', ')
            phone_number = '628' + ''.join(random.choices('0123456789', k=10))
            date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=60)

            # Step 2: Insert ke ApplicantProfile
            cursor.execute(
                """
                INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (first_name, last_name, date_of_birth, address, phone_number)
            )
            applicant_id = cursor.lastrowid  # Dapatkan ID hasil insert barusan

            # Step 3: Insert ke ApplicationDetail
            cursor.execute(
                """
                INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path)
                VALUES (%s, %s, %s)
                """,
                (applicant_id, application_role, file_path)
            )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Selesai memasukkan semua file PDF dari {folder_path} ke database.")


def load_search_data_from_sql() -> list:
    """
    Load all applicants and their CV text from SQL, return as list of SearchData.
    """
    from interface import SearchData
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ap.applicant_id, CONCAT(ap.first_name, ' ', ap.last_name), ad.cv_path
        FROM ApplicantProfile ap
        JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
    ''')
    result = []
    for row in cursor.fetchall():
        id, name, cv_path = row
        try:
            text = extract_text_from_pdf(cv_path)
        except Exception:
            text = ''
        result.append(SearchData(id=id, name=name, text=text))
    cursor.close()
    conn.close()
    return result


def get_cv_path_by_id(applicant_id: int) -> str:
    """
    Get CV file path for a given applicant id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ad.cv_path 
        FROM ApplicationDetail ad 
        WHERE ad.applicant_id = %s LIMIT 1
        ''', (applicant_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row[0] if row else None


def get_summary_by_id(applicant_id: int):
    """
    Extract summary info from PDF for a given applicant id.
    """
    cv_path = get_cv_path_by_id(applicant_id)
    if not cv_path:
        return None
    return extract_summary_data_from_pdf(cv_path)

def seed_applicant_profile(n: int = None):
    """
    Seed tabel ApplicantProfile dengan data dummy menggunakan Faker.
    """
    fake = Faker(id_ID=True)  # Menggunakan locale Indonesia
    conn = get_connection()
    cursor = conn.cursor()

    if n is None:
        cursor.execute("SELECT COUNT(*) FROM ApplicantProfile")
        current_count = cursor.fetchone()[0]
        n = current_count  # default fallback ke 10 jika tabel kosong

    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        address = fake.address().replace('\n', ', ')
        phone_number = ''.join(random.choices('0123456789', k=random.randint(8, 15)))
        print("phone number", phone_number)
        # Tanggal lahir random (opsional, jika ingin diisi)
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=60)
        cursor.execute(
            """
            INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (first_name, last_name, date_of_birth, address, phone_number)
        )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Berhasil seeding {n} data ke ApplicantProfile.")



if __name__ == "__main__":
    """
    alur nya, program akan menerima input folder yang berisi cv 
    cv berupa pdf kemudian akan dimasukan ke sql bersama dengan profil dan detail, 
    profil akan diseeding, kemudian dari sql akan disimpan sebagai list of search data 
    dengan id name sesuai sql, text sesuai isi text dari pdf dengan id dan name sesuai, 
    jadi saat algoritma mencari akan berdasar list of search data tersebut. 
    jika view cv akan membuka cv dari applicant yang dipilih (sesuai id), 
    jika view summary akan membuat extract_detailed_info dari pdf yang dipilih (sesuai id applicant)
    """
    # Pastikan tabel sudah ada
    create_tables_if_not_exist()

    reset_tables()  # Hapus semua data sebelumnya
    # Seed data dummy ke ApplicantProfile
    print("\nSeeding ApplicantProfile dengan Faker...")
    # seed_applicant_profile()

    # Masukkan semua PDF di folder data/ ke database
    print("\nMemasukkan semua PDF di folder data/ ke database...")
    insert_folder_pdfs_to_mysql("data/", application_role="Software Engineer")

    # Load data dari SQL ke list of SearchData
    print("\nLoad SearchData dari database:")
    search_data_list = load_search_data_from_sql()
    for sd in search_data_list:
        print(f"ID: {sd.id}, Name: {sd.name}, Text length: {len(sd.text)}")

    # Contoh view CV dan summary untuk applicant id pertama
    if search_data_list:
        first_id = search_data_list[0].id
        print(f"\nPath CV untuk applicant id {first_id}: {get_cv_path_by_id(first_id)}")
        summary = get_summary_by_id(first_id)
        print(f"\nSummary untuk applicant id {first_id}:")
        print(f"Nama: {summary.nama}")
        print(f"Skills: {summary.skills}")
        print(f"Experience: {summary.experience}")
        print(f"Education: {summary.education}")
        print(f"Summary: {summary.summary}")


    # test
    test_text = """
    Summary
    Experienced software engineer...

    Highlight
    - Fast learner
    - Team player

    Experience
    Company A - Developer

    Education
    B.Sc. Computer Science

    Skills
    Python
    Java
    C++

    Projects
    Personal Website

    Skills
    Machine Learning
    Data Analysis
    """
    # print("\n=== TESTCASE MANUAL (tanpa PDF) ===\n")
    # detailed_info = extract_detailed_info(test_text)
    # print(f"Name: {detailed_info.nama.strip()}\n")
    # print(f"Skills: {detailed_info.skills}\n")
    # print(f"Experience: {detailed_info.experience}\n")
    # print(f"Education: {detailed_info.education}\n")
    # print(f"Summary: {detailed_info.summary}\n")

    # PDF
    # path = "data/tes_pdf2.pdf"
    # extracted_text = extract_text_from_pdf(path)
    # extracted_text = clean_text(extracted_text)
    # detailed_info = extract_detailed_info(extracted_text)
    # print("\n=== TESTCASE PDF ===\n")
    # print(f"Name: {detailed_info.nama}\n")
    # print(f"Skills: {detailed_info.skills}\n")
    # print(f"Experience: {detailed_info.experience}\n")
    # print(f"Education: {detailed_info.education}\n")
    # print(f"Summary: {detailed_info.summary}\n")