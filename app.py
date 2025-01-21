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
            'Plat Nomor': []  # Menambahkan kolom Plat Nomor
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
            'Deposit': []  # Menambahkan kolom Deposit
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
        'Plat Nomor': [plat_nomor]  # Menambahkan Plat Nomor
    }
    new_mobil_df = pd.DataFrame(new_data)
    mobil_df = pd.concat([mobil_df, new_mobil_df], ignore_index=True)
    mobil_df.to_csv('data_mobil.csv', index=False)
    st.success("Mobil berhasil didaftarkan!")

# Fungsi untuk mendaftarkan pelanggan baru
def daftar_pelanggan(nama_pelanggan, alamat, no_telepon, ktp_penyewa, tanggal_lahir, jenis_kelamin, mobil_disewa, tanggal_penyewaan, tanggal_pengembalian):
    mobil_df = pd.read_csv('data_mobil.csv')
    pelanggan_df = pd.read_csv('data_pelanggan.csv')
    
    # Menghapus koma dari nomor telepon dan nomor KTP
    no_telepon = no_telepon.replace(',', '')
    ktp_penyewa = ktp_penyewa.replace(',', '')
    
    id_pelanggan = len(pelanggan_df) + 1
    # Menghitung deposit
    harga_sewa_perhari = mobil_df[mobil_df['Nama Mobil'] == mobil_disewa]['Harga Sewa'].values[0]
    durasi_sewa = (tanggal_pengembalian - tanggal_penyewaan).days
    total_harga = harga_sewa_perhari * durasi_sewa
    deposit = total_harga * 0.10
    
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
        'Deposit': [deposit]  # Menambahkan Deposit
    }
    new_pelanggan_df = pd.DataFrame(new_data)
    pelanggan_df = pd.concat([pelanggan_df, new_pelanggan_df], ignore_index=True)
    pelanggan_df.to_csv('data_pelanggan.csv', index=False)
    st.success("Pelanggan berhasil didaftarkan!")

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
def selesaikan_pesanan(id_pelanggan, nama_mobil):
    mobil_df = pd.read_csv('data_mobil.csv')
    pelanggan_df = pd.read_csv('data_pelanggan.csv')

    mobil = mobil_df[mobil_df['Nama Mobil'] == nama_mobil]
    pelanggan = pelanggan_df[pelanggan_df['ID Pelanggan'] == id_pelanggan]

    if not mobil.empty and not pelanggan.empty:
        st.success(f"Pesanan untuk {pelanggan['Nama Pelanggan'].values[0]} telah diselesaikan! Mobil: {mobil['Nama Mobil'].values[0]}")
    else:
        st.warning("Pesanan gagal! Pastikan ID pelanggan dan nama mobil valid.")

# Fungsi untuk mengganti mobil penyewa
def ganti_mobil_penyewa(id_pelanggan, mobil_pengganti):
    mobil_df = pd.read_csv('data_mobil.csv')
    pelanggan_df = pd.read_csv('data_pelanggan.csv')

    # Update mobil yang disewa oleh pelanggan
    pelanggan_df.loc[pelanggan_df['ID Pelanggan'] == id_pelanggan, 'Mobil Disewa'] = mobil_pengganti
    
    # Ambil tipe mobil pengganti
    tipe_mobil_pengganti = mobil_df[mobil_df['Nama Mobil'] == mobil_pengganti]['Tipe Mobil'].values[0]
    
    # Tampilkan tipe mobil yang dipilih
    st.success(f"Mobil penyewa telah diganti dengan {mobil_pengganti} ({tipe_mobil_pengganti})")

    # Simpan data pelanggan yang telah diperbarui
    pelanggan_df.to_csv('data_pelanggan.csv', index=False)

