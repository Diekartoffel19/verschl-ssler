from cryptography.fernet import Fernet
import os

def schlussel_machen():
    key = Fernet.generate_key()
    with open("geheimer_schlussel.key", "wb") as key_file:
        key_file.write(key)

def lade_schlussel():
    if not os.path.exists("geheimer_schlussel.key"):
        schlussel_machen()
    return open("geheimer_schlussel.key", "rb").read()

def verschlusseln(nachricht_zu_verschlusseln, key):
    byte_nachricht = nachricht_zu_verschlusseln.encode()
    f = Fernet(key)
    verschlusselte_nacricht = f.encrypt(byte_nachricht)
    return verschlusselte_nacricht

def schreibe_in_datei(dateiname, text, key):
    with open(dateiname, "w", encoding="utf-8") as f:
        f.write(f"{text}\n")

def nachricht_entschlusseln(verschlusselte_nachricht, key):
    f = Fernet(key)
    entschlusselte_nachricht = f.decrypt(verschlusselte_nachricht)
    return entschlusselte_nachricht.decode()

def wenn_kein_schlussel_verschlusseln():
    schlussel_machen()
    schlussel = lade_schlussel()
    text_zu_verschluesseln = input("Was möchtest du verschlüsseln? ")
    verschluesselter_text = verschlusseln(text_zu_verschluesseln, schlussel)
    print(verschluesselter_text)
    print(f"key: {schlussel}")
    schreibe_in_datei("output.txt", str(verschluesselter_text), schlussel)

def wenn_schlussel_da_verschlusseln():
    schlussel = input("bitte gebe den schlüssel ein: ").encode()
    text_zu_kodieren = input("Was möchtest du kodieren? ")
    verschluesselter_text = verschlusseln(text_zu_kodieren, schlussel)
    print(verschluesselter_text)
    schreibe_in_datei("output.txt", str(verschluesselter_text), schlussel)

print("________________________________")
print("Wilkommen zum text verschlüssler")
print("________________________________")

while True:
    while True:
        eingabe = input("Möchtest du eine Nachricht ver- oder entschlüsseln? (v/e): ").lower()
        if eingabe in ("v", "e"):
            break
        else:
            print("Ungültige Eingabe! Bitte nur 'v' oder 'e' eingeben.")

    if eingabe == "v":
        while True:
                mit_ohne_key = input("Hast du einen Schlüssel? (j/n): ").lower()
                if mit_ohne_key not in ("j", "n"):
                    print("Ungültige Eingabe! Bitte nur 'j' oder 'n' eingeben.")
                elif mit_ohne_key == "j":
                    quelle = input("Möchtest du den Schlüssel aus einer Datei laden? (j/n): ").lower()
                    if quelle == "j":
                        schlussel = lade_schlussel()
                    else:
                        schlussel = input("Bitte gebe den Schlüssel ein: ").encode()
                    text_zu_kodieren = input("Was möchtest du kodieren? ")
                    verschlüsselter_text = verschlusseln(text_zu_kodieren, schlussel)
                    print(verschlüsselter_text)
                    # Schreibe das Ergebnis als String in eine Datei
                    schreibe_in_datei("output.txt", str(verschlüsselter_text), schlussel)
                    break
                elif mit_ohne_key == "n":
                    wenn_kein_schlussel_verschlusseln()
                    break # <<< MINIMALE ÄNDERUNG 1: HINZUGEFÜGT
        # <<< MINIMALE ÄNDERUNG 2: DER FOLGENDE BLOCK WURDE ENTFERNT
        # if mit_ohne_key == "j":
        #     wenn_schlussel_da_verschlusseln()
        # elif mit_ohne_key == "n":
        #     wenn_kein_schlussel_verschlusseln()

    elif eingabe == "e":
        schluessel = lade_schlussel()
        with open("output.txt", "r", encoding="utf-8") as f:
            zeilen = f.readlines()
            verschluesselt = zeilen[0].strip()

        eigene_eingabe = input("Möchtest du eigenen Schlüssel und/oder Text eingeben? (j/n): ").lower()

        if eigene_eingabe == "j":
            text_ent = input("Gib den verschlüsselten Text ein (Bytestring z.B. b'...' oder nur Inhalt, Enter für Standard): ")
            key = input("Gib den Schlüssel ein (Enter für Standard): ")
            if text_ent:
                if text_ent.startswith("b'") and text_ent.endswith("'"):
                    verschluesselt_bytes = eval(text_ent)
                else:
                    verschluesselt_bytes = text_ent.encode()
            else:
                if verschluesselt.startswith("b'") and verschluesselt.endswith("'"):
                    verschluesselt_bytes = eval(verschluesselt)
                else:
                    verschluesselt_bytes = verschluesselt.encode()
            if key:
                key_bytes = key.encode()
            else:
                key_bytes = schluessel
        else:
            if verschluesselt.startswith("b'") and verschluesselt.endswith("'"):
                verschluesselt_bytes = eval(verschluesselt)
            else:
                verschluesselt_bytes = verschluesselt.encode()
            key_bytes = schluessel

        try:
            entschluesselt = nachricht_entschlusseln(verschluesselt_bytes, key_bytes)
            print("Entschlüsselte Nachricht:", entschluesselt)
        except Exception as e:
            print("Fehler bei der Entschlüsselung:", e)

    weiter = input("Noch etwas machen? j/n ").lower()
    if weiter == "n":
        print("Programm zu Ende.")
        break