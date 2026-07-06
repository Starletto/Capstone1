import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, insert, MetaData, Table, text

def buat_koneksi():
    #Membuat koneksi sql dari main ke database sql
    try:
        engine = create_engine('mysql+mysqlconnector://root:romeoisugly01@localhost/purwadhika')
        print("Koneksi ke database berhasil")
        return engine
    except Exception as e:
        print(f"Terjadi error: {e}")
        return None

def login():
    print("""
=======================================
    SELAMAT DATANG DI APLIKASI LOGIN
=======================================
Masuk sebagai:
1. Admin
2. Pembeli
3. Keluar
          """)
    #Membuat variabel pilihan untuk diinput user
    pilihan = input("Pilih role: ")

    #Logika if untuk pilihan user
    if pilihan == '1':
        #Memasukkan password admin
        password = input("Masukkan password admin: ")
        if password == '12345':
            print("Selamat datang Admin!")
            return 'admin'
        else:
            print("[!] Password salah. [!]")
            return None
        
    elif pilihan == '2':
        print("Selamat datang pembeli, selamat berbelanja!")
        return 'pembeli'
    
    elif pilihan == '3':
        print("Terimakasih telah menggunakan aplikasi ini.")
        return 'exit'

    else:
        print("Pilihan tidak valid.")
        return None

def read_data():
    try:
    #Menampilkan pilihan tabel yang ada di MySQL
        print("""
=======================================
            DAFTAR TABEL
=======================================
1. Tabel Stok
2. Tabel Transaksi
3. Tabel Voucher
4. Keluar
              """)
        
        #Memasukkan input user
        pilihan = int(input("Masukkan pilihan anda: "))

        #Logika if untuk menampilkan tabel yang dipilih user
        if pilihan == 1:
            df = pd.read_sql("SELECT * FROM capstone1", engine)
        elif pilihan == 2:
            df = pd.read_sql("SELECT * FROM transaksi", engine)
        elif pilihan == 3:
            df = pd.read_sql("SELECT * FROM voucher", engine)
        elif pilihan == 4:
            print("Kembali ke Menu Utama")
            return

        #Logika if jika tabel kosong
        if df.empty:
            print("Data produk kosong")
        else:
            print(df)
    except Exception as e:
        print(f"Terjadi error {e}")
        return None
    
def show_statistik():

    #Membuat looping
    while True:
        print("""
=======================================
        STATISTIK PENJUALAN
=======================================
Pilihan kolom :
1. Harga
2. Stok
3. Jumlah pembelian
4. Revenue
5. Keluar
        """)
            #Memasukkan input user
        pilihan = int(input("Masukkan pilihan anda: "))
        if pilihan == 5:
            print("Kembali ke Menu Utama.")
            break
        
        try:

            #Membuat logika if untuk dari pilihan user
            if pilihan == 1:
                df = pd.read_sql("SELECT harga FROM capstone1", engine)
                nama_kolom = 'harga'
            elif pilihan == 2:
                df = pd.read_sql("SELECT stok_sisa FROM capstone1", engine)
                nama_kolom = 'stok_sisa'
            elif pilihan == 3:
                df = pd.read_sql("SELECT jumlah_beli FROM transaksi", engine)
                nama_kolom = 'jumlah_beli'
            elif pilihan == 4:
                df = pd.read_sql("SELECT total_akhir FROM transaksi", engine)
                nama_kolom = 'total_akhir'
            else:
                print("Pilihan tidak valid, masukkan angka kembali!")
                continue

            #Kode untuk menampilkan mean
            rata_rata = df[nama_kolom].mean()
            print(f"Rata-rata dari tabel {nama_kolom} adalah {rata_rata}")

        except Exception as e:
            print(f"Terjadi error: {e}")
            break

