from datetime import datetime
from bs4 import BeautifulSoup, Tag
import requests
import json


class Books:
    def __scrape_books(self) -> list[tuple[str, str, str]]:
        web_endpoint = "https://ranobedb.org"
        image_endpoint = "https://images.ranobedb.org"
        response = requests.get(f"{web_endpoint}/releases/calendar?rl=en&rf=digital")
        if not response.ok:
            return []
        books = []
        soup = BeautifulSoup(response.text, "html.parser")
        date = datetime.today().date()
        time_tags = soup.find_all("time", {"datetime": date.strftime("%Y-%m-%d")})
        for time_tag in time_tags:
            if not isinstance(time_tag, Tag):
                continue
            release_href = time_tag.find_next("a", {"class": "link"}).get("href")
            response = requests.get(f"{web_endpoint}/api/v0{release_href}")
            if not response.ok:
                continue
            release = json.loads(response.text)["release"]
            title = release["title"]
            href = f"{web_endpoint}/release/{release["id"]}"
            img = f"{image_endpoint}/{release["books"][0]["image"]["filename"]}"
            books.append((title, href, img))
        return books

    def book_tag_list(self) -> list[Tag]:
        book_list = []
        books = self.__scrape_books()
        soup = BeautifulSoup("<html></html>", "html.parser")
        for title, href, img in books:
            li_tag = soup.new_tag("li")
            title_tag = soup.new_tag("a")
            img_tag = soup.new_tag("img")
            title_tag.string = title
            title_tag.attrs["href"] = href
            title_tag.attrs["style"] = "display:block; font-size: 1.2rem;"
            img_tag.attrs["src"] = img
            li_tag.append(img_tag)
            li_tag.append(title_tag)
            li_tag.attrs["style"] = "text-align: center;"
            book_list.append(li_tag)
        return book_list
