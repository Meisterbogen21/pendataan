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
            'Fitur Tambahan': []
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
            'Jenis Kelamin': []
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
def daftar_mobil(nama_mobil, tipe_mobil, harga_sewa, transmisi, jumlah_penumpang, fitur_tambahan):
    mobil_df = pd.read_csv('data_mobil.csv')
    id_mobil = len(mobil_df) + 1
    new_data = {
        'ID Mobil': [id_mobil],
        'Nama Mobil': [nama_mobil],
        'Tipe Mobil': [tipe_mobil],
        'Harga Sewa': [harga_sewa],
        'Transmisi': [transmisi],
        'Jumlah Penumpang': [jumlah_penumpang],
        'Fitur Tambahan': [fitur_tambahan]
    }
    new_mobil_df = pd.DataFrame(new_data)
    mobil_df = pd.concat([mobil_df, new_mobil_df], ignore_index=True)
    mobil_df.to_csv('data_mobil.csv', index=False)
    st.success("Mobil berhasil didaftarkan!")

# Fungsi untuk mendaftarkan pelanggan baru
def daftar_pelanggan(nama_pelanggan, alamat, no_telepon, ktp_penyewa, tanggal_lahir, jenis_kelamin):
    pelanggan_df = pd.read_csv('data_pelanggan.csv')
    id_pelanggan = len(pelanggan_df) + 1
    new_data = {
        'ID Pelanggan': [id_pelanggan],
        'Nama Pelanggan': [nama_pelanggan],
        'Alamat': [alamat],
        'No Telepon': [no_telepon],
        'KTP Penyewa': [ktp_penyewa],
        'Tanggal Lahir': [tanggal_lahir],
        'Jenis Kelamin': [jenis_kelamin]
    }
    new_pelanggan_df = pd.DataFrame(new_data)
    pelanggan_df = pd.concat([pelanggan_df, new_pelanggan_df], ignore_index=True)
    pelanggan_df.to_csv('data_pelanggan.csv', index=False)
    st.success("Pelanggan berhasil didaftarkan!")

# Fungsi untuk mencari data pelanggan
def cari_pelanggan(id_pelanggan):
    pelanggan_df = pd.read_csv('data_pelanggan.csv')
    result = pelanggan_df[pelanggan_df['ID Pelanggan'] == id_pelanggan]
    if not result.empty:
        st.write(result)
    else:
        st.warning("Pelanggan tidak ditemukan!")

# Fungsi untuk mencari data mobil
def cari_mobil(id_mobil):
    mobil_df = pd.read_csv('data_mobil.csv')
    result = mobil_df[mobil_df['ID Mobil'] == id_mobil]
    if not result.empty:
        st.write(result)
    else:
        st.warning("Mobil tidak ditemukan!")

# Fungsi untuk menyelesaikan pesanan
def selesaikan_pesanan(id_pelanggan, id_mobil):
    mobil_df = pd.read_csv('data_mobil.csv')
    pelanggan_df = pd.read_csv('data_pelanggan.csv')

    mobil = mobil_df[mobil_df['ID Mobil'] == id_mobil]
    pelanggan = pelanggan_df[pelanggan_df['ID Pelanggan'] == id_pelanggan]

    if not mobil.empty and not pelanggan.empty:
        st.success(f"Pesanan untuk {pelanggan['Nama Pelanggan'].values[0]} telah diselesaikan! Mobil: {mobil['Nama Mobil'].values[0]}")
    else:
        st.warning("Pesanan gagal! Pastikan ID pelanggan dan ID mobil valid.")

# Menjalankan aplikasi Streamlit
def main():
    create_csv_if_not_exists()

    st.title("Sistem Pendataan Sewa Mobil")

    menu = ["Dashboard", "Daftar Mobil", "Daftar Pelanggan", "Tabel Mobil", "Tabel Pelanggan", "Selesaikan Pesanan", "Cari Mobil", "Cari Pelanggan"]
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
        fitur_tambahan = st.text_area("Fitur Tambahan (Pisahkan dengan koma)")

        if st.button("Daftar Mobil"):
            daftar_mobil(nama_mobil, tipe_mobil, harga_sewa, transmisi, jumlah_penumpang, fitur_tambahan)

    elif choice == "Daftar Pelanggan":
        st.subheader("Formulir Daftar Pelanggan")
        nama_pelanggan = st.text_input("Nama Pelanggan")
        alamat = st.text_area("Alamat")
        no_telepon = st.text_input("No Telepon")
        ktp_penyewa = st.text_input("KTP Penyewa")
        tanggal_lahir = st.date_input("Tanggal Lahir")
        jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

        if st.button("Daftar Pelanggan"):
            daftar_pelanggan(nama_pelanggan, alamat, no_telepon, ktp_penyewa, tanggal_lahir, jenis_kelamin)

    elif choice == "Tabel Mobil":
        tampilkan_data_mobil()

    elif choice == "Tabel Pelanggan":
        tampilkan_data_pelanggan()

    elif choice == "Selesaikan Pesanan":
        st.subheader("Selesaikan Pesanan")
        id_pelanggan = st.number_input("ID Pelanggan", min_value=1)
        id_mobil = st.number_input("ID Mobil", min_value=1)

        if st.button("Selesaikan Pesanan"):
            selesaikan_pesanan(id_pelanggan, id_mobil)

    elif choice == "Cari Mobil":
        st.subheader("Cari Mobil")
        id_mobil = st.number_input("ID Mobil", min_value=1)
        if st.button("Cari Mobil"):
            cari_mobil(id_mobil)

    elif choice == "Cari Pelanggan":
        st.subheader("Cari Pelanggan")
        id_pelanggan = st.number_input("ID Pelanggan", min_value=1)
        if st.button("Cari Pelanggan"):
            cari_pelanggan(id_pelanggan)

if __name__ == "__main__":
    main()
