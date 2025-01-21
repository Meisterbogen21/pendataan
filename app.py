import streamlit as st
import pandas as pd
import os

# Fungsi untuk membuat file CSV jika belum ada
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
            'Status': []  # Menambahkan kolom status
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

# Fungsi untuk menyelesaikan pesanan
def selesaikan_pesanan(nama_pelanggan):
    mobil_df = pd.read_csv('data_mobil.csv')
    pelanggan_df = pd.read_csv('data_pelanggan.csv')

    # Cari pelanggan berdasarkan nama
    pelanggan = pelanggan_df[pelanggan_df['Nama Pelanggan'].str.contains(nama_pelanggan, case=False, na=False)]

    if not pelanggan.empty:
        pelanggan_data = pelanggan.iloc[0]
        mobil_disewa = pelanggan_data['Mobil Disewa']
        tanggal_penyewaan = pd.to_datetime(pelanggan_data['Tanggal Penyewaan'])
        tanggal_pengembalian = pd.to_datetime(pelanggan_data['Tanggal Pengembalian'])

        # Menghitung jumlah hari sewa
        jumlah_hari = (tanggal_pengembalian - tanggal_penyewaan).days

        # Mencari mobil yang disewa
        mobil = mobil_df[mobil_df['Nama Mobil'] == mobil_disewa]

        if not mobil.empty:
            harga_sewa_per_hari = mobil['Harga Sewa'].values[0]
            deposit = pelanggan_data['Deposit']

            # Hitung total harga yang harus dibayar
            total_harga = harga_sewa_per_hari * jumlah_hari
            total_bayar = total_harga - deposit

            # Menampilkan informasi
            st.write(f"Nama Penyewa: {pelanggan_data['Nama Pelanggan']}")
            st.write(f"Mobil yang Disewa: {mobil_disewa}")
            st.write(f"Tanggal Penyewaan: {tanggal_penyewaan.strftime('%Y-%m-%d')}")
            st.write(f"Tanggal Pengembalian: {tanggal_pengembalian.strftime('%Y-%m-%d')}")
            st.write(f"Total Harga Sewa (tanpa deposit): Rp {total_harga}")
            st.write(f"Deposit: Rp {deposit}")
            st.write(f"Total yang Harus Dibayar: Rp {total_bayar}")

            # Menghapus data pelanggan yang telah selesai
            pelanggan_df = pelanggan_df[pelanggan_df['ID Pelanggan'] != pelanggan_data['ID Pelanggan']]
            pelanggan_df.to_csv('data_pelanggan.csv', index=False)

            # Set mobil menjadi tersedia setelah pesanan selesai
            mobil_df.loc[mobil_df['Nama Mobil'] == mobil_disewa, 'Status'] = 'Tersedia'
            mobil_df.to_csv('data_mobil.csv', index=False)

            st.success(f"Pesanan untuk {pelanggan_data['Nama Pelanggan']} telah diselesaikan dan data pelanggan telah dihapus!")

        else:
            st.warning("Mobil yang disewa tidak ditemukan!")
    else:
        st.warning("Pelanggan tidak ditemukan!")

# Fungsi untuk mengganti mobil penyewa
def ganti_mobil_penyewa(id_pelanggan, mobil_baru):
    mobil_df = pd.read_csv('data_mobil.csv')
    pelanggan_df = pd.read_csv('data_pelanggan.csv')

    pelanggan = pelanggan_df[pelanggan_df['ID Pelanggan'] == id_pelanggan]

    if not pelanggan.empty:
        mobil_sebelumnya = pelanggan['Mobil Disewa'].values[0]
        if mobil_sebelumnya == mobil_baru:
            st.warning("Mobil yang dipilih sama dengan mobil sebelumnya!")
        else:
            # Update data mobil penyewa
            pelanggan_df.loc[pelanggan_df['ID Pelanggan'] == id_pelanggan, 'Mobil Disewa'] = mobil_baru
            pelanggan_df.to_csv('data_pelanggan.csv', index=False)

            # Mengupdate status mobil
            mobil_df.loc[mobil_df['Nama Mobil'] == mobil_sebelumnya, 'Status'] = 'Tersedia'
            mobil_df.loc[mobil_df['Nama Mobil'] == mobil_baru, 'Status'] = 'Tersewa'
            mobil_df.to_csv('data_mobil.csv', index=False)

            st.success(f"Mobil penyewa ID {id_pelanggan} berhasil diganti menjadi {mobil_baru}!")
    else:
        st.warning("Pelanggan tidak ditemukan!")

