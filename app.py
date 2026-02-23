import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
import random

# 1. Konfigurasi Halaman & CSS Pokok Sakura
st.set_page_config(page_title="Laman Kenangan Cikgu Nordin", page_icon="🌸", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');
    
    .stApp { 
        background: linear-gradient(135deg, #FFEBEE 0%, #E3F2FD 33%, #E8F5E9 66%, #F3E5F5 100%); 
        overflow-x: hidden;
    }

    /* Pokok Sakura di Bucu - Visual Style */
    .pokok {
        position: fixed;
        font-size: 250px;
        opacity: 0.15;
        z-index: 0;
        pointer-events: none;
        user-select: none;
    }
    .kiri-atas { top: -50px; left: -80px; transform: rotate(-15deg); }
    .kanan-bawah { bottom: -80px; right: -80px; transform: rotate(15deg); }
    
    .tajuk-gergasi {
        font-family: 'Great Vibes', cursive;
        color: #4A4A4A;
        font-size: 100px !important;
        line-height: 1.0;
        margin-bottom: 0px;
        text-shadow: 2px 2px 10px rgba(255,183,197,0.5);
    }

    /* Animasi Kelopak Gugur */
    .sakura { 
        position: fixed; top: -10%; background-color: #ffb7c5; border-radius: 100% 0 100% 0; 
        z-index: 999; pointer-events: none; animation: fall linear infinite; 
    }
    @keyframes fall { 0% { transform: translateY(0vh) rotate(0deg); } 100% { transform: translateY(110vh) rotate(360deg); } }
    .s1 { left: 15%; width: 15px; height: 15px; animation-duration: 8s; }
    .s2 { left: 55%; width: 12px; height: 12px; animation-duration: 10s; }
    .s3 { left: 80%; width: 18px; height: 18px; animation-duration: 12s; }

    /* Butang Custom */
    .custom-btn {
        background-color: #D1C4E9 !important;
        color: #4A4A4A !important;
        padding: 15px 30px;
        border-radius: 25px;
        text-align: center;
        text-decoration: none;
        width: 100%;
        max-width: 400px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid white;
        display: block;
        margin: 10px auto;
    }
    .btn-text { font-family: 'Great Vibes', cursive !important; font-size: 30px !important; }

    /* Kotak Ucapan Rawak (Masonry Style) */
    .box-ucapan {
        background-color: #FCE4EC;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #F8BBD0;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.05);
        transition: transform 0.3s;
    }
    .box-ucapan:hover { transform: scale(1.02); }
    </style>

    <div class="pokok kiri-atas">🌸</div>
    <div class="pokok kanan-bawah">🌸</div>
    <div class="sakura s1"></div><div class="sakura s2"></div><div class="sakura s3"></div>
    """, unsafe_allow_html=True)

# 2. Header: Tajuk & Gambar Cikgu
col_h1, col_h2 = st.columns([2, 1])

with col_h1:
    st.markdown('<p class="tajuk-gergasi">Selaut Budi<br>Seribu Memori</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:26px; font-weight:bold; color:#FF1493;">Laman Kenangan Persaraan Cikgu Nordin Bin Yasir</p>', unsafe_allow_html=True)

with col_h2:
    try:
        st.image("cikgu_nordin.png", width=280)
    except:
        st.write("📸 *Imej Cikgu Nordin*")

st.markdown("---")

# 3. Kawasan Arahan & Butang
st.markdown('<p style="text-align:center; color:#FF1493; font-weight:bold; font-size:18px;">( KLIK BUTANG KEHADIRAN DI BAWAH )</p>', unsafe_allow_html=True)
st.markdown(f"""
    <a href="https://forms.gle/A9A6GyfFFTM1gPb29" target="_blank" style="text-decoration: none;">
        <div class="custom-btn">
            <span class="btn-text">🌸 Titip Ucapan 🌸</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

st.write("")

# 4. Dinding Ucapan Rawak (Random Grid)
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(ttl=0)
    if not df.empty:
        # Gunakan sistem 3 column untuk nampak rawak
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        # Susun dari yang terbaru
        for index, row in df.iloc[::-1].iterrows():
            # Pilih column secara rawak untuk setiap ucapan
            with random.choice(cols):
                st.markdown(f"""
                    <div class="box-ucapan">
                        <strong style="font-size: 20px; color: #D81B60;">{row.iloc[1]}</strong><br>
                        <small style="color: #6D6D6D;">{row.iloc[2]}</small>
                        <p style="margin-top: 10px; color: #4A4A4A; font-style: italic; font-size: 18px; line-height: 1.4;">
                            "{row.iloc[3]}"
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.write("Menunggu ucapan pertama...")
except Exception as e:
    st.error("Sila pastikan sambungan Google Sheets betul.")

# Auto-refresh (10 saat)
time.sleep(10)
st.rerun()
