# **HR Magang: Sistem ATS Berbasis CV**

## **Fitur Aplikasi**
- Antarmuka pengguna yangn ditulis dengan PyQT
- Upload file PDF CV
- Mendukung 3 algoritma pencocokan yaitu Knuth-Morris-Pratt, Boyer-Moore, dan Aho-Corasick
- Mendukung pencocokan secara *fuzzy matching* dengan perhitungan Levenshtein Distance
- Penyimpanan data ke dalam database MySQL
- Enkripsi data pribadi *applicant* menggunakan *Substitution-Permutation Network* dan *Elliptic Curve Cryptography*

Sistem ini merupakan implementasi dari tiga algoritma pencocokan pola klasik untuk memproses dan menganalisis teks secara efisien. Proyek ini dikembangkan untuk memenuhi tugas dalam ranah _Human Resources_ (HR) yang melibatkan penyaringan dan analisis data tekstual.
Demo aplikasi: [Youtube](https://youtu.be/KJO5aRVa1f8?si=_zvF52Mz_caCNj3_)

## **Penjelasan Singkat Algoritma**

Proyek ini mengimplementasikan tiga algoritma pencocokan pola yang berbeda, masing-masing dengan kekuatan dan karakteristik uniknya.

### **Knuth-Morris-Pratt (KMP)**
KMP memanfaatkan informasi dari karakter yang sudah cocok sebelumnya untuk melakukan pergeseran yang lebih cerdas dan lebih jauh.

### **Boyer-Moore (BM)**
Boyer-Moore memiliki pendekatan yang unik, yaitu melakukan proses pencocokan karakter dari kanan ke kiri pada pola, bukan dari kiri ke kanan seperti kebanyakan algoritma lainnya. Pendekatan ini memungkinkan Boyer-Moore untuk melompati sebagian besar teks dalam sekali pergeseran jika ditemukan mismatch.

### **Aho-Corasick**
Algoritma Aho-Corasick adalah algoritma string matching yang dirancang untuk mencari semua kemunculan dari sekumpulan pola sekaligus secara bersamaan di dalam sebuah teks.

---

## **🚀 Kebutuhan & Instalasi Program**

Untuk menjalankan program ini, pastikan lingkungan Anda telah memenuhi persyaratan berikut dan ikuti langkah-langkah instalasi di bawah ini.

### **Prasyarat**
- **Python 3.x** terinstal di sistem Anda.
- **MariaDB** atau sistem database lain yang kompatibel dengan **MySQL** (contoh: XAMPP, Laragon, atau instalasi mandiri).

### **Langkah-langkah Instalasi**

1.  **Buat dan Aktifkan Lingkungan Virtual (Virtual Environment):**
    * Buka terminal atau command prompt di direktori root proyek.
    * Jalankan perintah berikut untuk membuat lingkungan virtual bernama `venv`:
        ```bash
        python -m venv venv
        ```
    * Aktifkan lingkungan tersebut:
        * **Windows:**
            ```bash
            .\venv\Scripts\activate
            ```
        * **macOS/Linux:**
            ```bash
            source venv/bin/activate
            ```

2.  **Instal Dependensi:**
    * Pastikan `venv` Anda aktif, lalu instal semua pustaka yang dibutuhkan dari file `requirements.txt`:
        ```bash
        pip install -r requirements.txt
        ```

3.  **Konfigurasi Database:**
    * Buat sebuah file bernama `.env` di direktori root proyek.
    * Isi file tersebut dengan detail koneksi database Anda seperti contoh di bawah. Sesuaikan nilainya sesuai dengan konfigurasi lokal Anda.

    ```env
    # Contoh isi file .env
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=
    DB_NAME=hr_magang_db
    ```

4.  **Jalankan Program:**
    * Setelah semua langkah di atas selesai, jalankan aplikasi utama:
        ```bash
        python .\src\main.py
        ```

---

## **👥 Author**

Proyek ini dengan bangga dikembangkan oleh:

-   **Muhammad Alfansya** - `13523005`
-   **M. Rayhan Farrukh** - `13523035`
-   **Nadhif Al Rozin** - `13523076`
