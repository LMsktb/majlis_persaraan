import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# 1. Setting Page & Tab
st.set_page_config(page_title="Selaut Budi Seribu Memori", page_icon="🌸", layout="centered")

# 2. CSS: Warna Pastel Lembut & Gaya Tulisan
st.markdown("""
    <style>
    /* Background Pastel Lembut */
    .stApp {
        background: linear-gradient(135deg, #FFEBEE 0%, #E3F2FD 33%, #E8F5E9 66%, #F3E5F5 100%);
    }

    /* Tajuk Majlis */
    .tajuk-utama {
        font-family: 'Georgia', serif;
        color: #4A4A4A;
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        padding-top: 10px;
        margin-bottom: 0px;
    }

    .sub-tajuk {
        text-align: center;
        color: #6D6D6D;
        font-size: 18px;
        margin-top: -10px;
        font-style: italic;
    }

    /* Kotak Borang & Kad Ucapan */
    div[data-testid="stForm"], .card-ucapan {
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 20px;
        border: none;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 15px;
    }

    /* Butang Hantar */
    .stButton>button {
        background-color: #FFCDD2 !important;
        color: #4A4A4A !important;
        border-radius: 12px !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown('<p class="tajuk-utama">Selaut Budi Seribu Memori</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-tajuk">Laman Kenangan Persaraan Cikgu</p>', unsafe_allow_html=True)

# 4. Sambungan ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 5. Borang Kehadiran (Bahagian Atas)
with st.form("borang_utama", clear_on_submit=True):
    st.markdown("<h4 style='text-align: center; color: #4A4A4A;'>🌷 Isi Kehadiran & Ucapan</h4>", unsafe_allow_html=True)
    nama = st.text_input("Nama Penuh")
    sekolah = st.text_input("Sekolah / Unit")
    ucapan = st.text_area("Ucapan Ringkas")
    submit = st.form_submit_button("Hantar Ucapan 🌸")

if submit:
    if nama and sekolah and ucapan:
        try:
            # Baca data sedia ada
            df = conn.read()
            # Tambah baris baru
            new_data = pd.DataFrame([{"Nama": nama, "Sekolah": sekolah, "Ucapan": ucapan}])
            updated_df = pd.concat([df, new_data], ignore_index=True)
            # Update Google Sheets
            conn.update(data=updated_df)
            
            st.balloons()
            st.success("Ucapan Moon telah selamat dihantar!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error("Gagal menyambung ke Google Sheets. Sila semak fail secrets.toml anda.")
    else:
        st.warning("Moon, sila isi semua ruangan ya!")

st.write("---")

# 6. Dinding Ucapan Live (Bahagian Bawah)
st.markdown("<h3 style='text-align: center; color: #4A4A4A;'>✨ Dinding Memori ✨</h3>", unsafe_allow_html=True)

# Fungsi untuk paparkan ucapan secara automatik
try:
    df_live = conn.read()
    if not df_live.empty:
        # Papar ucapan terbaru di atas (reverse order)
        for index, row in df_live.iloc[::-1].iterrows():
            st.markdown(f"""
                <div class="card-ucapan">
                    <strong style="color: #FF8AAB;">{row['Nama']}</strong> <small>({row['Sekolah']})</small><br>
                    <p style="margin-top: 8px; color: #4A4A4A;">"{row['Ucapan']}"</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Menunggu ucapan pertama masuk...")
except:
    st.write("Sila pastikan Google Sheet anda sudah sedia.")

# Kod Auto-Refresh (Halaman akan segar semula setiap 30 saat untuk tarik ucapan baru)
time.sleep(30)
st.rerun()
