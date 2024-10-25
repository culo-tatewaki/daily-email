from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import ssl
from bs4 import BeautifulSoup

from sources.light_novels import LightNovels
from sources.animanga_news import AniMangaNews
from sources.content import Content


class Email:
    def __init__(self) -> None:
        self.__html_content = None
        with open("email.html", "r", encoding="utf-8") as file:
            self.__html_content = file.read()
        self.__html_content = BeautifulSoup(self.__html_content, "html.parser")

        self.__email = MIMEMultipart()
        self.__email["From"] = os.getenv("EMAIL_SENDER")
        self.__email["To"] = os.getenv("EMAIL_RECEIVER")
        self.__email["Subject"] = "THE Daily Email :)"

        self.__scraped_content = [
            LightNovels("light-novels"),
            AniMangaNews("animanga-news"),
        ]

    def generate_content(self) -> None:
        for item in self.__scraped_content:
            if not isinstance(item, Content):
                continue
            item.add_to_email(self.__html_content)

    def send_email(self) -> None:
        self.__email.attach(MIMEText(self.__html_content, "html"))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(self.__email["From"], os.getenv("SMTP_PASSWORD"))
            smtp.sendmail(
                self.__email["From"], self.__email["To"], self.__email.as_string()
            )

    def test_email(self) -> None:
        with open("test/test.html", "w", encoding="utf-8") as file:
            file.write(str(self.__html_content))
