import streamlit as st
import pandas as pd
import requests

# Load dataset from GitHub URLs
mobil_url = "https://raw.githubusercontent.com/Meisterbogen21/python8/refs/heads/main/mobil_data_spesifik.csv"
penyewa_url = "https://raw.githubusercontent.com/Meisterbogen21/python8/refs/heads/main/penyewa_data_spesifik.csv"

@st.cache
def load_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_csv(url)

mobil_data = load_data(mobil_url)
penyewa_data = load_data(penyewa_url)

# Initialize Streamlit app
st.title("Sistem Pendataan Sewa Mobil")

menu = st.sidebar.selectbox("Pilih Menu", [
    "Daftarkan Pelanggan",
    "Daftarkan Mobil Baru",
    "Tampilkan Tabel Mobil",
    "Tampilkan Tabel Pelanggan",
    "Selesaikan Pesanan",
    "Cari Data Pelanggan",
    "Cari Data Mobil"
])

if menu == "Daftarkan Pelanggan":
    st.header("Daftarkan Pelanggan Baru")
    nama = st.text_input("Nama Pelanggan")
    alamat = st.text_input("Alamat")
    no_telepon = st.text_input("No Telepon")
    email = st.text_input("Email")

    if st.button("Simpan Pelanggan"):
        new_pelanggan = pd.DataFrame({
            'Nama': [nama],
            'Alamat': [alamat],
            'No Telepon': [no_telepon],
            'Email': [email]
        })
        penyewa_data = pd.concat([penyewa_data, new_pelanggan], ignore_index=True)
        st.success("Pelanggan berhasil ditambahkan!")

if menu == "Daftarkan Mobil Baru":
    st.header("Daftarkan Mobil Baru")
    merk = st.text_input("Merk Mobil")
    model = st.text_input("Model Mobil")
    plat_nomor = st.text_input("Plat Nomor")
    harga_sewa = st.number_input("Harga Sewa per Hari", min_value=0, step=1)

    if st.button("Simpan Mobil"):
        new_mobil = pd.DataFrame({
            'Merk': [merk],
            'Model': [model],
            'Plat Nomor': [plat_nomor],
            'Harga Sewa': [harga_sewa]
        })
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
