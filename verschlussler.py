from cryptography.fernet import Fernet

def schlussel_machen():
    key = Fernet.generate_key()
    with open("geheimer_schlussel.key", "wb") as key_file:
        key_file.write(key)

def lade_schlussel():
    return open("geheimer_schlussel.key", "rb").read()

def verschlusseln(nachricht_zu_verschlusseln, key):
    byte_nachricht = nachricht_zu_verschlusseln.encode() #macht alles zu bytes
    f = Fernet(key)
    verschlusselte_nacricht = f.encrypt(byte_nachricht) #verschlüsselt die nachricht wirklich mit dem key
    return verschlusselte_nacricht

# Neue Funktion: schreibt beliebigen Text in eine Datei
def schreibe_in_datei(dateiname, text, key):
    with open(dateiname, "w", encoding="utf-8") as f:
        f.write(f"Verschlüsselter Text: {text}\n")
        f.write(f"Key: {key.decode()}\n")


def nachricht_entschlusseln(verschlusselte_nachricht, key):
    f = Fernet(key)
    entschlusselte_nachricht = f.decrypt(verschlusselte_nachricht) #entschlusselt nachricht
    return entschlusselte_nachricht.decode()  #macht string


def wenn_kein_schlussel_verschlusseln():

    schlussel_machen()
    schlussel = lade_schlussel()
    text_zu_verschlüsseln = input("Was möchtest du verschlüsseln? ")
    verschlüsselter_text = verschlusseln(text_zu_verschlüsseln, schlussel)
    print(verschlüsselter_text)
    print(f"key: {schlussel}")
    # Schreibe das Ergebnis als String in eine Datei
    schreibe_in_datei("output.txt", str(verschlüsselter_text), schlussel)

def wenn_schlussel_da_verschlusseln():
    schlussel = input("bitte gebe den schlüssel ein: ").encode()
    text_zu_kodieren = input("Was möchtest du kodieren? ")
    verschlüsselter_text = verschlusseln(text_zu_kodieren, schlussel)
    print(verschlüsselter_text)
    # Schreibe das Ergebnis als String in eine Datei
    schreibe_in_datei("output.txt", str(verschlüsselter_text), schlussel)

print("________________________________")
print("Wilkommen zum text verschlüssler")
print("________________________________")




# Wiederhole die Eingabe bis sie gültig ist
while True:
    eingabe = input("Möchtest du eine Nachricht ver- oder entschlüsseln? (v/e): ")
    if eingabe in ("v", "e"):
        print("Eingabe akzeptiert.")
        break
    else:
        print("Ungültige Eingabe! Bitte nur 'v' oder 'e' eingeben.")

if eingabe == "v":
    while True:
        mit_ohne_key = input("Hast du einen Schlüssel? (j/n): ").lower()
        if mit_ohne_key in ("j", "n"):
            print("Eingabe akzeptiert.")
            break
        else:
            print("Ungültige Eingabe! Bitte nur 'j' oder 'n' eingeben.")
    if mit_ohne_key == "j":
        wenn_schlussel_da_verschlusseln()
    elif mit_ohne_key == "n":
        wenn_kein_schlussel_verschlusseln()
elif eingabe == "e":
    quelle = input("Möchtest du die Daten aus output.txt verwenden? (j/n): ").lower()
    if quelle == "j":
        try:
            with open("output.txt", "r", encoding="utf-8") as f:
                zeilen = f.readlines()
                verschluesselt = zeilen[0].split(": ", 1)[1].strip()
                key = zeilen[1].split(": ", 1)[1].strip()
            verschluesselt_bytes = eval(verschluesselt)
            key_bytes = key.encode()
            entschluesselt = nachricht_entschlusseln(verschluesselt_bytes, key_bytes)
            print("Entschlüsselte Nachricht:", entschluesselt)
        except Exception as e:
            print("Fehler beim Lesen der Datei:", e)
    else:
        text_ent = input("Was möchtest du entschlüsseln? (Bytestring z.B. b'...' oder nur Inhalt): ")
        key = input("Gib den Schlüssel ein: ")
        try:
            # Akzeptiere entweder b'...' oder nur den Inhalt
            if text_ent.startswith("b'") and text_ent.endswith("'"):
                verschluesselt_bytes = eval(text_ent)
            else:
                verschluesselt_bytes = text_ent.encode()
            key_bytes = key.encode()
            entschluesselt = nachricht_entschlusseln(verschluesselt_bytes, key_bytes)
            print("Entschlüsselte Nachricht:", entschluesselt)
        except Exception as e:
            print("Fehler bei der Entschlüsselung:", e)

