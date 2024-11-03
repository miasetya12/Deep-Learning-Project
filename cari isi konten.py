from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import csv
import json
import time
import re

# Path ke driver Chrome Anda
PATH = r"C:\Users\Lenovo\Documents\Deep Learning\Drivers\chromedriver.exe"

# Inisialisasi Selenium WebDriver dengan opsi
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Menjalankan tanpa membuka browser (opsional)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

chrome_service = ChromeService(executable_path=PATH)
driver = webdriver.Chrome(service=chrome_service, options=options)

# List untuk menyimpan semua hasil scraping
data_list = []

# Baca URL dan Title dari CSV dan lakukan scraping pada tiap URL
with open('test_data.csv', mode='r', encoding='utf-8') as file:  # Tambahkan encoding='utf-8' di sini
    reader = csv.DictReader(file)

    for row in reader:
        url = row['Link']  # Asumsi kolom bernama 'Link' di CSV
        title = row['Title']  # Asumsi kolom bernama 'Title' di CSV
        
        driver.get(url)

        # Tunggu sampai elemen utama halaman dimuat
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "section.body.main-article-body"))
            )
            # Parse HTML dengan BeautifulSoup setelah halaman dimuat
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Mengambil konten dari abstract
            abstract = soup.select_one("section.abstract").get_text(strip=True) if soup.select_one("section.abstract") else "Tidak ditemukan"
            
            # Mengambil semua konten dari section yang diawali dengan "sec" tanpa sub-sections (tidak mengandung "dot")
            sections = []
            section_ids = []  # List untuk menyimpan ID dari setiap sec utama
            for sec in soup.select("section[id^='sec']"):
                if re.match(r'^sec\d+-', sec['id']):  # Hanya ambil ID yang sesuai dengan pola "sec" diikuti angka (tidak mengandung "dot")
                    sections.append(sec.get_text(strip=True))
                    section_ids.append(sec['id'])  # Menyimpan ID dari section utama
                
            # Gabungkan isi sections dengan spasi antar bagian
            combined_sections = " ".join(sections) if sections else "Tidak ditemukan"
            section_count = len(sections)
            
            # Print jumlah sections utama dan ID dari setiap section utama
            print(f"Jumlah 'sec' utama yang ditemukan di URL {url}: {section_count}")
            print(f"ID 'sec' utama yang ditemukan: {', '.join(section_ids)}")
            
            # Menyimpan hasil scraping ke list sebagai dictionary
            data_list.append({
                "Link": url,
                "Title": title,
                "Abstract": abstract,
                "Sections": combined_sections
            })
            
            # Print pesan berhasil
            print(f"Berhasil mengambil data dari URL: {url}")

        except Exception as e:
            print(f"Gagal mengambil data dari {url}: {e}")
            data_list.append({
                "Link": url,
                "Title": title,
                "Abstract": "Gagal mengambil data",
                "Sections": ""
            })

        time.sleep(2)  # Delay untuk menghindari deteksi bot

# Simpan data_list ke file JSON
with open('output_7.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(data_list, jsonfile, ensure_ascii=False, indent=4)

# Tutup WebDriver
driver.quit()