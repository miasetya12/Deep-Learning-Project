from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import json
import time
import re
import csv

# Path ke driver Chrome Anda
PATH = r"C:\Users\Lenovo\Documents\Deep-Learning-Project\Drivers\chromedriver.exe"

# Inisialisasi Selenium WebDriver dengan opsi
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Menjalankan tanpa membuka browser (opsional)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

chrome_service = ChromeService(executable_path=PATH)
driver = webdriver.Chrome(service=chrome_service, options=options)

# Baca URL dan Title dari CSV dan lakukan scraping pada tiap URL
with open('test data.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    # Buat list untuk menyimpan hasil scraping
    results = []

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
            
            # Mengambil dan menggabungkan konten dari h2 dan p di dalam abstract
            abstract_h2 = soup.select_one("section.abstract h2").get_text(strip=True) if soup.select_one("section.abstract h2") else ""
            abstract_p = soup.select_one("section.abstract p").get_text(strip=True) if soup.select_one("section.abstract p") else ""
            combined_abstract = f"{abstract_h2} {abstract_p}".strip() if abstract_h2 or abstract_p else "Tidak ditemukan"
            
            # Mengambil konten dari section.kwd-group di dalam abstract
            keywords_section = soup.select_one("section.kwd-group").get_text(strip=True) if soup.select_one("section.kwd-group") else "Tidak ditemukan"
            
            # Simpan data ke dalam dictionary
            result = {
                'Link': url,
                'Title': title,
                'Abstract': combined_abstract,
                'Keywords': keywords_section
            }
            results.append(result)  # Tambahkan hasil ke list results
            
            # Print pesan berhasil
            print(f"Berhasil mengambil data dari URL: {url}")

        except Exception as e:
            print(f"Gagal mengambil data dari {url}: {e}")
            results.append({
                'Link': url,
                'Title': title,
                'Abstract': "Gagal mengambil data",
                'Keywords': "Gagal mengambil data"
            })

        time.sleep(2)  # Delay untuk menghindari deteksi bot

# Simpan hasil ke file JSON
with open('output_8.json', mode='w', encoding='utf-8') as jsonfile:
    json.dump(results, jsonfile, ensure_ascii=False, indent=4)

# Tutup WebDriver
driver.quit()
