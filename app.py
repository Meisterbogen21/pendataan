import streamlit as st
import pandas as pd
import os

# Membuat file CSV untuk dataset jika belum ada
def create_csv_if_not_exists():
    if not os.path.exists('data_mobil.csv'):
        mobil_data = {
            'ID Mobil': [],
            'Nama Mobil': [],
            'Tipe Mobil': [],
            'Harga Sewa': [],
            'Transmisi': [],
            'Jumlah Penumpang': [],
            'Plat Nomor': [],
            'Status': []
        }
        mobil_df = pd.DataFrame(mobil_data)
        mobil_df.to_csv('data_mobil.csv', index=False)

    if not os.path.exists('data_pelanggan.csv'):
        pelanggan_data = {
            'ID Pelanggan': [],
            'Nama Pelanggan': [],
            'Alamat': [],
            'No Telepon': [],
            'KTP Penyewa': [],
            'Tanggal Lahir': [],
            'Jenis Kelamin': [],
            'Mobil Disewa': [],
            'Tanggal Penyewaan': [],
            'Tanggal Pengembalian': [],
            'Deposit': []
        }
        pelanggan_df = pd.DataFrame(pelanggan_data)
        pelanggan_df.to_csv('data_pelanggan.csv', index=False)

# Fungsi untuk menampilkan data mobil
def tampilkan_data_mobil():
    mobil_df = pd.read_csv('data_mobil.csv')
    st.write(mobil_df)

# Fungsi untuk menampilkan data pelanggan
def tampilkan_data_pelanggan():
    pelanggan_df = pd.read_csv('data_pelanggan.csv')
    st.write(pelanggan_df)

# Fungsi untuk mendaftarkan mobil baru
def daftar_mobil(nama_mobil, tipe_mobil, harga_sewa, transmisi, jumlah_penumpang, plat_nomor):
    mobil_df = pd.read_csv('data_mobil.csv')
    id_mobil = len(mobil_df) + 1
    new_data = {
        'ID Mobil': [id_mobil],
        'Nama Mobil': [nama_mobil],
        'Tipe Mobil': [tipe_mobil],
        'Harga Sewa': [harga_sewa],
        'Transmisi': [transmisi],
        'Jumlah Penumpang': [jumlah_penumpang],
        'Plat Nomor': [plat_nomor],
        'Status': ['Tersedia']
    }
    new_mobil_df = pd.DataFrame(new_data)
    mobil_df = pd.concat([mobil_df, new_mobil_df], ignore_index=True)
    mobil_df.to_csv('data_mobil.csv', index=False)
    st.success("Mobil berhasil didaftarkan!")

# Fungsi untuk mendaftarkan pelanggan baru
def daftar_pelanggan(nama_pelanggan, alamat, no_telepon, ktp_penyewa, tanggal_lahir, jenis_kelamin, mobil_disewa, tanggal_penyewaan, tanggal_pengembalian):
    mobil_df = pd.read_csv('data_mobil.csv')
    pelanggan_df = pd.read_csv('data_pelanggan.csv')
    
    # Cek jika mobil yang dipilih tersedia
    mobil_terpilih = mobil_df[mobil_df['Nama Mobil'] == mobil_disewa]
    if mobil_terpilih.empty or mobil_terpilih['Status'].values[0] != 'Tersedia':
        st.warning("Mobil yang dipilih sudah disewa atau tidak tersedia!")
        return
    
    id_pelanggan = len(pelanggan_df) + 1
    deposit = mobil_terpilih['Harga Sewa'].values[0] * (tanggal_pengembalian - tanggal_penyewaan).days * 0.1
    new_data = {
        'ID Pelanggan': [id_pelanggan],
        'Nama Pelanggan': [nama_pelanggan],
        'Alamat': [alamat],
        'No Telepon': [no_telepon],
        'KTP Penyewa': [ktp_penyewa],
        'Tanggal Lahir': [tanggal_lahir],
        'Jenis Kelamin': [jenis_kelamin],
        'Mobil Disewa': [mobil_disewa],
        'Tanggal Penyewaan': [tanggal_penyewaan],
        'Tanggal Pengembalian': [tanggal_pengembalian],
        'Deposit': [deposit]
    }
    new_pelanggan_df = pd.DataFrame(new_data)
    pelanggan_df = pd.concat([pelanggan_df, new_pelanggan_df], ignore_index=True)

    # Update status mobil menjadi 'Tersewa'
    mobil_df.loc[mobil_df['Nama Mobil'] == mobil_disewa, 'Status'] = 'Tersewa'
    mobil_df.to_csv('data_mobil.csv', index=False)
    pelanggan_df.to_csv('data_pelanggan.csv', index=False)
    
    st.success("Pelanggan berhasil didaftarkan!")

