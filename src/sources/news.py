from datetime import datetime, timedelta
from bs4 import BeautifulSoup, Tag
import requests


class News:
    def __scrape_news(self) -> list[tuple[str, str, str, str]]:
        url = "https://www.animenewsnetwork.com"
        response = requests.get(url)
        if not response.ok:
            return []
        news = []
        soup = BeautifulSoup(response.text, "html.parser")
        date = (datetime.today() - timedelta(1)).date()
        news_list = soup.find("div", {"data-day": date.strftime("%Y-%m-%d")})
        topic_tags = news_list.find_all("span", class_="topics")
        for topic_tag in topic_tags:
            if not isinstance(topic_tag, Tag):
                continue
            categories = topic_tag.find_previous("div", class_="category").attrs[
                "class"
            ]
            is_news = False
            i = 0
            while i < len(categories) and not is_news:
                is_news = categories[i] == "news"
                i += 1
            is_manga = topic_tag.find("a", topic="manga")
            is_novel = topic_tag.find("a", topic="novels")
            if (is_manga or is_novel) and is_news:
                title_tag = topic_tag.find_previous("h3")
                title = title_tag.text
                href = f"{url}{title_tag.find_next("a")["href"]}"
                img_tag = topic_tag.find_previous("div", {"data-src": True})
                img = f"{url}{img_tag.attrs["data-src"]}"
                content = topic_tag.find_next("div").text
                news.append((title, content, href, img))
        return news

    def news_tag_list(self) -> list[Tag]:
        news_list = []
        news = self.__scrape_news()
        soup = BeautifulSoup("<html></html>", "html.parser")
        for title, content, href, img in news:
            li_tag = soup.new_tag("li")
            title_tag = soup.new_tag("a")
            content_tag = soup.new_tag("p")
            img_tag = soup.new_tag("img")
            title_tag.string = title
            title_tag.attrs["href"] = href
            title_tag.attrs["style"] = "font-size: 1.2rem;"
            content_tag.string = content
            img_tag.attrs["src"] = img
            li_tag.append(img_tag)
            li_tag.append(title_tag)
            li_tag.append(content_tag)
            news_list.append(li_tag)
        return news_list