def data_visualization():
    #Membuat looping
    while True:
        print("""
=======================================
          VISUALISASI DATA
=======================================
Pilihan Tabel:
1. Tabel Stok
2. Tabel Transaksi
3. Keluar
            """)
        try:
            pilih = int(input("Masukkan pilihan anda: "))

            if pilih == 1:
                df = pd.read_sql("SELECT * FROM capstone1", engine)
            elif pilih == 2:
                df = pd.read_sql("SELECT * FROM transaksi", engine)
            elif pilih == 3:
                print("Kembali ke Menu Utama")
                break
            else:
                break
            
            #Menampilkan pilihan dari MySQl
            print("""
=======================================
            KOLOM TERSEDIA
=======================================
            """)
            for i, kolom in enumerate(df.columns[1:], 1):
                print(f"{i}. {kolom}")

            pilihan = int(input("Pilih kolom untuk visualisasi: "))

            try:
                kolom_terpilih = df.columns[1:][int(pilihan)-1]
                
                plt.figure(figsize=(10, 6))
                
                #Jika kolom bertipe object maka piechart akan diinisiasi
                if df[kolom_terpilih].dtype == 'object':
                    print(f"\nDistribusi Kategori pada Kolom '{kolom_terpilih}'")
                    counts = df[kolom_terpilih].value_counts()
                    plt.pie(counts, labels=counts.index)
                    plt.title(f'Distribusi {kolom_terpilih}')
                
                #Jika kolom bertipe numerik maka histogram akan diinisiasi
                else:
                    print(f"\nDistribusi Nilai pada Kolom '{kolom_terpilih}'")
                    sns.histplot(df[kolom_terpilih], kde=True)
                    plt.title(f'Distribusi {kolom_terpilih}')
                    
                plt.tight_layout()
                plt.show()
                
            except (IndexError, ValueError):
                print("Pilihan tidak valid!")
                
        except Exception as e:
            print(f"Terjadi error: '{e}'")

def add_data():
    try:
        print("""
=======================================
            DATABASE
=======================================
1. Tambah Data Produk
2. Tambah Voucher
3. Keluar
            """)
        pilihan = int(input("Masukkan pilihan anda: "))
        if pilihan == 1:
                #menambahkan data baru ke tabel produk
                print("TAMBAH DATA PRODUK")
                nama = input("Masukkan nama produk: ")
                kategori = input("Masukkan kategori produk")
                harga = float(input("Masukkan harga produk: "))
                stok = int(input("Masukkan stok produk: "))

                metadata = MetaData()
                tabel_produk = Table('capstone1', metadata, autoload_with=engine)

                #Membuat variabel agar data lebih mudah dimasukkan ke database MySQL
                stmt = insert(tabel_produk).values(
                    nama=nama,
                    kategori=kategori,
                    harga=harga,
                    stok_sisa=stok
                )
        elif pilihan == 2:
                #menambahkan data baru ke tabel voucher
                print("TAMBAH DATA VOUCHER")
                kode_voucher = input("Masukkan kode voucher: ")
                potongan = float(input("Masukkan potongan harga: "))
                kuota = int(input("Masukkan kuota voucher: "))

                metadata = MetaData()
                tabel_voucher = Table('voucher', metadata, autoload_with=engine)

                #Membuat variabel agar data lebih mudah dimasukkan ke database MySQL
                stmt = insert(tabel_voucher).values(
                    kode_voucher=kode_voucher,
                    potongan=potongan,
                    kuota=kuota
                )
        elif pilihan == 3:
            return

        #Menginisiasi agar data dapat mengupdate data di MySQL
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()

        print(f"Data berhasil ditambahkan!")

    except Exception as e:
        print(f"Terjadi error: {e}")
                            
