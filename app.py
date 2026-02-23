import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# 1. Setting Page
st.set_page_config(page_title="Selaut Budi Seribu Memori", page_icon="🌸", layout="centered")

# 2. CSS: Sakura Falling, Background Pastel, & Soft Purple Boxes
st.markdown("""
    <style>
    /* Background Pastel */
    .stApp {
        background: linear-gradient(135deg, #FFEBEE 0%, #E3F2FD 33%, #E8F5E9 66%, #F3E5F5 100%);
        overflow: hidden;
    }

    /* Animasi Sakura Jatuh */
    .sakura {
        position: absolute;
        background-color: #ffb7c5;
        border-radius: 100% 0 100% 0;
        opacity: 0.7;
        pointer-events: none;
        animation: fall linear infinite;
    }

    @keyframes fall {
        0% { transform: translateY(-10vh) rotate(0deg); }
        100% { transform: translateY(110vh) rotate(360deg); }
    }

    /* Tajuk Majlis */
    .tajuk-utama {
        font-family: 'Georgia', serif;
        color: #4A4A4A;
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 0px;
    }

    .sub-tajuk {
        text-align: center;
        color: #6D6D6D;
        font-size: 18px;
        margin-top: -10px;
        font-style: italic;
    }

    /* Kotak Borang & Kad Ucapan (Soft Purple) */
    div[data-testid="stForm"], .card-ucapan {
        background-color: rgba(235, 209, 255, 0.6) !important; /* Ungu Lembut Lutsinar */
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        margin-bottom: 15px;
    }

    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 10px !important;
    }

    /* Butang Hantar */
    .stButton>button {
        background-color: #D1C4E9 !important; /* Ungu Pastel */
        color: #4A4A4A !important;
        border-radius: 12px !important;
        width: 100%;
        border: none !important;
        font-weight: bold;
    }
    </style>
    
    <script>
    function createSakura() {
        const sakura = document.createElement('div');
        sakura.classList.add('sakura');
        sakura.style.left = Math.random() * 100 + 'vw';
        sakura.style.width = Math.random() * 10 + 5 + 'px';
        sakura.style.height = sakura.style.width;
        sakura.style.animationDuration = Math.random() * 3 + 7 + 's';
        document.body.appendChild(sakura);
        setTimeout(() => { sakura.remove(); }, 10000);
    }
    setInterval(createSakura, 300);
    </script>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown('<p class="tajuk-utama">Selaut Budi Seribu Memori</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-tajuk">Laman Kenangan Persaraan Cikgu</p>', unsafe_allow_html=True)

# 4. Sambungan ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 5. Borang Kehadiran
with st.form("borang_utama", clear_on_submit=True):
    st.markdown("<h4 style='text-align: center; color: #4A4A4A;'>🌸 Isi Kehadiran & Ucapan</h4>", unsafe_allow_html=True)
    nama = st.text_input("Nama Penuh")
    sekolah = st.text_input("Sekolah / Unit")
    ucapan = st.text_area("Ucapan Ringkas")
    submit = st.form_submit_button("Hantar Ucapan 🌸")

if submit:
    if nama and sekolah and ucapan:
        try:
            df = conn.read()
            new_data = pd.DataFrame([{"Nama": nama, "Sekolah": sekolah, "Ucapan": ucapan}])
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(data=updated_df)
            st.balloons()
            st.success("Ucapan telah selamat dihantar!")
            time.sleep(1)
            st.rerun()
        except:
            st.error("Sila semak sambungan Google Sheets anda.")
    else:
        st.warning("Sila isi semua ruangan.")

st.write("---")

# 6. Dinding Ucapan Live
st.markdown("<h3 style='text-align: center; color: #4A4A4A;'>✨ Dinding Memori ✨</h3>", unsafe_allow_html=True)

try:
    df_live = conn.read()
    if not df_live.empty:
        for index, row in df_live.iloc[::-1].iterrows():
            st.markdown(f"""
                <div class="card-ucapan">
                    <strong style="color: #9575CD;">{row['Nama']}</strong> <small>({row['Sekolah']})</small><br>
                    <p style="margin-top: 8px; color: #4A4A4A; font-style: italic;">"{row['Ucapan']}"</p>
                </div>
            """, unsafe_allow_html=True)
except:
    st.info("Menunggu ucapan pertama...")

# Auto-refresh
time.sleep(30)
st.rerun()
