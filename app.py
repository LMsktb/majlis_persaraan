import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
import random

# 1. Konfigurasi Halaman & CSS Estetik
st.set_page_config(page_title="Laman Kenangan Cikgu Nordin", page_icon="🌸", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');
    
    .stApp { 
        background: linear-gradient(135deg, #FFEBEE 0%, #E3F2FD 33%, #E8F5E9 66%, #F3E5F5 100%); 
        overflow-x: hidden;
    }

    /* Pokok Sakura di Setiap 4 Sudut */
    .pokok {
        position: fixed;
        font-size: 180px;
        opacity: 0.12;
        z-index: 0;
        pointer-events: none;
    }
    .kiri-atas { top: -40px; left: -60px; transform: rotate(-15deg); }
    .kanan-atas { top: -40px; right: -60px; transform: rotate(15deg); }
    .kiri-bawah { bottom: -60px; left: -60px; transform: rotate(15deg); }
    .kanan-bawah { bottom: -60px; right: -60px; transform: rotate(-15deg); }
    
    /* Tajuk Gergasi */
    .tajuk-gergasi {
        font-family: 'Great Vibes', cursive;
        color: #4A4A4A;
        font-size: 110px !important;
        line-height: 0.9;
        margin-bottom: 5px;
        text-shadow: 2px 2px 8px rgba(255,183,197,0.6);
    }

    /* Animasi Kelopak Sakura */
    .sakura { 
        position: fixed; top: -10%; background-color: #ffb7c5; border-radius: 100% 0 100% 0; 
        z-index: 999; pointer-events: none; animation: fall linear infinite; 
    }
    @keyframes fall { 0% { transform: translateY(0vh) rotate(0deg); } 100% { transform: translateY(110vh) rotate(360deg); } }
    .s1 { left: 10%; width: 14px; height: 14px; animation-duration: 7s; }
    .s2 { left: 50%; width: 10px; height: 10px; animation-duration: 10s; }
    .s3 { left: 85%; width: 16px; height: 16px; animation-duration: 12s; }

    /* Butang Titip Ucapan & Arahan */
    .btn-container {
        text-align: center;
        margin-bottom: 40px;
    }
    .custom-btn {
        background: linear-gradient(to right, #F8BBD0, #D1C4E9) !important;
        color: #4A4A4A !important;
        padding: 12px 40px;
        border-radius: 50px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-family: 'Great Vibes', cursive !important;
        font-size: 38px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid white;
        transition: 0.3s;
    }
    .custom-btn:hover { transform: scale(1.05); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }

    /* Kotak Ucapan Rawak (Masonry) */
    .box-ucapan {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #F8BBD0;
        box-shadow: 2px 4px 12px rgba(0,0,0,0.05);
        backdrop-filter: blur(5px);
    }
    </style>

    <div class="pokok kiri-atas">🌸</div>
    <div class="pokok kanan-atas">🌸</div>
    <div class="pokok kiri-bawah">🌸</div>
    <div class="pokok kanan-bawah">🌸</div>

    <div class="sakura s1"></div><div class="sakura s2"></div><div class="sakura s3"></div>
    """, unsafe_allow_html=True)

# 2. Header: Tajuk (Kiri) & Gambar (Kanan)
col_h1, col_h2 = st.columns([2, 1])

with col_h1:
    st.markdown('<p class="tajuk-gergasi">Selaut Budi<br>Seribu Memori</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:24px; font-weight:bold; color:#FF1493; margin-top:10px;">Laman Kenangan Persaraan Cikgu Nordin Bin Yasir</p>', unsafe_allow_html=True)
    
    # 3. Butang Arahan & Titip Ucapan (Di bawah Laman Kenangan)
    st.markdown('<p style="color:#D81B60; font-weight:bold; font-size:16px; margin-top:20px;">( KLIK BUTANG DI BAWAH UNTUK KEHADIRAN )</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <a href="https://forms.gle/A9A6GyfFFTM1gPb29" target="_blank" style="text-decoration: none;">
            <div class="custom-btn">🌸 Titip Ucapan 🌸</div>
        </a>
        """, unsafe_allow_html=True)

with col_h2:
    try:
        # Imej Cikgu Nordin (Pastikan fail cikgu_nordin.png ada di GitHub)
        st.image("cikgu_nordin.png", width=300)
    except:
        st.write("📸 *Ruang Gambar Cikgu*")

st.markdown("<br><hr>", unsafe_allow_html=True)

# 4. Dinding Ucapan (Grid 3-Kolum Rawak)
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(ttl=0)
    if not df.empty:
        # Gunakan 3 column untuk nampak rawak dan cantik di laptop
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        # Ucapan terbaru di atas
        for index, row in df.iloc[::-1].iterrows():
            # Masukkan ke column secara bergilir/rawak
            target_col = cols[index % 3]
            with target_col:
                st.markdown(f"""
                    <div class="box-ucapan">
                        <strong style="font-size: 19px; color: #D81B60;">{row.iloc[1]}</strong><br>
                        <small style="color: #880E4F;">{row.iloc[2]}</small>
                        <hr style="margin: 10px 0; border: 0.5px solid #F8BBD0;">
                        <p style="color: #4A4A4A; font-style: italic; font-size: 17px; line-height: 1.5;">
                            "{row.iloc[3]}"
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Menunggu ucapan pertama daripada tetamu...")
except Exception as e:
    st.error("Sila semak sambungan Google Sheets.")

# 5. Auto-refresh
time.sleep(10)
st.rerun()