# Fungsi untuk mengganti mobil penyewa
def ganti_mobil(nama_pelanggan):
    mobil_df = pd.read_csv('data_mobil.csv')
    pelanggan_df = pd.read_csv('data_pelanggan.csv')
    
    # Cari pelanggan berdasarkan nama
    pelanggan = pelanggan_df[pelanggan_df['Nama Pelanggan'] == nama_pelanggan]
    if pelanggan.empty:
        st.warning("Pelanggan tidak ditemukan!")
        return

    # Tampilkan mobil yang sedang disewa
    mobil_disewa = pelanggan['Mobil Disewa'].values[0]
    st.write(f"Mobil yang sedang disewa: {mobil_disewa}")

    # Cek mobil yang tersedia
    mobil_tersedia = mobil_df[mobil_df['Status'] == 'Tersedia']
    mobil_baru = st.selectbox("Pilih mobil pengganti", mobil_tersedia['Nama Mobil'])

    if st.button("Ganti Mobil"):
        # Update data pelanggan dan mobil
        pelanggan_df.loc[pelanggan_df['Nama Pelanggan'] == nama_pelanggan, 'Mobil Disewa'] = mobil_baru

        # Update status mobil lama menjadi 'Tersedia' dan mobil baru menjadi 'Tersewa'
        mobil_df.loc[mobil_df['Nama Mobil'] == mobil_disewa, 'Status'] = 'Tersedia'
        mobil_df.loc[mobil_df['Nama Mobil'] == mobil_baru, 'Status'] = 'Tersewa'

        mobil_df.to_csv('data_mobil.csv', index=False)
        pelanggan_df.to_csv('data_pelanggan.csv', index=False)

        st.success(f"Mobil untuk {nama_pelanggan} berhasil diganti menjadi {mobil_baru}!")

# Fungsi untuk mencari pelanggan
def cari_pelanggan(nama_pelanggan):
    pelanggan_df = pd.read_csv('data_pelanggan.csv')
    pelanggan = pelanggan_df[pelanggan_df['Nama Pelanggan'].str.contains(nama_pelanggan, case=False, na=False)]
    if pelanggan.empty:
        st.warning("Pelanggan tidak ditemukan!")
    else:
        st.write(pelanggan)

# Fungsi untuk mencari mobil
def cari_mobil(nama_mobil):
    mobil_df = pd.read_csv('data_mobil.csv')
    mobil = mobil_df[mobil_df['Nama Mobil'].str.contains(nama_mobil, case=False, na=False)]
    if mobil.empty:
        st.warning("Mobil tidak ditemukan!")
    else:
        st.write(mobil)

# Menjalankan aplikasi Streamlit
def main():
    create_csv_if_not_exists()

    st.title("Sistem Pendataan Sewa Mobil")

    menu = ["Dashboard", "Daftar Mobil", "Daftar Pelanggan", "Tabel Mobil", "Tabel Pelanggan", "Ganti Mobil", "Cari Pelanggan", "Cari Mobil"]
    choice = st.sidebar.selectbox("Pilih Menu", menu)

    if choice == "Dashboard":
        st.subheader("Selamat datang di sistem pendataan sewa mobil")

    elif choice == "Daftar Mobil":
        st.subheader("Formulir Daftar Mobil")
        nama_mobil = st.text_input("Nama Mobil")
        tipe_mobil = st.selectbox("Tipe Mobil", ["SUV", "MPV", "Sedan", "Hatchback", "Pickup", "Sports", "4x4"])  # Pilihan tipe mobil sesuai dataset
        harga_sewa = st.number_input("Harga Sewa", min_value=100000, step=1000)
        transmisi = st.selectbox("Transmisi", ["Manual", "Automatic"])
        jumlah_penumpang = st.number_input("Jumlah Penumpang", min_value=1)
        plat_nomor = st.text_input("Plat Nomor")

        if st.button("Daftar Mobil"):
            daftar_mobil(nama_mobil, tipe_mobil, harga_sewa, transmisi, jumlah_penumpang, plat_nomor)

    elif choice == "Daftar Pelanggan":
        st.subheader("Formulir Daftar Pelanggan")
        nama_pelanggan = st.text_input("Nama Pelanggan")
        alamat = st.text_area("Alamat")
        no_telepon = st.text_input("No Telepon")
        ktp_penyewa = st.text_input("KTP Penyewa")
        tanggal_lahir = st.date_input("Tanggal Lahir")
        jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        
        # Pilih mobil yang tersedia
        mobil_df = pd.read_csv('data_mobil.csv')
        mobil_tersedia = mobil_df[mobil_df['Status'] == 'Tersedia']
        mobil_disewa = st.selectbox("Pilih Mobil yang Disewa", mobil_tersedia['Nama Mobil'])

        tanggal_penyewaan = st.date_input("Tanggal Penyewaan")
        tanggal_pengembalian = st.date_input("Tanggal Pengembalian")

        if st.button("Daftar Pelanggan"):
            daftar_pelanggan(nama_pelanggan, alamat, no_telepon, ktp_penyewa, tanggal_lahir, jenis_kelamin, mobil_disewa, tanggal_penyewaan, tanggal_pengembalian)

    elif choice == "Tabel Mobil":
        tampilkan_data_mobil()

    elif choice == "Tabel Pelanggan":
        tampilkan_data_pelanggan()

    elif choice == "Ganti Mobil":
        st.subheader("Ganti Mobil Penyewa")
        nama_pelanggan = st.text_input("Nama Penyewa")
        if st.button("Cari Penyewa"):
            ganti_mobil(nama_pelanggan)

    elif choice == "Cari Pelanggan":
        st.subheader("Cari Pelanggan")
        nama_pelanggan = st.text_input("Nama Pelanggan")
        if st.button("Cari"):
            cari_pelanggan(nama_pelanggan)

    elif choice == "Cari Mobil":
        st.subheader("Cari Mobil")
        nama_mobil = st.text_input("Nama Mobil")
        if st.button("Cari"):
            cari_mobil(nama_mobil)

if __name__ == "__main__":
    main()
