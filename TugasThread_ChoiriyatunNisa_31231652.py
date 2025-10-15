import threading
import time

# ======================================================
# Program: Simulasi Penarikan Uang Bersama (Multithreading)
# Nama: Nisa Latansa
# NIM: 31231652
# Deskripsi:
#   Program ini mensimulasikan dua orang (Andi dan Budi)
#   menarik uang dari rekening bersama menggunakan dua thread.
#   Tujuannya menunjukkan perbedaan hasil dengan dan tanpa lock.
# ======================================================

# Fungsi utama untuk menarik uang
def tarik_uang(nama, jumlah, saldo_data, gunakan_lock, lock=None):
    print(f"{nama} mencoba menarik uang sebesar {jumlah}")

    # Jika pakai lock, maka kunci akses saldo agar tidak terjadi konflik data
    if gunakan_lock:
        with lock:  # hanya satu thread yang bisa masuk ke bagian ini
            proses_tarik(nama, jumlah, saldo_data)
    else:
        # Tanpa lock, dua thread bisa mengakses saldo bersamaan
        proses_tarik(nama, jumlah, saldo_data)

# Fungsi yang benar-benar mengurangi saldo
def proses_tarik(nama, jumlah, saldo_data):
    # Komentar 1: Fungsi ini menampilkan dan mengurangi saldo
    print(f"{nama} sedang mengakses saldo...")
    time.sleep(1)  # Komentar 2: Simulasi waktu proses transaksi
    if saldo_data["saldo"] >= jumlah:
        saldo_data["saldo"] -= jumlah  # Komentar 3: Saldo dikurangi jika cukup
        print(f"{nama} berhasil menarik {jumlah}")
    else:
        print(f"{nama} gagal menarik. Saldo tidak cukup!")  # Komentar 4: Jika saldo tidak mencukupi
    print(f"Saldo tersisa: {saldo_data['saldo']}\n")  # Komentar 5: Tampilkan saldo terkini

# ====================================================
# SIMULASI 1: TANPA LOCK (potensi race condition)
# ====================================================
print("\n=== SIMULASI 1: TANPA LOCK ===")
saldo_data = {"saldo": 100}  # saldo awal 100, disimpan dalam dict agar bisa diubah oleh thread

t1 = threading.Thread(target=tarik_uang, args=("Andi", 80, saldo_data, False))
t2 = threading.Thread(target=tarik_uang, args=("Budi", 80, saldo_data, False))

# Jalankan kedua thread bersamaan
t1.start()
t2.start()

# Tunggu kedua thread selesai
t1.join()
t2.join()

print(f"Saldo akhir tanpa lock: {saldo_data['saldo']}\n")

# ====================================================
# SIMULASI 2: DENGAN LOCK (aman dan konsisten)
# ====================================================
print("=== SIMULASI 2: DENGAN LOCK ===")
saldo_data = {"saldo": 100}  # reset saldo awal
lock = threading.Lock()  # membuat objek lock

t3 = threading.Thread(target=tarik_uang, args=("Andi", 80, saldo_data, True, lock))
t4 = threading.Thread(target=tarik_uang, args=("Budi", 80, saldo_data, True, lock))

t3.start()
t4.start()

t3.join()
t4.join()

print(f"Saldo akhir dengan lock: {saldo_data['saldo']}\n")

# ====================================================
# PENJELASAN HASIL SIMULASI
# ====================================================
print("=== PENJELASAN ===")
print("- Tanpa lock → Kedua thread bisa mengakses saldo bersamaan, "
      "sehingga hasil bisa kacau atau negatif (race condition).")
print("- Dengan lock → Akses saldo dikunci untuk satu thread saja. "
      "Hasil aman, saldo tidak akan minus, dan lebih konsisten.")
