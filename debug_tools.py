import requests

def check_connection(url):
    print(f"\n🌐 Sprawdzam połączenie z: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"✅ Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Odpowiedź ma długość: {len(response.text)} znaków")
            print(f"🔍 Fragment treści:\n{response.text[:500]}")
        else:
            print(f"⚠️ Serwer zwrócił kod: {response.status_code}")
            print(f"🔍 Fragment odpowiedzi:\n{response.text[:500]}")
    
    except requests.exceptions.SSLError as ssl_err:
        print("❌ Błąd SSL:", ssl_err)
    
    except requests.exceptions.ConnectionError as conn_err:
        print("❌ Błąd połączenia:", conn_err)
    
    except requests.exceptions.Timeout:
        print("⏳ Timeout – serwer nie odpowiedział na czas.")
    
    except Exception as e:
        print("❌ Inny błąd:", e)
