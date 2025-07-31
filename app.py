import streamlit as st
from config import konkurencja_urls, obszar
from scraper_selenium import pobierz_zawartosc_strony
from analiza import analizuj_oferte
from raport import generuj_raport

st.set_page_config(page_title="Analiza konkurencji", layout="wide")
st.title("🔍 Analiza ofert konkurencyjnych hoteli")

# 📍 Obszar
st.sidebar.header("📍 Obszar analizy")
obszar = st.sidebar.text_input("Region", obszar)

# 🌐 Lista stron
st.sidebar.header("🌐 Strony konkurencji")
urls = st.sidebar.text_area("Wklej linki (po jednym w linii)", "\n".join(konkurencja_urls)).splitlines()

# ✏️ Prompt
st.sidebar.header("🧠 Prompt do analizy (zastępuje zmienne {nazwa}, {obszar}, {tekst})")
default_prompt = (
    "Przeanalizuj ofertę obiektu '{nazwa}' działającego w regionie {obszar}. "
    "Wskaż mocne i słabe strony, grupę docelową, unikalne cechy oferty, cenę jeśli występuje, "
    "oraz ogólną atrakcyjność dla klienta.\n\nTreść oferty:\n{tekst}"
)
prompt_template = st.sidebar.text_area("Prompt", value=default_prompt, height=200)

# 🔘 Start analizy
if st.button("Rozpocznij analizę"):
    analizy = {}
    with st.spinner("🔎 Analizuję strony konkurencji..."):
        for url in urls:
            if url.strip():
                st.markdown(f"#### 🌐 {url}")
                tekst = pobierz_zawartosc_strony(url, delay=10)
                st.text(tekst)
                if tekst:
                    nazwa = url.split("//")[-1].split("/")[0]
                    prompt = prompt_template.format(nazwa=nazwa, obszar=obszar, tekst=tekst)
                    analiza = analizuj_oferte(prompt)
                    analizy[nazwa] = analiza
                    st.success(f"✅ Zanalizowano {nazwa}")
                else:
                    st.error(f"❌ Nie udało się pobrać treści z {url}")
    
    if analizy:
        st.header("📊 Raport końcowy")
        raport = generuj_raport(analizy, zapis_do_pliku=True)
        st.text_area("Raport", value=raport, height=500)
        
        with open("raport_konkurencji.txt", "rb") as f:
            st.download_button("📥 Pobierz raport TXT", f, file_name="raport_konkurencji.txt")

# if st.checkbox("🔍 Pokaż surowy tekst HTML"):
#    st.text(tekst)
