from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pytz
import time
import random
import sys

# ===============================
# KONFIGURASI TIMEZONE (WIB)
# ===============================
WIB = pytz.timezone("Asia/Jakarta")
now = datetime.now(WIB)

print("===================================")
print(" SHOPEE CHAT MACRO - WIB (CLI)")
print("===================================\n")

# ===============================
# INPUT COOKIE VIA TERMINAL
# ===============================
spc_u = input("Masukkan cookie SPC_U      : ").strip()
spc_ec = input("Masukkan cookie SPC_EC     : ").strip()
spc_t_id = input("Masukkan cookie SPC_T_ID  : ").strip()
spc_t_iv = input("Masukkan cookie SPC_T_IV  : ").strip()

# ===============================
# INPUT WAKTU EKSEKUSI (WIB)
# ===============================
print("\n-- WAKTU MASUK CHAT (WIB) --")
jam = int(input("Jam   (0-23): "))
menit = int(input("Menit (0-59): "))
detik = int(input("Detik (0-59): "))

pesan = input("\nPesan auto-reply: ")

# ===============================
# HITUNG WAKTU TUNGGU
# ===============================
target = WIB.localize(datetime(
    now.year, now.month, now.day, jam, menit, detik
))

if target <= now:
    print("\n❌ Waktu sudah lewat (WIB)")
    sys.exit()

wait_sec = int((target - now).total_seconds())
print(f"\n⏳ Menunggu {wait_sec} detik sampai waktu target (WIB)...")
time.sleep(wait_sec)

# ===============================
# SETUP SELENIUM (CHROME)
# ===============================
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--no-sandbox")              # aktifkan jika Linux/VPS
# options.add_argument("--disable-dev-shm-usage")  # aktifkan jika Linux/VPS

driver = webdriver.Chrome(options=options)

# ===============================
# BUKA SHOPEE & INJECT COOKIE
# ===============================
print("➡ Membuka Shopee & inject cookie...")
driver.get("https://shopee.co.id")
time.sleep(5)

cookies = [
    {"name": "SPC_U", "value": spc_u, "domain": ".shopee.co.id", "path": "/"},
    {"name": "SPC_EC", "value": spc_ec, "domain": ".shopee.co.id", "path": "/"},
    {"name": "SPC_T_ID", "value": spc_t_id, "domain": ".shopee.co.id", "path": "/"},
    {"name": "SPC_T_IV", "value": spc_t_iv, "domain": ".shopee.co.id", "path": "/"},
]

for c in cookies:
    driver.add_cookie(c)

driver.refresh()
time.sleep(8)

# ===============================
# MASUK CHAT SELLER
# ===============================
print("➡ Masuk halaman chat seller...")
driver.get("https://seller.shopee.co.id/portal/chat")
time.sleep(12)

# ===============================
# KLIK CHAT TERATAS
# ===============================
print("➡ Klik chat teratas...")
chat = driver.find_element(
    By.XPATH,
    "(//div[contains(@class,'chat') or contains(@class,'conversation')])[1]"
)
chat.click()

time.sleep(random.randint(6, 15))

# ===============================
# KIRIM PESAN
# ===============================
print("➡ Mengirim pesan...")
input_box = driver.find_element(By.XPATH, "//textarea")
input_box.send_keys(pesan)
time.sleep(random.randint(2, 4))
input_box.send_keys("\n")

print("\n✅ Pesan berhasil dikirim (WIB)")

# ===============================
# SELESAI
# ===============================
time.sleep(10)
driver.quit()
print("✔ Script selesai & browser ditutup")