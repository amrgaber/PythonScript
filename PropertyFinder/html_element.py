from bs4 import BeautifulSoup
from abc import ABC

class HtmlElement(ABC):
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
