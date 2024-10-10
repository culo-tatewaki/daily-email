from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import ssl
from bs4 import BeautifulSoup

from sources.books import Books
from sources.news import News

from sources.web_novels import WebNovels


class Email:
    def __init__(self) -> None:
        self.__content = None
        with open("email.html", "r", encoding="utf-8") as file:
            self.__content = file.read()
        self.__content = BeautifulSoup(self.__content, "html.parser")

        self.__email = MIMEMultipart()
        self.__email["From"] = os.getenv("EMAIL_SENDER")
        self.__email["To"] = os.getenv("EMAIL_RECEIVER")
        self.__email["Subject"] = "Novedades del Día"

    def generate_content(self) -> None:
        books_tag = self.__content.find("ul", id="books")
        book_list = Books().book_tag_list()
        for book_item in book_list:
            books_tag.append(book_item)

        news_tag = self.__content.find("ul", id="news")
        news_list = News().news_tag_list()
        for news_item in news_list:
            news_tag.append(news_item)

        wn_tag = self.__content.find("ul", id="wn")
        series_list = WebNovels().wns_tag_list()
        for series in series_list:
            wn_tag.append(series)

    def send_email(self) -> None:
        self.__email.attach(MIMEText(self.__content, "html"))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(self.__email["From"], os.getenv("SMTP_PASSWORD"))
            smtp.sendmail(
                self.__email["From"], self.__email["To"], self.__email.as_string()
            )

    def test_email(self) -> None:
        with open("test/test.html", "w", encoding="utf-8") as file:
            file.write(str(self.__content))
