from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import csv
import time

url = 'https://www.ncbi.nlm.nih.gov/pmc/?term=%22Behav%20Sci%20(Basel)%22%5Bjour%5D'
options = Options()
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

PATH = r"C:\Users\Lenovo\Documents\Deep Learning\Drivers\chromedriver.exe"
chrome_service = ChromeService(executable_path=PATH)
driver = webdriver.Chrome(service=chrome_service, options=options)
driver.maximize_window()

# Buka URL
driver.get(url)

# Inisialisasi daftar untuk menyimpan tautan
links = []
max_pages = 170  # Batas maksimal halaman yang ingin di-scrape
page_count = 0   # Inisialisasi penghitung halaman

try:
    while page_count < max_pages:
        # Tunggu sampai elemen dengan kelas 'rprt' muncul
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rprt")))

        # Ambil halaman sumber dan parsing dengan BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all(class_='rprt')
        
        # Ambil semua tautan (href) dari setiap elemen dengan kelas 'rprt'
        for article in articles:
            link = article.find('a', href=True)
            if link:
                full_url = "https://www.ncbi.nlm.nih.gov" + link['href']
                links.append(full_url)
                print(full_url)

        # Perbarui penghitung halaman
        page_count += 1

        # Coba menemukan tombol "Next" di bagian pagination
        try:
            # Temukan tombol 'Next' dan cek apakah dapat diklik
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "next"))
            )
            next_button.click()
            time.sleep(2)  # Beri jeda agar halaman baru termuat

        except:
            print("Halaman terakhir telah dicapai atau tombol 'Next' tidak ditemukan.")
            break

    # Menyimpan hasil ke dalam file CSV
    with open('links_all.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Link'])
        for link in links:
            writer.writerow([link])

finally:
    driver.quit()
