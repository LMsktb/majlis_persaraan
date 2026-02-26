import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
import random

# 1. Konfigurasi Halaman & CSS Estetik Gergasi
st.set_page_config(page_title="Laman Kenangan Cikgu Nordin", page_icon="🌸", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');
    
    .stApp { 
        background: linear-gradient(135deg, #FFEBEE 0%, #E3F2FD 33%, #E8F5E9 66%, #F3E5F5 100%); 
        overflow-x: hidden;
    }

    /* 4 Pokok Sakura di Setiap Sudut */
    .pokok {
        position: fixed;
        font-size: 200px;
        opacity: 0.15;
        z-index: 0;
        pointer-events: none;
        user-select: none;
    }
    .kiri-atas { top: -60px; left: -80px; transform: rotate(-15deg); }
    .kanan-atas { top: -60px; right: -80px; transform: rotate(15deg); }
    .kiri-bawah { bottom: -80px; left: -80px; transform: rotate(15deg); }
    .kanan-bawah { bottom: -80px; right: -80px; transform: rotate(-15deg); }
    
    /* Tajuk Berangkai Gergasi */
    .tajuk-gergasi {
        font-family: 'Great Vibes', cursive;
        color: #4A4A4A;
        font-size: 120px !important;
        line-height: 0.9;
        margin-bottom: 10px;
        text-shadow: 3px 3px 10px rgba(255,183,197,0.7);
    }

    /* Animasi Kelopak Sakura (DIBANYAKKAN) */
    .sakura { 
        position: fixed; top: -10%; background-color: #ffb7c5; border-radius: 100% 0 100% 0; 
        z-index: 999; pointer-events: none; animation: fall linear infinite; 
    }
    @keyframes fall { 0% { transform: translateY(0vh) rotate(0deg); } 100% { transform: translateY(110vh) rotate(360deg); } }
    
    /* Variasi Kelopak */
    .s1 { left: 5%; width: 15px; height: 15px; animation-duration: 7s; }
    .s2 { left: 25%; width: 10px; height: 10px; animation-duration: 10s; }
    .s3 { left: 45%; width: 18px; height: 18px; animation-duration: 8s; }
    .s4 { left: 65%; width: 12px; height: 12px; animation-duration: 11s; }
    .s5 { left: 85%; width: 16px; height: 16px; animation-duration: 9s; }
    .s6 { left: 15%; width: 10px; height: 10px; animation-duration: 12s; }
    .s7 { left: 35%; width: 14px; height: 14px; animation-duration: 6s; }
    .s8 { left: 55%; width: 12px; height: 12px; animation-duration: 13s; }
    .s9 { left: 75%; width: 17px; height: 17px; animation-duration: 10s; }
    .s10 { left: 95%; width: 13px; height: 13px; animation-duration: 8s; }

    /* Butang Custom */
    .custom-btn {
        background: linear-gradient(to right, #F8BBD0, #D1C4E9) !important;
        color: #4A4A4A !important;
        padding: 15px 45px;
        border-radius: 50px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-family: 'Great Vibes', cursive !important;
        font-size: 40px !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        border: 2px solid white;
        transition: 0.3s;
    }
    .custom-btn:hover { transform: scale(1.05); }

    /* Kotak Ucapan */
    .box-ucapan {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 25px;
        border: 1px solid #F8BBD0;
        box-shadow: 4px 6px 15px rgba(0,0,0,0.05);
        backdrop-filter: blur(5px);
    }
    </style>

    <div class="pokok kiri-atas">🌸</div>
    <div class="pokok kanan-atas">🌸</div>
    <div class="pokok kiri-bawah">🌸</div>
    <div class="pokok kanan-bawah">🌸</div>

    <div class="sakura s1"></div><div class="sakura s2"></div><div class="sakura s3"></div>
    <div class="sakura s4"></div><div class="sakura s5"></div><div class="sakura s6"></div>
    <div class="sakura s7"></div><div class="sakura s8"></div><div class="sakura s9"></div>
    <div class="sakura s10"></div>
    """, unsafe_allow_html=True)

# 2. Header Layout (Wide)
col_h1, col_h2 = st.columns([1.5, 1])

with col_h1:
    st.markdown('<p class="tajuk-gergasi">Selaut Budi<br>Seribu Memori</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:28px; font-weight:bold; color:#FF1493;">Laman Kenangan Persaraan Cikgu Nordin Bin Yasir</p>', unsafe_allow_html=True)
    
    # 3. Arahan & Butang (Tepat di bawah Laman Kenangan)
    st.markdown('<p style="color:#D81B60; font-weight:bold; font-size:18px; margin-top:30px;">( KLIK BUTANG DI BAWAH UNTUK KEHADIRAN )</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <a href="https://forms.gle/A9A6GyfFFTM1gPb29" target="_blank" style="text-decoration: none;">
            <div class="custom-btn">🌸 Titip Ucapan 🌸</div>
        </a>
        """, unsafe_allow_html=True)

with col_h2:
    try:
        # GAMBAR BESAR: Width dinaikkan ke 450
        st.image("cikgu_nordin.png", width=450)
    except:
        st.info("Sila upload cikgu_nordin.png ke GitHub.")

st.markdown("<br><hr style='border: 1px solid #F8BBD0;'>", unsafe_allow_html=True)

# 4. Dinding Ucapan (Masonry 3-Kolum)
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(worksheet="Form Responses 1", ttl=0)
    df = df.dropna(subset=["UCAPAN"])

    if not df.empty:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]

        for index, row in df.iloc[::-1].iterrows():
            with cols[index % 3]:
                st.markdown(f"""
                    <div class="box-ucapan">
                        <strong style="font-size: 22px; color: #D81B60;">
                            {row['NAMA']}
                        </strong><br>
                        <small style="color: #880E4F; font-size: 15px;">
                            {row['SEKOLAH / UNIT']}
                        </small>
                        <hr style="margin: 12px 0; border: 0.5px solid #F8BBD0;">
                        <p style="color: #4A4A4A; font-style: italic; font-size: 19px;">
                            "{row['UCAPAN']}"
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.write("Belum ada ucapan lagi.")

except Exception as e:
    st.write("Debug:", e)   # sementara untuk tengok error sebenar

# 5. Auto-refresh
time.sleep(10)
st.rerun()
