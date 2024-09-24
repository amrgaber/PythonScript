from bs4 import BeautifulSoup
from html_element import HtmlElement

EXCEL_LIST = ['phone', 'whatsapp', 'agent_name', 'agent_response_time', 'broker_name', 'broker_properties']


class Agent(HtmlElement):

    def __init__(self, soup, tag):
        super().__init__(soup)
        self.tag = tag
