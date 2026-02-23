import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# 1. Konfigurasi Halaman & CSS
st.set_page_config(page_title="Laman Kenangan Cikgu Nordin", page_icon="🌸", layout="centered")

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
        font-size: 110px !important;
        line-height: 1.1;
        margin-top: 50px;
        animation: glow 3s ease-in-out infinite;
    }
    @keyframes glow { 0%, 100% { text-shadow: 0 0 10px #fff, 0 0 20px #ffb7c5; } 50% { text-shadow: 0 0 40px #ffb7c5, 0 0 60px #ff8aab; } }

    /* Styling Butang Yang Seragam & Panjang */
    .btn-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 15px;
        margin-top: 20px;
    }

    .custom-btn {
        background-color: #D1C4E9 !important;
        color: #4A4A4A !important;
        padding: 15px 30px;
        border-radius: 20px;
        text-align: center;
        text-decoration: none;
        width: 100%;
        max-width: 500px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid white;
        cursor: pointer;
        display: block;
    }

    .btn-text {
        font-family: 'Great Vibes', cursive !important;
        font-size: 35px !important;
    }

    /* Sakura Animation */
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
    
    .stExpander {
        border: none !important;
        background: transparent !important;
    }
    </style>
    <div class="sakura s1"></div><div class="sakura s2"></div><div class="sakura s3"></div>
    """, unsafe_allow_html=True)

# Tajuk Besar
st.markdown('<p class="tajuk-gergasi">Selaut Budi Seribu Memori</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:28px; font-weight:bold; color:#FF1493;">Laman Kenangan Persaraan Cikgu Nordin Bin Yasir</p>', unsafe_allow_html=True)

# 2. Sambungan ke Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Ayat Arahan & Susunan Butang
st.markdown('<div class="btn-container">', unsafe_allow_html=True)
st.markdown('<p style="color: #FF1493; font-size: 20px; font-weight: bold; text-align: center; margin-bottom: -5px;">( KLIK BUTANG KEHADIRAN DI BAWAH )</p>', unsafe_allow_html=True)

# Butang Atas: Titip Ucapan
st.markdown(f"""
    <a href="https://forms.gle/A9A6GyfFFTM1gPb29" target="_blank" style="text-decoration: none; width: 100%; display: flex; justify-content: center;">
        <div class="custom-btn">
            <span class="btn-text">🌸 Titip Ucapan 🌸</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

# Butang Bawah: Papar Ucapan
with st.container():
    col1, col2, col3 = st.columns([1, 4, 1]) 
    with col2:
        with st.expander("🌸 Papar Ucapan 🌸"):
            try:
                df = conn.read(ttl=0)
                if not df.empty:
                    for index, row in df.iloc[::-1].iterrows():
                        # Saiz box ucapan dikecilkan sikit (Compact)
                        st.markdown(f"""
                            <div style="background-color: #FCE4EC; border-radius: 15px; padding: 12px 18px; margin-bottom: 10px; border: 1px solid #F8BBD0;">
                                <strong style="font-size: 18px; color: #D81B60;">{row.iloc[1]}</strong>
                                <span style="color: #6D6D6D; font-size: 14px; margin-left: 8px;">({row.iloc[2]})</span>
                                <p style="margin-top: 5px; color: #4A4A4A; font-style: italic; font-size: 17px; line-height: 1.4;">"{row.iloc[3]}"</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("Belum ada ucapan lagi.")
            except Exception as e:
                st.error("Gagal menarik data.")

st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh setiap 10 saat
time.sleep(10)
st.rerun()
