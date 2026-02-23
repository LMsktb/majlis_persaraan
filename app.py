import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# 1. Setting Halaman
st.set_page_config(page_title="Selaut Budi Seribu Memori", page_icon="🌸", layout="centered")

# 2. CSS: Sakura, Tajuk Gergasi, & Transparent Boxes
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

    /* Background Utama */
    .stApp {
        background: linear-gradient(135deg, #FFEBEE 0%, #E3F2FD 33%, #E8F5E9 66%, #F3E5F5 100%);
    }

    /* Tajuk Berangkai GERGASI & Glowing */
    .tajuk-utama {
        font-family: 'Great Vibes', cursive;
        color: #4A4A4A;
        text-align: center;
        font-size: 120px; /* Saiz paling besar */
        line-height: 1.2;
        margin-bottom: 0px;
        animation: glow 3s ease-in-out infinite;
    }

    @keyframes glow {
        0%, 100% { text-shadow: 0 0 10px #fff, 0 0 20px #ffb7c5; }
        50% { text-shadow: 0 0 40px #ffb7c5, 0 0 60px #ff8aab; }
    }

    .sub-tajuk {
        text-align: center;
        color: #6D6D6D;
        font-size: 25px;
        margin-top: -20px;
        font-style: italic;
    }

    /* BUANG BOX HITAM - Buat jadi Transparent */
    div[data-testid="stForm"], .card-ucapan {
        background-color: rgba(255, 255, 255, 0.2) !important; /* Lutsinar habis */
        border-radius: 30px;
        padding: 30px;
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }

    /* Buat kotak input pun jadi cerah/lutsinar */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.6) !important;
        color: #4A4A4A !important;
        border: none !important;
    }

    /* Tulisan Label Pink Terang */
    .stTextInput label, .stTextArea label {
        color: #FF1493 !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* Animasi Sakura Jatuh */
    .sakura {
        position: fixed;
        background-color: #ffb7c5;
        border-radius: 100% 0 100% 0;
        opacity: 0.8;
        pointer-events: none;
        z-index: 9999; /* Biar dia duduk paling depan */
        animation: fall linear infinite;
    }

    @keyframes fall {
        0% { transform: translateY(-10vh) rotate(0deg); }
        100% { transform: translateY(110vh) rotate(360deg); }
    }

    /* Butang Hantar Purple */
    .stButton>button {
        background-color: #D1C4E9 !important;
        color: #4A4A4A !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
    }
    </style>
    
    <script>
    function createSakura() {
        const sakura = document.createElement('div');
        sakura.classList.add('sakura');
        sakura.style.left = Math.random() * 100 + 'vw';
        sakura.style.width = Math.random() * 15 + 10 + 'px';
        sakura.style.height = sakura.style.width;
        sakura.style.animationDuration = Math.random() * 5 + 8 + 's';
        document.body.appendChild(sakura);
        setTimeout(() => { sakura.remove(); }, 12000);
    }
    setInterval(createSakura, 300);
    </script>
    """, unsafe_allow_html=True)

# 3. Paparan Tajuk
st.markdown('<p class="tajuk-utama">Selaut Budi Seribu Memori</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-tajuk">Laman Kenangan Persaraan Cikgu</p>', unsafe_allow_html=True)

st.write("")

# 4. Sambungan GSheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 5. Borang
with st.form("borang_utama", clear_on_submit=True):
    st.markdown("<h2 style='text-align: center; color: #FF1493;'>🌷 Titipkan Ucapan</h2>", unsafe_allow_html=True)
    nama_input = st.text_input("NAMA PENUH")
    sekolah_input = st.text_input("SEKOLAH / UNIT")
    ucapan_input = st.text_area("UCAPAN & DOA")
    submit = st.form_submit_button("Hantar Kehadiran & Ucapan 🌸")

if submit:
    if nama_input and sekolah_input and ucapan_input:
        try:
            df = conn.read()
            # Gunakan NAMA, SEKOLAH, UCAPAN ikut gambar Sheets Bubu
            new_row = pd.DataFrame([{"NAMA": nama_input, "SEKOLAH": sekolah_input, "UCAPAN": ucapan_input}])
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
        st.warning("Mohon isi semua maklumat ya Bubu.")

st.write("---")

# 6. Dinding Live
st.markdown("<h3 style='text-align: center; color: #FF1493;'>✨ Dinding Memori Live ✨</h3>", unsafe_allow_html=True)

try:
    data_live = conn.read()
    if not data_live.empty:
        for index, row in data_live.iloc[::-1].iterrows():
            st.markdown(f"""
                <div class="card-ucapan">
                    <strong style="font-size: 20px; color: #FF1493;">{row['NAMA']}</strong><br>
                    <small style="color: #4A4A4A;">{row['SEKOLAH']}</small>
                    <p style="margin-top: 10px; color: #4A4A4A; font-style: italic; font-size: 18px;">"{row['UCAPAN']}"</p>
                </div>
            """, unsafe_allow_html=True)
except:
    st.info("Menunggu ucapan pertama...")

time.sleep(30)
st.rerun()
