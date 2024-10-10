from datetime import datetime, timedelta
from bs4 import BeautifulSoup, Tag
import requests
import re


class WebNovels:
    def __scrape_shuukura_chapters(self) -> tuple[str, str, list[tuple[str, str]]]:
        series_title = "Shuukura"
        web_endpoint = "https://amawashigroup.wordpress.com/story-about-buying-my-classmate-once-a-week/"
        response = requests.get(web_endpoint)
        if not response.ok:
            return []
        chapters = []
        soup = BeautifulSoup(response.text, "html.parser")
        date = (datetime.today() - timedelta(1)).date().strftime("%Y/%m/%d")
        chapter_tags = soup.find_all("a", {"href": re.compile(date)})
        for chapter_tag in chapter_tags:
            if not isinstance(chapter_tag, Tag):
                continue
            title = chapter_tag.text
            href = chapter_tag.get("href")
            img = soup.find("img").get("src")
            chapters.append((title, href))
        return (series_title, img, chapters)

    def __scrape_chapters(self) -> list[tuple[str, str, list[tuple[str, str]]]]:
        chapters = []
        chapters.append(self.__scrape_shuukura_chapters())
        return chapters

    def wns_tag_list(self) -> list[Tag]:
        wn_list = []
        series_chapters = self.__scrape_chapters()
        soup = BeautifulSoup("<html></html>", "html.parser")
        for series_title, img, chapters in series_chapters:
            series_li_tag = soup.new_tag("li")
            series_title_tag = soup.new_tag("div")
            series_img_tag = soup.new_tag("img")
            series_title_tag.string = series_title
            series_title_tag.attrs["style"] = "font-size:1.4rem;"
            series_img_tag.attrs["src"] = img
            series_img_tag.attrs["style"] = "width:100%"
            series_li_tag.append(series_img_tag)
            series_li_tag.append(series_title_tag)
            for title, href in chapters:
                chapter_tag = soup.new_tag("a")
                chapter_tag.string = title
                chapter_tag.attrs["href"] = href
                chapter_tag.attrs["style"] = (
                    "display:block;margin-left:1rem;font-size:1.2rem"
                )
                series_li_tag.append(chapter_tag)
        series_li_tag.attrs["style"] = "text-align:center;"
        wn_list.append(series_li_tag)
        return wn_list