# Fungsi untuk menampilkan data mobil
def tampilkan_data_mobil():
    mobil_df = pd.read_csv('data_mobil.csv')
    st.write(mobil_df)

# Fungsi untuk menampilkan data pelanggan
def tampilkan_data_pelanggan():
    pelanggan_df = pd.read_csv('data_pelanggan.csv')
    st.write(pelanggan_df)

# Fungsi untuk mencari data mobil berdasarkan nama
def cari_mobil_by_name(nama_mobil):
    mobil_df = pd.read_csv('data_mobil.csv')
    result = mobil_df[mobil_df['Nama Mobil'].str.contains(nama_mobil, case=False, na=False)]
    if not result.empty:
        st.write(result)
    else:
        st.warning("Mobil tidak ditemukan!")

# Fungsi untuk mencari data pelanggan berdasarkan nama
def cari_pelanggan_by_name(nama_pelanggan):
    pelanggan_df = pd.read_csv('data_pelanggan.csv')
    result = pelanggan_df[pelanggan_df['Nama Pelanggan'].str.contains(nama_pelanggan, case=False, na=False)]
    if not result.empty:
        st.write(result)
    else:
        st.warning("Pelanggan tidak ditemukan!")

# Menjalankan aplikasi Streamlit
def main():
    create_csv_if_not_exists()

    st.title("Sistem Pendataan Sewa Mobil")

    menu = ["Dashboard", "Selesaikan Pesanan", "Daftar Mobil", "Daftar Pelanggan", "Tabel Mobil", "Tabel Pelanggan", "Cari Mobil", "Cari Pelanggan", "Ganti Mobil Penyewa"]
    choice = st.sidebar.selectbox("Pilih Menu", menu)

    if choice == "Dashboard":
        st.subheader("Selamat datang di sistem pendataan sewa mobil")

    elif choice == "Selesaikan Pesanan":
        st.subheader("Selesaikan Pesanan")
        nama_pelanggan = st.text_input("Masukkan Nama Penyewa")

        if st.button("Selesaikan Pesanan"):
            if nama_pelanggan:
                selesaikan_pesanan(nama_pelanggan)
            else:
                st.warning("Nama penyewa harus diisi!")

    elif choice == "Ganti Mobil Penyewa":
        st.subheader("Ganti Mobil Penyewa")
        id_pelanggan = st.number_input("Masukkan ID Pelanggan", min_value=1)
        mobil_baru = st.selectbox("Pilih Mobil Baru", ["Toyota Avanza", "Honda Civic", "Isuzu Panther", "Mitsubishi Pajero", "Daihatsu Xenia", "Suzuki Swift", "Nissan X-Trail", "Hyundai Elantra", "Ford Ranger", "Chevrolet Trax"])

        if st.button("Ganti Mobil"):
            ganti_mobil_penyewa(id_pelanggan, mobil_baru)

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
        mobil_disewa = st.selectbox("Mobil Disewa", ["Toyota Avanza", "Honda Civic", "Isuzu Panther", "Mitsubishi Pajero", "Daihatsu Xenia", "Suzuki Swift", "Nissan X-Trail", "Hyundai Elantra", "Ford Ranger", "Chevrolet Trax"])
        tanggal_penyewaan = st.date_input("Tanggal Penyewaan")
        tanggal_pengembalian = st.date_input("Tanggal Pengembalian")

        if st.button("Daftar Pelanggan"):
            daftar_pelanggan(nama_pelanggan, alamat, no_telepon, ktp_penyewa, tanggal_lahir, jenis_kelamin, mobil_disewa, tanggal_penyewaan, tanggal_pengembalian)

    elif choice == "Tabel Mobil":
        st.subheader("Tabel Mobil")
        tampilkan_data_mobil()

    elif choice == "Tabel Pelanggan":
        st.subheader("Tabel Pelanggan")
        tampilkan_data_pelanggan()

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

if __name__ == "__main__":
    main()
