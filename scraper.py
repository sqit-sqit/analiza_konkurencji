import requests
from bs4 import BeautifulSoup

def pobierz_zawartosc_strony(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # podniesie wyjątek dla błędów 4xx/5xx

        soup = BeautifulSoup(response.text, "html.parser")
        tekst = soup.get_text(separator=" ", strip=True)

        return tekst[:5000] if tekst else ""
    except requests.exceptions.RequestException as e:
        print(f"Błąd przy pobieraniu {url}: {e}")
        return ""
