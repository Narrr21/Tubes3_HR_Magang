import random
from typing import List
import fitz 
import re
import os
from faker import Faker
import os

import mysql.connector
import dotenv

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
    try :
        full_text = []

        with fitz.open(file_path) as doc:
            for page in doc:
                text = page.get_text()
                if text:
                    full_text.append(text)

        return "\n".join(full_text)
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""
    # return full_text

def clean_text(text):
    text = text.strip().replace("\r", "").replace("Â", "").replace("ï¼", "")
    return text


def extract_detailed_info(text):
    text = clean_text(text)
    # Summary
    summary_matches = list(re.finditer(r'(Summary|Objective)(.*?)(Certifications|Skills|Experience|$)', text, flags=re.DOTALL))
    if summary_matches:
        summary = "\n".join([m.group(2).strip() for m in summary_matches if m.group(2).strip()])
    else:
        summary = 'No summary available'

    # Skills & Highlight
    skills_matches = list(re.finditer(r'(Skills|Highlight.?)(.*?)(Experience|Education|Projects|Skills|$)', text, flags=re.DOTALL))
    if skills_matches:
        skills = "\n".join([m.group(2).strip() for m in skills_matches if m.group(2).strip()])
    else:
        skills = 'No skills available'

    # Experience
    # experience_matches = list(re.finditer(r'(Experience|Work History)(.*?)(Education|Skills|$)', text, flags=re.DOTALL))
    # if experience_matches:
    #     experience = "\n".join([m.group(2).strip() for m in experience_matches if m.group(2).strip()])
    # else:
    #     experience = 'No experience listed'

    experience_matches = re.search(r'(Experience|Work History)(.*?)(Education|Skills|Projects|$)', text, re.DOTALL)
    exp_text = experience_matches.group(2).strip() if experience_matches else ''
    pattern = re.compile(
            r'(?P<position>.+?)\s*'                                
            r'(?P<start_month>\w+)\s(?P<start_year>\d{4})\s*'         
            r'to\s*'                              
            r'(?P<end_month>\w+|Current)\s(?P<end_year>\d{4}|)\s*'    
            r'(?P<company>.+)?',                
            re.IGNORECASE
        )

    print(f"[DEBUG] Extracting experience from text: {exp_text}")
    exp = []
    for match in pattern.finditer(exp_text):
        position = match.group("position").strip()
        start = f"{match.group('start_month')} {match.group('start_year')}"
        end = match.group("end_month")
        if end != "Current":
            end = f"{end} {match.group('end_year')}"
        company = match.group("company").strip() if match.group("company") else "Unknown"
        exp.append(f"{position} {start} to {end} {company}")
    

    # Education
    education_matches = list(re.finditer(r'(Education|Academic Background)(.*?)(Skills|Experience|Projects|$)', text, flags=re.DOTALL))
    if education_matches:
        education = "\n".join([m.group(2).strip() for m in education_matches if m.group(2).strip()])
    else:
        education = 'No education listed'

    return SummaryData(
        nama=None, # ini seeding ????
        email=None,  # ini seeding ????
        phone=None,  # ini seeding ????
        address=None,  # ini seeding ????
        skills=[s.strip() for s in skills.split('\n') if s.strip()],
        experience=exp,
        education=[e.strip() for e in education.split('\n') if e.strip()],
        summary=summary
    )

def extract_summary_data_from_pdf(file_path: str) -> SummaryData:
    """
    Mengekstrak data dari file PDF dan mengembalikannya dalam bentuk SummaryData.
    :param file_path: Path ke file PDF
    :return: SummaryData
    """
    extracted_text = extract_text_from_pdf(file_path)
    if isinstance(extracted_text, list):
        extracted_text = "\n".join(extracted_text)
    summary_data = extract_detailed_info(extracted_text)
    return summary_data


