# scraper_selenium.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


def ekstraktuj_ceny_z_html(soup):
    ceny = []
    for el in soup.find_all(string=lambda t: "zł" in t or "PLN" in t):
        ceny.append(el.strip())
    return "\n".join(ceny)





def pobierz_zawartosc_strony(url, delay=12):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("window-size=1920x1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # 🔍 Czekamy aż pojawi się przynajmniej jedna oferta
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'zł') or contains(text(), 'PLN')]")
            )
        )

        # 📜 Pobieramy pełną stronę po załadowaniu
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, "html.parser")
        tekst = soup.get_text(separator=" ", strip=True)


        ceny = ekstraktuj_ceny_z_html(soup)
        tekst += f"\n\nWydobyte ceny:\n{ceny}"




        return tekst[:10000] if tekst else ""

    except Exception as e:
        print(f"❌ Błąd Selenium przy pobieraniu {url}: {e}")
        return ""
