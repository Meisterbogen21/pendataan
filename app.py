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
def ganti_mobil(id_pelanggan, mobil_baru):
    mobil_df = pd.read_csv('data_mobil.csv')
    pelanggan_df = pd.read_csv('data_pelanggan.csv')
    
    # Cek apakah mobil baru tersedia
    mobil_terpilih = mobil_df[mobil_df['Nama Mobil'] == mobil_baru]
    if mobil_terpilih.empty or mobil_terpilih['Status'].values[0] != 'Tersedia':
        st.warning("Mobil yang dipilih sudah disewa atau tidak tersedia!")
        return

    # Cari pelanggan berdasarkan ID
    pelanggan = pelanggan_df[pelanggan_df['ID Pelanggan'] == id_pelanggan]
    if pelanggan.empty:
        st.warning("Pelanggan tidak ditemukan!")
        return

    # Update data pelanggan dan mobil
    old_mobil = pelanggan['Mobil Disewa'].values[0]
    pelanggan_df.loc[pelanggan_df['ID Pelanggan'] == id_pelanggan, 'Mobil Disewa'] = mobil_baru

    # Update status mobil lama menjadi 'Tersedia' dan mobil baru menjadi 'Tersewa'
    mobil_df.loc[mobil_df['Nama Mobil'] == old_mobil, 'Status'] = 'Tersedia'
    mobil_df.loc[mobil_df['Nama Mobil'] == mobil_baru, 'Status'] = 'Tersewa'

    mobil_df.to_csv('data_mobil.csv', index=False)
    pelanggan_df.to_csv('data_pelanggan.csv', index=False)

    st.success(f"Mobil untuk {pelanggan['Nama Pelanggan'].values[0]} berhasil diganti menjadi {mobil_baru}!")

# Fungsi untuk mencari data pelanggan berdasarkan nama
def cari_pelanggan_by_name(nama_pelanggan):
    pelanggan_df = pd.read_csv('data_pelanggan.csv')
    result = pelanggan_df[pelanggan_df['Nama Pelanggan'].str.contains(nama_pelanggan, case=False, na=False)]
    if not result.empty:
        st.write(result)
    else:
        st.warning("Pelanggan tidak ditemukan!")

# Fungsi untuk mencari data mobil berdasarkan nama
def cari_mobil_by_name(nama_mobil):
    mobil_df = pd.read_csv('data_mobil.csv')
    result = mobil_df[mobil_df['Nama Mobil'].str.contains(nama_mobil, case=False, na=False)]
    if not result.empty:
        st.write(result)
    else:
        st.warning("Mobil tidak ditemukan!")

# Fungsi untuk menyelesaikan pesanan
def selesaikan_pesanan(nama_pelanggan):
    mobil_df = pd.read_csv('data_mobil.csv')
    pelanggan_df = pd.read_csv('data_pelanggan.csv')

    # Cari pelanggan berdasarkan nama
    pelanggan = pelanggan_df[pelanggan_df['Nama Pelanggan'].str.contains(nama_pelanggan, case=False, na=False)]
    if pelanggan.empty:
        st.warning("Pelanggan tidak ditemukan!")
        return

    # Ambil data pelanggan yang ditemukan
    id_pelanggan = pelanggan['ID Pelanggan'].values[0]
    mobil_disewa = pelanggan['Mobil Disewa'].values[0]
    tanggal_penyewaan = pd.to_datetime(pelanggan['Tanggal Penyewaan'].values[0])
    tanggal_pengembalian = pd.to_datetime(pelanggan['Tanggal Pengembalian'].values[0])
    
    # Cari mobil yang disewa oleh pelanggan
    mobil_terpilih = mobil_df[mobil_df['Nama Mobil'] == mobil_disewa]
    if mobil_terpilih.empty:
        st.warning("Mobil yang disewa tidak ditemukan!")
        return

    harga_sewa = mobil_terpilih['Harga Sewa'].values[0]
    
    # Hitung jumlah hari sewa
    jumlah_hari = (tanggal_pengembalian - tanggal_penyewaan).days
    if jumlah_hari <= 0:
        st.warning("Tanggal pengembalian harus lebih besar dari tanggal penyewaan!")
        return

    # Hitung total harga dan deposit
    total_harga = harga_sewa * jumlah_hari
    deposit = total_harga * 0.1

    # Tampilkan informasi kepada pengguna
    st.write(f"Mobil yang disewa: {mobil_disewa}")
    st.write(f"Jumlah Hari Sewa: {jumlah_hari} hari")
    st.write(f"Total Harga: Rp{total_harga}")
    st.write(f"Deposit: Rp{deposit}")

    # Konfirmasi penyelesaian pesanan
    if st.button("Selesaikan Pesanan"):
        mobil_df.loc[mobil_df['Nama Mobil'] == mobil_disewa, 'Status'] = 'Tersedia'
        pelanggan_df = pelanggan_df[pelanggan_df['ID Pelanggan'] != id_pelanggan]  # Hapus pelanggan dari daftar
        mobil_df.to_csv('data_mobil.csv', index=False)
        pelanggan_df.to_csv('data_pelanggan.csv', index=False)
        st.success(f"Pesanan {nama_pelanggan} berhasil diselesaikan dan mobil telah dikembalikan!")

# Menjalankan aplikasi Streamlit
def main():
    create_csv_if_not_exists()

    st.title("Sistem Pendataan Sewa Mobil")

    menu = ["Dashboard", "Daftar Mobil", "Daftar Pelanggan", "Tabel Mobil", "Tabel Pelanggan", "Ganti Mobil", "Selesaikan Pesanan", "Cari Mobil", "Cari Pelanggan"]
    choice = st.sidebar.selectbox("Pilih Menu", menu)

    if choice == "Dashboard":
        st.subheader("Selamat datang di sistem pendataan sewa mobil")

    elif choice == "Daftar Mobil":
        st.subheader("Formulir Daftar Mobil")
        nama_mobil = st.text_input("Nama Mobil")
        tipe_mobil = st.selectbox("Tipe Mobil", ["SUV", "MPV", "Sedan", "Hatchback", "Coupe", "Convertible"])
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
        mobil_disewa = st.selectbox("Mobil Disewa", mobil_tersedia['Nama Mobil'])

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
        id_pelanggan = st.number_input("ID Pelanggan", min_value=1)
        mobil_baru = st.text_input("Mobil Baru")

        if st.button("Ganti Mobil"):
            ganti_mobil(id_pelanggan, mobil_baru)

    elif choice == "Selesaikan Pesanan":
        nama_pelanggan = st.text_input("Nama Penyewa")
        if st.button("Cari Penyewa"):
            selesaikan_pesanan(nama_pelanggan)

    elif choice == "Cari Mobil":
        nama_mobil = st.text_input("Nama Mobil")
        if st.button("Cari Mobil"):
            cari_mobil_by_name(nama_mobil)

    elif choice == "Cari Pelanggan":
        nama_pelanggan = st.text_input("Nama Pelanggan")
        if st.button("Cari Pelanggan"):
            cari_pelanggan_by_name(nama_pelanggan)

if __name__ == "__main__":
    main()