# ==================================== PDF TO MYSQL ====================================
dotenv.load_dotenv()  # Load environment variables from .env file
DB_HOST = os.getenv("DB_HOST") 
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD") 
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    temp_conn = mysql.connector.connect(
        # host="localhost",
        # user="root",
        # password="",
        host= DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
    )
    temp_cursor = temp_conn.cursor()
    temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    temp_conn.commit()
    temp_cursor.close()
    temp_conn.close()

    return mysql.connector.connect(
        # host="localhost",
        # user="root",
        # password="",
        # database="tubes3stima_db"
        host= DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
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
    # seeding
    fake = Faker("id_ID") 
    conn = get_connection()
    cursor = conn.cursor()

    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            print(f"Memproses file: {filename} ==================================")
            file_path = os.path.join(folder_path, filename)

            first_name = fake.first_name()
            last_name = fake.last_name()
            address = fake.address().replace('\n', ', ')
            phone_number = '628' + ''.join(random.choices('0123456789', k=10))
            date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=60)
            email = f"{last_name.lower()}.{first_name}@StimeHehe.com"
            cursor.execute(
                """
                INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (first_name, last_name, date_of_birth, address, phone_number)
            )
            applicant_id = cursor.lastrowid  # Dapatkan ID hasil insert barusan

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
        app_id, name, cv_path = row
        try:
            text = extract_text_from_pdf(cv_path)
        except Exception:
            text = ''
        result.append(SearchData(id=app_id, name=name, text=text))
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
    data = extract_summary_data_from_pdf(cv_path)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM ApplicantProfile WHERE applicant_id = %s', (applicant_id,))
    row = cursor.fetchone()
    data.email = row[0] if row else None

    cursor.execute('SELECT phone_number FROM ApplicantProfile WHERE applicant_id = %s', (applicant_id,))
    row = cursor.fetchone()
    data.phone = row[0] if row else None

    cursor.execute('SELECT address FROM ApplicantProfile WHERE applicant_id = %s', (applicant_id,))
    row = cursor.fetchone()
    data.address = row[0] if row else None

    cursor.close()
    conn.close()

    return data.nama, data.email, data.phone, data.address, data.skills, data.experience, data.education, data.summary

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
        email = f"{last_name}{first_name}{random.randint(1,999)}@stimehehe.com"

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
    # # Pastikan tabel sudah ada
    # create_tables_if_not_exist()

    # reset_tables()  # Hapus semua data sebelumnya
    # # Seed data dummy ke ApplicantProfile
    # print("\nSeeding ApplicantProfile dengan Faker...")
    # # seed_applicant_profile()

    # # Masukkan semua PDF di folder data/ ke database
    # print("\nMemasukkan semua PDF di folder data/ ke database...")
    # insert_folder_pdfs_to_mysql("data/", application_role="Software Engineer")

    # # Load data dari SQL ke list of SearchData
    # print("\nLoad SearchData dari database:")
    # search_data_list = load_search_data_from_sql()
    # for sd in search_data_list:
    #     print(f"ID: {sd.id}, Name: {sd.name}, Text length: {len(sd.text)}")

    # # Contoh view CV dan summary untuk applicant id pertama
    # if search_data_list:
    #     first_id = search_data_list[0].id
    #     print(f"\nPath CV untuk applicant id {first_id}: {get_cv_path_by_id(first_id)}")
    #     summary = get_summary_by_id(first_id)
    #     print(f"\nSummary untuk applicant id {first_id}:")
    #     print(f"Nama: {summary.nama}")
    #     print(f"Skills: {summary.skills}")
    #     print(f"Experience: {summary.experience}")
    #     print(f"Education: {summary.education}")
    #     print(f"Summary: {summary.summary}")


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
    def extract_experience_entries(text: str):
    # Regex pattern yang lebih fleksibel
        pattern = re.compile(
            r'(?P<position>.+?)\s*\n'                                # Baris 1: Posisi/Jabatan
            r'(?P<start_month>\w+)\s(?P<start_year>\d{4})\s*'         # Baris 2: Tanggal mulai
            r'to\s*'                                                 # Kata penghubung 'to'
            r'(?P<end_month>\w+|Current)\s(?P<end_year>\d{4}|)\s*'    # Tanggal akhir (bisa Current)
            r'(?P<company>.+)?',                
            # r'(?P<position>.+?)\s*(?P<start_month>\w+)\s(?P<start_year>\d{4})\s*to\s*(?P<end_month>\w+|Current)\s(?P<end_year>\d{4}|)\s*(?P<company>.+)?'                       # Nama perusahaan (bisa di akhir baris)
            re.IGNORECASE
        )

        results = []
        for match in pattern.finditer(text):
            position = match.group("position").strip()
            start = f"{match.group('start_month')} {match.group('start_year')}"
            end = match.group("end_month")
            if end != "Current":
                end = f"{end} {match.group('end_year')}"
            company = match.group("company").strip() if match.group("company") else "Unknown"
            results.append(f"{position} {start} to {end} {company}")

        return results

    # text = extract_summary_data_from_pdf("data/tes_pdf.pdf")
    text = extract_text_from_pdf("data/tes_pdf2.pdf")
    exp = extract_experience_entries(text)
    for e in exp:
        print(e)
    # print(f"Nama: {text.nama} \n")
    # print(f"Email: {text.email} \n")
    # print(f"Phone: {text.phone} \n")
    # print(f"Address: {text.address} \n")
    # print(f"Skills: {text.skills} \n")
    # print(f"Experience: {text.experience} \n")
    # print(f"Education: {text.education} \n")
    # print(f"Summary: {text.summary} \n")

    # bla = extract_text_from_pdf("data/tes_pdf.pdf")
    # print("\n\n", bla)