# Menjalankan aplikasi Streamlit
def main():
    create_csv_if_not_exists()

    st.title("Sistem Pendataan Sewa Mobil")

    menu = ["Dashboard", "Daftar Mobil", "Daftar Pelanggan", "Tabel Mobil", "Tabel Pelanggan", "Selesaikan Pesanan", "Cari Mobil", "Cari Pelanggan", "Ganti Mobil Penyewa"]
    choice = st.sidebar.selectbox("Pilih Menu", menu)

    if choice == "Dashboard":
        st.subheader("Selamat datang di sistem pendataan sewa mobil")

    elif choice == "Daftar Mobil":
        st.subheader("Formulir Daftar Mobil")
        nama_mobil = st.text_input("Nama Mobil")
        tipe_mobil = st.text_input("Tipe Mobil")
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
        mobil_disewa = st.selectbox("Mobil yang Disewa", ["Toyota Avanza", "Honda Civic", "Isuzu Panther", "Mitsubishi Pajero", "Daihatsu Xenia", "Suzuki Swift", "Nissan X-Trail", "Hyundai Elantra", "Ford Ranger", "Chevrolet Trax"])
        tanggal_penyewaan = st.date_input("Tanggal Penyewaan")
        tanggal_pengembalian = st.date_input("Tanggal Pengembalian")

        if st.button("Daftar Pelanggan"):
            daftar_pelanggan(nama_pelanggan, alamat, no_telepon, ktp_penyewa, tanggal_lahir, jenis_kelamin, mobil_disewa, tanggal_penyewaan, tanggal_pengembalian)

    elif choice == "Tabel Mobil":
        st.subheader("Data Mobil")
        tampilkan_data_mobil()

    elif choice == "Tabel Pelanggan":
        st.subheader("Data Pelanggan")
        tampilkan_data_pelanggan()

    elif choice == "Selesaikan Pesanan":
        st.subheader("Selesaikan Pesanan")
        pelanggan_df = pd.read_csv('data_pelanggan.csv')
        pilihan_pelanggan = st.selectbox("Pilih Pelanggan", pelanggan_df['Nama Pelanggan'].unique())

        pilihan_mobil = st.selectbox("Pilih Mobil", ["Toyota Avanza", "Honda Civic", "Isuzu Panther", "Mitsubishi Pajero", "Daihatsu Xenia", "Suzuki Swift", "Nissan X-Trail", "Hyundai Elantra", "Ford Ranger", "Chevrolet Trax"])

        if st.button("Selesaikan Pesanan"):
            id_pelanggan = pelanggan_df[pelanggan_df['Nama Pelanggan'] == pilihan_pelanggan]['ID Pelanggan'].values[0]
            selesaikan_pesanan(id_pelanggan, pilihan_mobil)

    elif choice == "Cari Mobil":
        st.subheader("Cari Mobil")
        nama_mobil = st.text_input("Cari Nama Mobil")
        if nama_mobil:
            cari_mobil_by_name(nama_mobil)

    elif choice == "Cari Pelanggan":
        st.subheader("Cari Pelanggan")
        nama_pelanggan = st.text_input("Cari Nama Pelanggan")
        if nama_pelanggan:
            cari_pelanggan_by_name(nama_pelanggan)

    elif choice == "Ganti Mobil Penyewa":
        st.subheader("Ganti Mobil Penyewa")
        pelanggan_df = pd.read_csv('data_pelanggan.csv')
        pilihan_pelanggan = st.selectbox("Pilih Pelanggan", pelanggan_df['Nama Pelanggan'].unique())
        pilihan_mobil_baru = st.selectbox("Pilih Mobil Pengganti", ["Toyota Avanza", "Honda Civic", "Isuzu Panther", "Mitsubishi Pajero", "Daihatsu Xenia", "Suzuki Swift", "Nissan X-Trail", "Hyundai Elantra", "Ford Ranger", "Chevrolet Trax"])

        if st.button("Ganti Mobil"):
            id_pelanggan = pelanggan_df[pelanggan_df['Nama Pelanggan'] == pilihan_pelanggan]['ID Pelanggan'].values[0]
            ganti_mobil_penyewa(id_pelanggan, pilihan_mobil_baru)

if __name__ == "__main__":
    main()
