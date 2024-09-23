import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

# Tetapan Selenium Chrome Driver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Lokasi fail cookie
COOKIES_FILE = 'cookies.json'

# Muatkan cookie dari fail
def load_cookies():
    try:
        with open(COOKIES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Fail cookies.json tidak dijumpai!")
        return []

# Simpan cookies dalam browser session
def set_cookies(driver, cookies):
    for cookie in cookies:
        driver.add_cookie({
            'name': cookie['name'],
            'value': cookie['value'],
            'domain': cookie['domain']
        })

# Pilih akaun dan aksi
def pilih_aksi():
    print("Pilih aksi:")
    print("[01] LIKE")
    print("[02] VIEW")
    print("[03] FOLLOWER")
    pilihan = input("Masukkan nombor aksi: ")
    if pilihan == '01':
        return 'like'
    elif pilihan == '02':
        return 'view'
    elif pilihan == '03':
        return 'follower'
    else:
        print("Pilihan tidak sah!")
        return pilih_aksi()

# Mulakan proses mengikut akaun dan pilihan aksi
def proses_akaun(cookie_data, link, jumlah, aksi):
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get('https://www.tiktok.com')
    sleep(2)
    
    # Set cookies
    set_cookies(driver, cookie_data)
    sleep(2)
    
    # Mula login semula dengan cookies
    driver.refresh()
    sleep(3)
    
    if aksi == 'like':
        like_video(driver, link, jumlah)
    elif aksi == 'view':
        view_video(driver, link, jumlah)
    elif aksi == 'follower':
        follow_user(driver, link, jumlah)
    
    driver.quit()

# Aksi Like Video
def like_video(driver, link, jumlah):
    driver.get(link)
    for i in range(jumlah):
        try:
            like_button = driver.find_element(By.XPATH, '//button[contains(@class,"like")]')
            like_button.click()
            print(f"Like {i+1} berjaya!")
            sleep(2)
        except Exception as e:
            print(f"Error semasa like: {e}")

# Aksi View Video
def view_video(driver, link, jumlah):
    for i in range(jumlah):
        driver.get(link)
        print(f"Tonton video untuk view {i+1}")
        sleep(5)

# Aksi Follow User
def follow_user(driver, link, jumlah):
    driver.get(link)
    for i in range(jumlah):
        try:
            follow_button = driver.find_element(By.XPATH, '//button[contains(@class,"follow")]')
            follow_button.click()
            print(f"Follow {i+1} berjaya!")
            sleep(2)
        except Exception as e:
            print(f"Error semasa follow: {e}")

# Main Function
def main():
    cookies_list = load_cookies()
    
    if not cookies_list:
        print("Tiada cookies untuk akaun.")
        return

    print(f"Terdapat {len(cookies_list)} akaun tersedia.")
    
    # Paparkan pilihan untuk LIKE, VIEW, FOLLOWER
    aksi = pilih_aksi()
    
    # Minta URL dari pengguna
    link = input("Masukkan link TikTok: ")
    
    # Minta jumlah
    jumlah = int(input(f"Berapa banyak {aksi} yang anda ingin buat? "))

    # Mulakan proses untuk setiap akaun dalam cookies.json
    for i, cookie_data in enumerate(cookies_list):
        print(f"\nMemproses akaun {i+1}/{len(cookies_list)}")
        proses_akaun(cookie_data, link, jumlah, aksi)

if __name__ == '__main__':
    main()
               
