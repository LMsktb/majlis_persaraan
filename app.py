import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# 1. Setting Halaman
st.set_page_config(page_title="Selaut Budi Seribu Memori", page_icon="🌸", layout="centered")

# 2. CSS: Sakura, Berangkai & Glowing Title, Pink Info Text
st.markdown("""
    <style>
    /* Import Font Berangkai dari Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

    .stApp {
        background: linear-gradient(135deg, #FFEBEE 0%, #E3F2FD 33%, #E8F5E9 66%, #F3E5F5 100%);
        overflow-x: hidden;
    }

    /* Tajuk Berangkai, Besar & Berkelip Perlahan */
    .tajuk-utama {
        font-family: 'Great Vibes', cursive;
        color: #4A4A4A;
        text-align: center;
        font-size: 85px; /* Saiz font lebih besar */
        font-weight: normal;
        margin-bottom: 0px;
        animation: glow 3s ease-in-out infinite;
    }

    @keyframes glow {
        0%, 100% { text-shadow: 0 0 5px #fff, 0 0 10px #ffb7c5; }
        50% { text-shadow: 0 0 20px #ffb7c5, 0 0 30px #ff8aab; }
    }

    .sub-tajuk {
        text-align: center;
        color: #6D6D6D;
        font-size: 22px;
        margin-top: -15px;
        font-style: italic;
    }

    /* Warna Tulisan Maklumat (Pink Terang) */
    .stTextInput label, .stTextArea label, .card-ucapan strong, .card-ucapan p {
        color: #FF1493 !important; /* Deep Pink */
        font-weight: bold;
    }

    /* Kotak Ungu Lembut */
    div[data-testid="stForm"], .card-ucapan {
        background-color: rgba(235, 209, 255, 0.5) !important;
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Animasi Sakura */
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
    </style>
    
    <script>
    function createSakura() {
        const sakura = document.createElement('div');
        sakura.classList.add('sakura');
        sakura.style.left = Math.random() * 100 + 'vw';
        sakura.style.width = Math.random() * 10 + 8 + 'px';
        sakura.style.height = sakura.style.width;
        sakura.style.animationDuration = Math.random() * 5 + 10 + 's';
        document.body.appendChild(sakura);
        setTimeout(() => { sakura.remove(); }, 15000);
    }
    setInterval(createSakura, 400);
    </script>
    """, unsafe_allow_html=True)

# 3. Paparan Tajuk
st.markdown('<p class="tajuk-utama">Selaut Budi Seribu Memori</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-tajuk">Laman Kenangan Persaraan Cikgu</p>', unsafe_allow_html=True)

st.write("")

# 4. Sambungan Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 5. Borang Input
with st.form("borang_utama", clear_on_submit=True):
    st.markdown("<h3 style='text-align: center; color: #FF1493;'>🌷 Titipkan Ucapan</h3>", unsafe_allow_html=True)
    nama_input = st.text_input("NAMA PENUH")
    sekolah_input = st.text_input("SEKOLAH / UNIT")
    ucapan_input = st.text_area("UCAPAN & DOA")
    
    submit = st.form_submit_button("Hantar Kehadiran & Ucapan 🌸")

if submit:
    if nama_input and sekolah_input and ucapan_input:
        try:
            df = conn.read()
            # Gunakan huruf besar NAMA, SEKOLAH, UCAPAN ikut gambar Sheets Bubu
            new_row = pd.DataFrame([{"NAMA": nama_input, "SEKOLAH": sekolah_input, "UCAPAN": ucapan_input}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.cache_data.clear() 
            st.balloons()
            st.success("Ucapan berjaya disimpan!")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Sila isi semua maklumat ya Bubu.")

st.write("---")

# 6. Dinding Memori Live
st.markdown("<h3 style='text-align: center; color: #FF1493;'>✨ Dinding Memori Live ✨</h3>", unsafe_allow_html=True)

try:
    data_live = conn.read()
    if not data_live.empty:
        for index, row in data_live.iloc[::-1].iterrows():
            st.markdown(f"""
                <div class="card-ucapan">
                    <strong style="font-size: 18px;">{row['NAMA']}</strong><br>
                    <small style="color: #4A4A4A;">{row['SEKOLAH']}</small>
                    <p style="margin-top: 10px; font-style: italic;">"{row['UCAPAN']}"</p>
                </div>
            """, unsafe_allow_html=True)
except:
    st.info("Menunggu ucapan pertama...")

time.sleep(30)
st.rerun()