def pembelian():
    print("Pembelian")
    read_data(role='pembeli')

    id_p = int(input('Masukkan ID produk yang ingin dibeli:'))
    qty = int(input('Masukkan jumlah produk yang ingin dibeli:'))

    try:
        #Menghubungkan database dengan program
        with engine.connect() as conn:
            res = conn.execute(text('SELECT * FROM capstone1 WHERE id = :id'), {'id': id_p}).fetchone()
        
        #Logika jika stok barang tidak cukup atau tidak ditemukan
        if not res or res.stok_sisa < qty:
            print("Maaf, stok produk tidak mencukupi atau produk tidak ditemukan.")
            return
        
        #Perhitungan harga awal sebelum diskon
        total_awal = res.harga * qty
        diskon = 0
        kode_v = input("Masukkan kode voucher (Jika tidak ada, tekan Enter):")

        #Membuat variabel yang akan digunakan nanti jika pembeli tidak mempunya voucher
        voucher_valid = False


        if kode_v:
            with engine.connect() as conn:
                v_res = conn.execute(text('SELECT * FROM voucher WHERE kode_voucher = :k AND kuota > 0'), {'k': kode_v}).fetchone()
                if v_res:
                    diskon = v_res.potongan
                    voucher_valid = True
                    conn.execute(text('UPDATE voucher SET kuota = kuota - 1 WHERE kode_voucher = :k'), {'k': kode_v})

                else:
                    print("Kode voucher tidak valid atau kuota habis.")

        total_akhir = max(0, total_awal - diskon)

        #Update Database MySQL
        with engine.begin() as conn:
            #Update stok MySQL
            conn.execute(text("""
                            UPDATE capstone1
                            SET stok_sisa = stok_sisa - :q
                            WHERE id = :id
                            """), {'q': qty, 'id': id_p})
            
            if voucher_valid:
                conn.execute(text(' UPDATE voucher SET kuota = kuota - 1 WHERE kode_voucher = :k'), {'k': kode_v})
            
            #Mencatat Riwayat dan dimasukkan ke tabel di MySQL
            conn.execute(text("""
                              INSERT INTO transaksi (nama_produk, jumlah_beli, total_akhir, voucher_digunakan)
                              VALUES (:n, :q, :t, :v)
                              """), {'n': res.nama, 'q': qty, 't': total_akhir, 'v': kode_v if kode_v else '-'})
            

            #Mencetak struk
            print(f"""
=======================================
            STRUK PEMBELIAN
=======================================
Produk          : {res.nama}
Kuantitas       : {qty} Unit
Subtotal        : Rp {total_awal}
Voucher         : {kode_v if diskon > 0 else '-'}
Diskon          : Rp {diskon}
=======================================

TOTAL BAYAR     : Rp {total_akhir}

=======================================

Terima kasih atas kunjungan anda!
                  """)
    except Exception as e:
        print(f"Terjadi Error saat transaksi {e}")

def main():
    #Membuat engine menjadi global variabel agar dapat digunakna di semua function
    global engine
    engine = buat_koneksi() 
    
    if not engine:
        return
    
    try:
        while True:
            role = login()

            if role == 'admin':
                #Membuat looping untuk menu dashboard admin
                while True:
                    print("""
=======================================
        MENU DASHBOARD ADMIN
=======================================
1. Read Table
2. Show Statistics
3. Data Visualization
4. Add Data
5. Keluar
                        """)
                    pilih = int(input('Pilih Menu: '))

                    if pilih == 1: read_data()
                    elif pilih == 2: show_statistik()
                    elif pilih == 3: data_visualization()
                    elif pilih == 4: add_data()
                    elif pilih == 5: break


            #Membuat looping untuk menu pembeli
            elif role == 'pembeli':
                while True:
                    print("1. Beli barang")
                    print("2. Keluar")
                    pilih = int(input('Pilih Menu: '))

                    if pilih == 1: pembelian()
                    elif pilih == 2: break

            elif role == "exit":
                print("Mematikan Sistem... Sampai Jumpa!")
                break

    #Mematikan koneksi dengan MySQL
    finally:
        engine.dispose()
        print("Koneksi Database ditutup")
 
if __name__ == '__main__':
    main()