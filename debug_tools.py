import streamlit as st
import requests

def check_connection(url):
    st.markdown(f"### 🌐 Sprawdzanie połączenia z `{url}`")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        st.success(f"✅ Status HTTP: {response.status_code}")

        if response.status_code == 200:
            st.info(f"✅ Odpowiedź ma długość: {len(response.text)} znaków")
            st.code(response.text[:500], language="html")
        else:
            st.warning(f"⚠️ Serwer zwrócił kod: {response.status_code}")
            st.code(response.text[:500], language="html")
    
    except requests.exceptions.SSLError as ssl_err:
        st.error(f"❌ Błąd SSL: {ssl_err}")
    
    except requests.exceptions.ConnectionError as conn_err:
        st.error(f"❌ Błąd połączenia: {conn_err}")
    
    except requests.exceptions.Timeout:
        st.error("⏳ Timeout – serwer nie odpowiedział na czas.")
    
    except Exception as e:
        st.error(f"❌ Inny błąd: {e}")
