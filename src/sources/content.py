from bs4 import Tag, BeautifulSoup


class Content:
    def __init__(self, html_id: str) -> None:
        self.__html_id = html_id

    def __scrape(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_tag_list(self) -> list[Tag]:
        raise NotImplementedError("Subclasses must implement this method")

    def add_to_email(self, soup: BeautifulSoup) -> None:
        tag = soup.find("ul", id=self.__html_id)
        item_list = self.get_tag_list()
        for item in item_list:
            tag.append(item)

    def get_html_id(self) -> str:
        return self.__html_id
