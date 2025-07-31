# raport.py

def generuj_raport(analizy: dict, zapis_do_pliku=True):
    raport = "=== RAPORT ANALIZY KONKURENCJI ===\n\n"
    for nazwa, analiza in analizy.items():
        raport += f"--- {nazwa} ---\n{analiza}\n\n"

    if zapis_do_pliku:
        with open("raport_konkurencji.txt", "w", encoding="utf-8") as f:
            f.write(raport)

    return raport
