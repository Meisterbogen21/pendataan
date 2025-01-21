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
def ganti_mobil():
    pelanggan_df = pd.read_csv('data_pelanggan.csv')
    mobil_df = pd.read_csv('data_mobil.csv')

    nama_pelanggan_list = pelanggan_df['Nama Pelanggan'].tolist()
    nama_pelanggan = st.selectbox("Pilih Nama Pelanggan", nama_pelanggan_list)

    if nama_pelanggan:
        pelanggan = pelanggan_df[pelanggan_df['Nama Pelanggan'] == nama_pelanggan]
        mobil_saat_ini = pelanggan['Mobil Disewa'].values[0]

        st.write(f"Mobil yang sedang disewa: **{mobil_saat_ini}**")

        mobil_tersedia = mobil_df[mobil_df['Status'] == 'Tersedia']['Nama Mobil']
        mobil_baru = st.selectbox("Pilih Mobil Pengganti", mobil_tersedia)

        if st.button("Ganti Mobil"):
            # Update data pelanggan dan mobil
            pelanggan_df.loc[pelanggan_df['Nama Pelanggan'] == nama_pelanggan, 'Mobil Disewa'] = mobil_baru
            mobil_df.loc[mobil_df['Nama Mobil'] == mobil_saat_ini, 'Status'] = 'Tersedia'
            mobil_df.loc[mobil_df['Nama Mobil'] == mobil_baru, 'Status'] = 'Tersewa'

            mobil_df.to_csv('data_mobil.csv', index=False)
            pelanggan_df.to_csv('data_pelanggan.csv', index=False)

            st.success(f"Mobil untuk {nama_pelanggan} berhasil diganti menjadi {mobil_baru}!")

# Fungsi untuk menyelesaikan pesanan
def selesaikan_pesanan():
    pelanggan_df = pd.read_csv('data_pelanggan.csv')
    mobil_df = pd.read_csv('data_mobil.csv')

    nama_pelanggan_list = pelanggan_df['Nama Pelanggan'].tolist()
    nama_pelanggan = st.selectbox("Pilih Nama Penyewa", nama_pelanggan_list)

    if nama_pelanggan:
        pelanggan = pelanggan_df[pelanggan_df['Nama Pelanggan'] == nama_pelanggan]
        mobil_disewa = pelanggan['Mobil Disewa'].values[0]
        tanggal_penyewaan = pd.to_datetime(pelanggan['Tanggal Penyewaan'].values[0])
        tanggal_pengembalian = pd.to_datetime(pelanggan['Tanggal Pengembalian'].values[0])
        deposit = pelanggan['Deposit'].values[0]

        mobil_terpilih = mobil_df[mobil_df['Nama Mobil'] == mobil_disewa]
        harga_sewa = mobil_terpilih['Harga Sewa'].values[0]

        jumlah_hari = (tanggal_pengembalian - tanggal_penyewaan).days
        total_harga = (harga_sewa * jumlah_hari) - deposit

        st.write(f"**Mobil yang disewa:** {mobil_disewa}")
        st.write(f"**Total Harga yang Harus Dibayar:** Rp{total_harga}")

        if st.button("Selesaikan Pesanan"):
            mobil_df.loc[mobil_df['Nama Mobil'] == mobil_disewa, 'Status'] = 'Tersedia'
            pelanggan_df = pelanggan_df[pelanggan_df['Nama Pelanggan'] != nama_pelanggan]
            mobil_df.to_csv('data_mobil.csv', index=False)
            pelanggan_df.to_csv('data_pelanggan.csv', index=False)
            st.success(f"Pesanan atas nama {nama_pelanggan} berhasil diselesaikan!")

# Menjalankan aplikasi Streamlit
def main():
    create_csv_if_not_exists()

    st.title("Sistem Pendataan Sewa Mobil")

    menu = ["Dashboard", "Daftar Mobil", "Daftar Pelanggan", "Tabel Mobil", "Tabel Pelanggan", "Ganti Mobil", "Selesaikan Pesanan"]
    choice = st.sidebar.selectbox("Pilih Menu", menu)

    if choice == "Dashboard":
        st.subheader("Selamat datang di sistem pendataan sewa mobil")

    elif choice == "Daftar Mobil":
        st.subheader("Formulir Daftar Mobil")
        nama_mobil = st.text_input("Nama Mobil")
        tipe_mobil = st.selectbox("Tipe Mobil", ["SUV", "MPV", "Sedan", "Hatchback", "Pickup"])
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
        ganti_mobil()

    elif choice == "Selesaikan Pesanan":
        st.subheader("Selesaikan Pesanan")
        selesaikan_pesanan()

if __name__ == "__main__":
    main()
