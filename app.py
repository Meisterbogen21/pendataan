import streamlit as st
import pandas as pd
import requests

# Load dataset from GitHub URLs
mobil_url = "https://raw.githubusercontent.com/Meisterbogen21/python8/refs/heads/main/mobil_data_spesifik.csv"
penyewa_url = "https://raw.githubusercontent.com/Meisterbogen21/python8/refs/heads/main/penyewa_data_spesifik.csv"

@st.cache_data
def load_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_csv(url)

mobil_data = load_data(mobil_url)
penyewa_data = load_data(penyewa_url)

# Initialize Streamlit app
st.title("Sistem Pendataan Sewa Mobil")

menu = st.sidebar.selectbox("Pilih Menu", [
    "Daftarkan Penyewa",
    "Daftarkan Mobil Baru",
    "Tampilkan Tabel Mobil",
    "Tampilkan Tabel Pelanggan",
    "Selesaikan Pesanan",
    "Cari Data Pelanggan",
    "Cari Data Mobil"
])

if menu == "Daftarkan Penyewa":
  
    st.header("Daftarkan Penyewa Baru")
    nama = st.text_input("Nama Penyewa")
    alamat = st.text_input("Alamat")
    no_telepon = st.text_input("No Telepon")
    email = st.text_input("Email")
    pilihan_mobil = st.selectbox("Pilih Mobil", mobil_data['nama_mobil'] + " - " + mobil_data['transmisi'] + " - " + mobil_data['tipe_mobil'])
    tanggal_mulai = st.date_input("Tanggal Mulai Penyewaan")
    tanggal_selesai = st.date_input("Tanggal Selesai Penyewaan")

    if st.button("Simpan Penyewaan"):
        selected_mobil_id = pilihan_mobil.split(" - ")[0]

        # Tambahkan data penyewa baru
        new_penyewa = pd.DataFrame({
            Nama': [nama],
            'Alamat': [alamat],
            'No_Telepon': [no_telepon],
            'Email': [email],
            'ID_Mobil': [selected_mobil_id],
            'Tanggal_Mulai': [tanggal_mulai],
            'Tanggal_Selesai': [tanggal_selesai]
        })
        global penyewa_data
        penyewa_data = pd.concat([penyewa_data, new_penyewa], ignore_index=True)

        st.success("Penyewaan berhasil ditambahkan!")
     
        
if menu == "Daftarkan Mobil Baru":
    st.header("Daftarkan Mobil Baru")
    id_mobil = st.text_input("ID Mobil")
    merk = st.text_input("Merk Mobil")
    model = st.text_input("Model Mobil")
    tahun = st.number_input("Tahun", min_value=1900, max_value=2100, step=1)
    plat_nomor = st.text_input("Plat Nomor")
    harga_sewa = st.number_input("Harga Sewa per Hari", min_value=0, step=1)
    status = st.selectbox("Status Mobil", ["Tersedia", "Disewa"])

    if st.button("Simpan Mobil"):
        new_mobil = pd.DataFrame({
            'ID_Mobil': [id_mobil],
            'Merk': [merk],
            'Model': [model],
            'Tahun': [tahun],
            'Plat_Nomor': [plat_nomor],
            'Harga_Sewa': [harga_sewa],
            'Status': [status]
        })
        global mobil_data
        mobil_data = pd.concat([mobil_data, new_mobil], ignore_index=True)
        st.success("Mobil berhasil ditambahkan!")

if menu == "Tampilkan Tabel Mobil":
    st.header("Tabel Mobil")
    st.write(mobil_data)

if menu == "Tampilkan Tabel Pelanggan":
    st.header("Tabel Pelanggan")
    st.write(penyewa_data)

if menu == "Selesaikan Pesanan":
    st.header("Selesaikan Pesanan")
    pesanan_id = st.text_input("Masukkan ID Pesanan")

    if st.button("Selesaikan Pesanan"):
        st.success(f"Pesanan dengan ID {pesanan_id} telah diselesaikan.")

if menu == "Cari Data Pelanggan":
    st.header("Cari Data Pelanggan")
    keyword = st.text_input("Masukkan Nama atau No Telepon")

    if st.button("Cari"):
        hasil = penyewa_data[penyewa_data.apply(lambda row: keyword.lower() in row.astype(str).str.lower().to_string(), axis=1)]
        st.write(hasil)

if menu == "Cari Data Mobil":
    st.header("Cari Data Mobil")
    keyword = st.text_input("Masukkan Merk, Model, atau Plat Nomor")

    if st.button("Cari"):
        hasil = mobil_data[mobil_data.apply(lambda row: keyword.lower() in row.astype(str).str.lower().to_string(), axis=1)]
        st.write(hasil)
