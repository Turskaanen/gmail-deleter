import imaplib

IMAP_SERVER = "imap.gmail.com"


def poista_sahkopostit(mail, lahettajat=None, otsikko=None, poista_kaikki=False):
    mail.select("inbox")

    if poista_kaikki:
        print("\nEtsitään KAIKKIA viestejä...")
        status, data = mail.search(None, "ALL")

    elif lahettajat:
        print("\nEtsitään viestejä lähettäjiltä:", lahettajat)
        query = " ".join([f'(FROM "{s}")' for s in lahettajat])
        status, data = mail.search(None, query)

    elif otsikko:
        print(f'\nEtsitään viestejä otsikolla joka sisältää: "{otsikko}"')
        status, data = mail.search(None, f'(SUBJECT "{otsikko}")')

    else:
        print("Ei hakuehtoja.")
        return

    if status != "OK":
        print("Haku epäonnistui.")
        return

    viestit = data[0].split()

    if not viestit:
        print("Ei viestejä poistettavaksi.")
        return

    print(f"Löytyi {len(viestit)} viestiä. Poistetaan...")

    for msg_id in viestit:
        mail.store(msg_id, "+FLAGS", "\\Deleted")

    mail.expunge()
    print("\nValmis!")


def login():
    print("=== LOGIN ===")
    email_user = input("Syötä Gmail-osoite: ")
    email_pass = input("Syötä Gmail App Password: ")  # NÄKYY KIRJOITTAESSA

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(email_user, email_pass)
        print("\nKirjautuminen onnistui!")
        return mail
    except Exception as e:
        print("\nKirjautuminen epäonnistui!")
        print("Virhe:", e)
        return None


def delete_menu(mail):
    print("\n=== GMAIL EMAIL DELETE TOOL ===")
    print("1. Delete emails from ONE sender")
    print("2. Delete emails from MULTIPLE senders")
    print("3. DELETE ALL EMAILS (dangerous!)")
    print("4. Delete emails by SUBJECT")

    try:
        choice = int(input("Choose number: "))
    except:
        print("Invalid choice.")
        return

    if choice == 1:
        sender = input("Sender email: ")
        poista_sahkopostit(mail, lahettajat=[sender])

    elif choice == 2:
        senders = input("Senders (comma separated): ").replace(" ", "").split(",")
        poista_sahkopostit(mail, lahettajat=senders)

    elif choice == 3:
        confirm = input("Are you sure? (yes/no): ").lower()
        if confirm == "yes":
            poista_sahkopostit(mail, poista_kaikki=True)
        else:
            print("Cancelled.")

    elif choice == 4:
        subject = input("Enter subject text: ")
        poista_sahkopostit(mail, otsikko=subject)

    else:
        print("Invalid choice.")


def main():
    print("=== MAIN MENU ===")
    print("1. Login")
    print("")
    print("2. Help")
    option = input("Choose option: ")

    if option == "1":
        mail = login()
        if mail:
            delete_menu(mail)
            mail.logout()
            print("\nYhteys suljettu.")
    
    if option == "2":
        print("")
        print("Here you can get your google app password: https://myaccount.google.com/u/2/apppasswords")
        print("")
        print("And you need have 2FA on")
    
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
