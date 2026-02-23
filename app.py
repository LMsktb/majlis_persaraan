import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Selaut Budi Seribu Memori", page_icon="🌸", layout="centered")

# 2. CSS: Sakura, Tajuk Gergasi, & Box Transparent
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

    .stApp {
        background: linear-gradient(135deg, #FFEBEE 0%, #E3F2FD 33%, #E8F5E9 66%, #F3E5F5 100%);
        overflow-x: hidden;
    }

    .tajuk-gergasi {
        font-family: 'Great Vibes', cursive;
        color: #4A4A4A;
        text-align: center;
        font-size: 130px !important;
        line-height: 1.1;
        margin-top: 50px;
        margin-bottom: 10px;
        animation: glow 3s ease-in-out infinite;
        position: relative;
        z-index: 10;
    }

    @keyframes glow {
        0%, 100% { text-shadow: 0 0 10px #fff, 0 0 20px #ffb7c5; }
        50% { text-shadow: 0 0 40px #ffb7c5, 0 0 60px #ff8aab; }
    }

    div[data-testid="stForm"], .card-ucapan {
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-radius: 30px;
        padding: 40px;
        border: 2px solid rgba(255, 255, 255, 0.7) !important;
        margin-bottom: 25px;
        position: relative;
        z-index: 5;
    }

    .stTextInput label, .stTextArea label {
        color: #FF1493 !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }

    /* Sakura CSS Animation */
    .sakura {
        position: fixed;
        top: -10%;
        background-color: #ffb7c5;
        border-radius: 100% 0 100% 0;
        z-index: 999;
        pointer-events: none;
        animation: fall linear infinite;
    }
    @keyframes fall {
        0% { transform: translateY(0vh) rotate(0deg); }
        100% { transform: translateY(110vh) rotate(360deg); }
    }
    .s1 { left: 10%; width: 15px; height: 15px; animation-duration: 7s; }
    .s2 { left: 30%; width: 10px; height: 10px; animation-duration: 10s; }
    .s3 { left: 50%; width: 20px; height: 20px; animation-duration: 8s; }
    .s4 { left: 70%; width: 12px; height: 12px; animation-duration: 12s; }
    .s5 { left: 90%; width: 18px; height: 18px; animation-duration: 9s; }
    </style>

    <div class="sakura s1"></div>
    <div class="sakura s2"></div>
    <div class="sakura s3"></div>
    <div class="sakura s4"></div>
    <div class="sakura s5"></div>
    """, unsafe_allow_html=True)

st.markdown('<p class="tajuk-gergasi">Selaut Budi Seribu Memori</p>', unsafe_allow_html=True)

# 3. Sambungan GSheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. Borang
with st.form("borang_utama", clear_on_submit=True):
    st.markdown("<h2 style='text-align: center; color: #FF1493;'>🌷 Titipkan Ucapan</h2>", unsafe_allow_html=True)
    nama = st.text_input("NAMA PENUH")
    sekolah = st.text_input("SEKOLAH / UNIT")
    ucapan = st.text_area("UCAPAN & DOA")
    submit = st.form_submit_button("Hantar Kehadiran & Ucapan 🌸")

if submit:
    if nama and sekolah and ucapan:
        try:
            # 1. Baca data sedia ada
            df = conn.read()
            
            # 2. Sediakan baris baru (Sesuai dengan NAMA, SEKOLAH, UCAPAN dalam Sheets Bubu)
            new_row = pd.DataFrame([{"NAMA": nama, "SEKOLAH": sekolah, "UCAPAN": ucapan}])
            
            # 3. Cantumkan data lama dan baru
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            # 4. Paksa simpan (Update)
            conn.update(data=updated_df)
            
            # 5. Clear Cache supaya data baru terus muncul
            st.cache_data.clear()
            
            st.balloons()
            st.success(f"Terima kasih {nama}! Ucapan berjaya disimpan.")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f"Gagal simpan! Pastikan Google Sheets 'Anyone with link can Edit'. Ralat: {e}")
    else:
        st.warning("Bubu, kena isi semua kotak dulu baru boleh hantar!")

# 5. Dinding Live
st.write("---")
st.markdown("<h3 style='text-align: center; color: #FF1493;'>✨ Dinding Memori Live ✨</h3>", unsafe_allow_html=True)

try:
    data_live = conn.read()
    if not data_live.empty:
        for index, row in data_live.iloc[::-1].iterrows():
            st.markdown(f"""
                <div class="card-ucapan">
                    <strong style="font-size: 22px; color: #FF1493;">{row['NAMA']}</strong><br>
                    <small style="color: #4A4A4A;">{row['SEKOLAH']}</small>
                    <p style="margin-top: 10px; color: #4A4A4A; font-style: italic; font-size: 20px;">"{row['UCAPAN']}"</p>
                </div>
            """, unsafe_allow_html=True)
except:
    st.info("Menunggu ucapan pertama...")

# Auto-refresh
time.sleep(30)
st.rerun()
