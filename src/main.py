# from dotenv import load_dotenv
from mail import Email


def main():
    # load_dotenv()
    email = Email()
    email.generate_content()
    email.send_email()
    # email.test_email()


if __name__ == "__main__":
    main()
