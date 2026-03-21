import imaplib

IMAP_SERVER = "imap.gmail.com"


def delete_emails(mail, senders=None, subject=None, delete_all=False):
    mail.select("inbox")

    if delete_all:
        print("\nSearching for ALL emails...")
        status, data = mail.search(None, "ALL")

    elif senders:
        print("\nSearching for emails from senders:", senders)
        query = " ".join([f'(FROM "{s}")' for s in senders])
        status, data = mail.search(None, query)

    elif subject:
        print(f'\nSearching for emails with subject containing: "{subject}"')
        status, data = mail.search(None, f'(SUBJECT "{subject}")')

    else:
        print("No search criteria provided.")
        return

    if status != "OK":
        print("Search failed.")
        return

    messages = data[0].split()

    if not messages:
        print("No emails found to delete.")
        return

    print(f"Found {len(messages)} emails. Deleting...")

    for msg_id in messages:
        mail.store(msg_id, "+FLAGS", "\\Deleted")

    mail.expunge()
    print("\nDone!")


def login():
    print("=== LOGIN ===")
    email_user = input("Enter Gmail address: ")
    email_pass = input("Enter Gmail App Password: ")  # Visible while typing

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(email_user, email_pass)
        print("\nLogin successful!")
        return mail
    except Exception as e:
        print("\nLogin failed!")
        print("Error:", e)
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
        delete_emails(mail, senders=[sender])

    elif choice == 2:
        senders = input("Senders (comma separated): ").replace(" ", "").split(",")
        delete_emails(mail, senders=senders)

    elif choice == 3:
        confirm = input("Are you sure? (yes/no): ").lower()
        if confirm == "yes":
            delete_emails(mail, delete_all=True)
        else:
            print("Cancelled.")

    elif choice == 4:
        subject = input("Enter subject text: ")
        delete_emails(mail, subject=subject)

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
            print("\nConnection closed.")

    if option == "2":
        print("")
        print("You can get your Google App Password here:")
        print("https://myaccount.google.com/u/2/apppasswords")
        print("")
        print("You must have 2FA enabled.")

    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
