from html_element import HtmlElement

EXCEL_LIST = ['Broker ORN', 'Reference', 'Listed']

class PropertyReference(HtmlElement):

    def __init__(self, soup, tag):
        super().__init__(soup)
        self.tag = tag
        self.div = self.get_div_with_class()

    def get_div_with_class(self):
        return self.soup.find(self.tag, {'class': 'styles_desktop_content__jJfjX'})


    def extract_property_details(self):
        details = {}
        items = self.div.find_all('div', {'class': 'styles_desktop_item__N_U90'})
        for item in items:
            key = item.find('p').text.replace(':', '')
            value = item.find('p', {'class': 'styles_desktop_text__MmFrB'}).text
            details[key] = value
        return details