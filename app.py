import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
import random

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Selaut Budi Seribu Memori", page_icon="🌸", layout="centered")

# 2. CSS: Sakura (Pure CSS), Tajuk Gergasi, & Box Transparent
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

    /* Background Utama */
    .stApp {
        background: linear-gradient(135deg, #FFEBEE 0%, #E3F2FD 33%, #E8F5E9 66%, #F3E5F5 100%);
        overflow: hidden;
    }

    /* TAJUK GERGASI */
    .tajuk-gergasi {
        font-family: 'Great Vibes', cursive;
        color: #4A4A4A;
        text-align: center;
        font-size: 130px !important;
        line-height: 1.1;
        margin-top: 50px;
        margin-bottom: 0px;
        animation: glow 3s ease-in-out infinite;
        position: relative;
        z-index: 10;
    }

    @keyframes glow {
        0%, 100% { text-shadow: 0 0 10px #fff, 0 0 20px #ffb7c5; }
        50% { text-shadow: 0 0 40px #ffb7c5, 0 0 60px #ff8aab; }
    }

    /* BOX TRANSPARENT (TIADA KELABU) */
    div[data-testid="stForm"], .card-ucapan {
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-radius: 30px;
        padding: 40px;
        border: 2px solid rgba(255, 255, 255, 0.7) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        position: relative;
        z-index: 5;
    }

    /* Input Fields Cerah */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.8) !important;
        color: #4A4A4A !important;
        border: 1px solid #FFB7C5 !important;
    }

    /* Label Pink Terang */
    .stTextInput label, .stTextArea label {
        color: #FF1493 !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }

    /* ANIMASI SAKURA (PURE CSS) */
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

    /* Kedudukan Sakura Berbeza-beza */
    .s1 { left: 10%; width: 15px; height: 15px; animation-duration: 7s; animation-delay: 0s; }
    .s2 { left: 25%; width: 10px; height: 10px; animation-duration: 10s; animation-delay: 2s; }
    .s3 { left: 40%; width: 20px; height: 20px; animation-duration: 8s; animation-delay: 4s; }
    .s4 { left: 55%; width: 12px; height: 12px; animation-duration: 12s; animation-delay: 1s; }
    .s5 { left: 70%; width: 18px; height: 18px; animation-duration: 9s; animation-delay: 3s; }
    .s6 { left: 85%; width: 14px; height: 14px; animation-duration: 11s; animation-delay: 5s; }
    .s7 { left: 95%; width: 16px; height: 16px; animation-duration: 7s; animation-delay: 2s; }
    </style>

    <div class="sakura s1"></div>
    <div class="sakura s2"></div>
    <div class="sakura s3"></div>
    <div class="sakura s4"></div>
    <div class="sakura s5"></div>
    <div class="sakura s6"></div>
    <div class="sakura s7"></div>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown('<p class="tajuk-gergasi">Selaut Budi Seribu Memori</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:25px; font-style:italic; color:#6D6D6D;">Laman Kenangan Persaraan Cikgu</p>', unsafe_allow_html=True)

# 4. Sambungan GSheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 5. Borang
with st.form("borang_utama", clear_on_submit=True):
    st.markdown("<h2 style='text-align: center; color: #FF1493;'>🌷 Titipkan Ucapan</h2>", unsafe_allow_html=True)
    nama = st.text_input("NAMA PENUH")
    sekolah = st.text_input("SEKOLAH / UNIT")
    ucapan = st.text_area("UCAPAN & DOA")
    submit = st.form_submit_button("Hantar Kehadiran & Ucapan 🌸")

if submit:
    if nama and sekolah and ucapan:
        try:
            df = conn.read()
            new_row = pd.DataFrame([{"NAMA": nama, "SEKOLAH": sekolah, "UCAPAN": ucapan}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.cache_data.clear()
            st.balloons()
            st.success("Ucapan berjaya dihantar!")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Isi semua ruangan ya Bubu!")

# 6. Dinding Live
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

time.sleep(30)
st.rerun()
