from cryptography.fernet import Fernet
import os
from PIL import Image
import stepic


def speichere_nachricht(verschluesselter_text):
    """Speichert die verschlüsselte Nachricht in einer Textdatei."""
    with open("verschluesselte_nachricht.txt", "wb") as f:
        if isinstance(verschluesselter_text, str):
            verschluesselter_text = verschluesselter_text.encode()
        f.write(verschluesselter_text)
    print("Nachricht wurde in 'verschluesselte_nachricht.txt' gespeichert.")

def schlussel_machen():
    key = Fernet.generate_key()
    with open("geheimer_schlussel.key", "wb") as key_file:
        key_file.write(key)

def lade_schlussel():
    if not os.path.exists("geheimer_schlussel.key"):
        schlussel_machen()
    return open("geheimer_schlussel.key", "rb").read()

def verschlusseln(text, key):
    f = Fernet(key)
    return f.encrypt(text.encode())

def entschlusseln(verschluesselter_text, key):
    f = Fernet(key)
    return f.decrypt(verschluesselter_text).decode()

def verstecke_in_bild(bildpfad, text):
    with Image.open(bildpfad) as img:
        if isinstance(text, bytes):
            text = text.decode()
        img_mit_text = stepic.encode(img, text.encode())
        img_mit_text.save("bild_mit_text.png")


def text_aus_bild_holen(bildpfad):
    with Image.open(bildpfad) as img:
        return stepic.decode(img)



while True:
    aktion = input("Verschlüsseln oder entschlüsseln? (v/e)? ")
    if aktion not in ["v","e"]:
        print("Ungültige Eingabe.")
        continue
    #verschlüsseln
    if aktion == "v":
        schluessel = input("Hast du einen eigenen Schlüssel (j/n)? ").lower()
        if schluessel not in ["j", "n"]:
            print("ungültige einageb")
            continue
        if schluessel == "j":
            ladenfrage = input("Von einer Datei laden? (j/n): ")
            if ladenfrage == "j":
                key = lade_schlussel()

            else:
                key = input("Bitte gebe deinen schlüssel ein: ").encode()


        else:
            key = lade_schlussel()
            print(f"Der Schlüssel: {key.decode()} wurde geladen.")
        
        text = input("was gibt es zum verschlüsseln? ")
        verschluesselter_text = verschlusseln(text, key)
        print(f"Verschlüsselter Text: {verschluesselter_text}")
        speichere_nachricht(verschluesselter_text)

        in_bild = input("Soll die Nachricht noch in einem Bild versteckt werden? (j/n)").lower()
        if in_bild not in ["j", "n"]:
            print("Ungültige Eingabe.")
            continue
        if in_bild == "j":
            bild_pfad = input("Was ist der Pfad zum PNG Bild? ")
            verstecke_in_bild(bild_pfad, verschluesselter_text)


    else:
        aus_bild = input("Eine Nachricht aus einem Bild extarhieren? (j/n) ")
        if aus_bild not in ["j", "n"]:
            print("Ungültige Einagbe")
        
        if aus_bild == "j":
            bild_pfad = input("Bitte den Pfad des Bildes eingeben: ")
            verschluesselter_text = text_aus_bild_holen(bild_pfad).encode()

        else:
            verschluesselter_text = input("Bitte verschlüsselten Text eingeben: ")

        schluessel = input("Schlüssel aus Datei laden? (j/n): ")
        if schluessel not in ["j", "n"]:
            print("Ungültige Einagbe")

        if schluessel == "n":
            key = input("Bitte gebe den Schlüssel ein: ")

        else:
            key = lade_schlussel()

        try:
            entschluesselter_text = entschlusseln(verschluesselter_text, key)
            print(f"Entschlüsselter Text: {entschluesselter_text}")

        except Exception as e:
            print(f"Fehler beim entschlüsseln: {e}")


    if input("Noch etwas (j/n): ").lower() != "j":
        break
