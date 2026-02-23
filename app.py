import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# 1. Konfigurasi Halaman & CSS (Sakura & Tajuk Gergasi)
st.set_page_config(page_title="Selaut Budi Seribu Memori", page_icon="🌸", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');
    
    /* Latar Belakang Pastel */
    .stApp { 
        background: linear-gradient(135deg, #FFEBEE 0%, #E3F2FD 33%, #E8F5E9 66%, #F3E5F5 100%); 
        overflow-x: hidden; 
    }
    
    /* Tajuk Gergasi & Berkelip */
    .tajuk-gergasi {
        font-family: 'Great Vibes', cursive;
        color: #4A4A4A;
        text-align: center;
        font-size: 130px !important;
        line-height: 1.1;
        margin-top: 50px;
        animation: glow 3s ease-in-out infinite;
    }
    @keyframes glow { 0%, 100% { text-shadow: 0 0 10px #fff, 0 0 20px #ffb7c5; } 50% { text-shadow: 0 0 40px #ffb7c5, 0 0 60px #ff8aab; } }

    /* Animasi Sakura Pure CSS */
    .sakura { 
        position: fixed; 
        top: -10%; 
        background-color: #ffb7c5; 
        border-radius: 100% 0 100% 0; 
        z-index: 999; 
        pointer-events: none; 
        animation: fall linear infinite; 
    }
    @keyframes fall { 0% { transform: translateY(0vh) rotate(0deg); } 100% { transform: translateY(110vh) rotate(360deg); } }
    .s1 { left: 10%; width: 15px; height: 15px; animation-duration: 7s; }
    .s2 { left: 45%; width: 12px; height: 12px; animation-duration: 9s; }
    .s3 { left: 85%; width: 18px; height: 18px; animation-duration: 11s; }
    </style>
    <div class="sakura s1"></div><div class="sakura s2"></div><div class="sakura s3"></div>
    """, unsafe_allow_html=True)

st.markdown('<p class="tajuk-gergasi">Selaut Budi Seribu Memori</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:25px; font-style:italic; color:#6D6D6D;">Laman Kenangan Persaraan Cikgu</p>', unsafe_allow_html=True)

# 2. Sambungan ke Google Sheet (Read-Only)
# Pastikan secrets.toml ada link Google Sheet yang betul
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Kotak Hantar Ucapan (Guna Link Form Moon)
st.markdown(f"""
    <div style="background-color: rgba(255, 255, 255, 0.4); border-radius: 30px; padding: 40px; text-align: center; border: 2px solid white; position: relative; z-index: 5;">
        <h2 style="color: #FF1493; font-family: sans-serif;">🌷 Titipkan Ucapan 🌷</h2>
        <p style="color: #4A4A4A; font-size: 18px;">Klik butang di bawah untuk menghantar ucapan & kehadiran:</p>
        <br>
        <a href="https://forms.gle/A9A6GyfFFTM1gPb29" target="_blank">
            <button style="background-color: #D1C4E9; color: #4A4A4A; padding: 20px 40px; border-radius: 20px; border: none; font-weight: bold; font-size: 22px; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                ISI BORANG UCAPAN ✍️
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# 4. Dinding Ucapan Live (Tarik Data dari Sheet)
st.markdown("<h3 style='text-align: center; color: #FF1493;'>✨ Dinding Memori Live ✨</h3>", unsafe_allow_html=True)

try:
    # ttl=0 supaya dia tarik data paling baru setiap kali refresh
    df = conn.read(ttl=0) 
    if not df.empty:
        # Susun ikut yang terbaru (paling bawah di Sheet akan jadi paling atas di Web)
        for index, row in df.iloc[::-1].iterrows():
            # row.iloc[1], [2], [3] merujuk kepada kolum Nama, Sekolah, Ucapan
            st.markdown(f"""
                <div style="background-color: rgba(255, 255, 255, 0.4); border-radius: 25px; padding: 25px; margin-bottom: 15px; border: 1px solid white; position: relative; z-index: 5;">
                    <strong style="font-size: 22px; color: #FF1493;">{row.iloc[1]}</strong><br>
                    <small style="color: #4A4A4A;">{row.iloc[2]}</small>
                    <p style="margin-top: 10px; color: #4A4A4A; font-style: italic; font-size: 20px;">"{row.iloc[3]}"</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Menunggu ucapan pertama masuk dari Google Form...")
except Exception as e:
    st.error("Gagal menarik data. Pastikan link Google Sheet di secrets.toml adalah PUBLIC (Anyone with link can view).")

# Auto-refresh skrin setiap 10 saat
time.sleep(10)
st.rerun()
