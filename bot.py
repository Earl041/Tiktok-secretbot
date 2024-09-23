import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

# Tetapan Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')  # Tidak tunjukkan pelayar
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Fungsi untuk memuatkan cookies
def load_cookies(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Fail cookies tidak dijumpai.")
        return []

# Fungsi untuk login ke TikTok menggunakan cookies
def login_with_cookies(driver, cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)

# Fungsi untuk melakukan tindakan 'like'
def like_video(driver, link, count):
    driver.get(link)
    sleep(5)  # Tunggu laman memuat
    for _ in range(count):
        try:
            like_button = driver.find_element(By.XPATH, '//*[@data-e2e="like-button"]')
            like_button.click()
            print("Video telah dilike.")
            sleep(2)  # Tunggu sedikit sebelum like seterusnya
        except Exception as e:
            print(f"Gagal untuk like video: {e}")

# Fungsi untuk melakukan tindakan 'view'
def view_video(driver, link, count):
    driver.get(link)
    for _ in range(count):
        sleep(5)  # Lihat video selama 5 saat
        print("Video telah dilihat.")

# Fungsi untuk melakukan tindakan 'follow'
def follow_user(driver, link, count):
    driver.get(link)
    sleep(5)  # Tunggu laman memuat
    for _ in range(count):
        try:
            follow_button = driver.find_element(By.XPATH, '//*[@data-e2e="follow-button"]')
            follow_button.click()
            print("Pengguna telah diikuti.")
            sleep(2)  # Tunggu sedikit sebelum follow seterusnya
        except Exception as e:
            print(f"Gagal untuk follow pengguna: {e}")

# Fungsi utama
def main():
    # Fail untuk menyimpan cookies
    cookies_file = 'cookies.json'
    
    # Muatkan cookies dari fail
    cookies = load_cookies(cookies_file)
    
    if not cookies:
        return  # Jika tiada cookies, hentikan skrip

    # Inisialisasi webdriver
    driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'), options=chrome_options)
    
    # Pergi ke laman TikTok
    driver.get('https://www.tiktok.com')
    sleep(5)  # Tunggu laman memuat

    # Login dengan cookies
    login_with_cookies(driver, cookies)

    # Selepas login, ambil tindakan berdasarkan input pengguna
    action = input("Pilih tindakan: [LIKE, VIEW, FOLLOWER]: ").strip().upper()

    if action == 'LIKE':
        link = input("Masukkan link video: ")
        count = int(input("Masukkan jumlah like: "))
        like_video(driver, link, count)
    
    elif action == 'VIEW':
        link = input("Masukkan link video: ")
        count = int(input("Masukkan jumlah view: "))
        view_video(driver, link, count)

    elif action == 'FOLLOWER':
        link = input("Masukkan link profil: ")
        count = int(input("Masukkan jumlah follower: "))
        follow_user(driver, link, count)

    driver.quit()  # Tutup pelayar

if __name__ == '__main__':
    main()
    
