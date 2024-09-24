from bs4 import BeautifulSoup
from html_element import HtmlElement

EXCEL_LIST = ['amenities']

class Amenity(HtmlElement):


    def __init__(self, soup, tag):
        super().__init__(soup)
        self.tag = tag


    def get_div_with_class(self):
        return self.soup.find(self.tag, {'class': 'styles_container__TLFv4'})

    def extract_amenities(self, div):
        amenities = []
        amenity_elements = div.find_all('div', {'class': 'styles_amenity__c2P5u'})
        for amenity in amenity_elements:
            amenity_text = amenity.find('p', {'class': 'styles_text__IlyiW'}).text
            amenities.append(amenity_text)
        amenities = ', '.join(amenities)
        return {'amenities': amenities}

    def get_amenities(self):
        div = self.get_div_with_class()
        if div:
            return self.extract_amenities(div)
        else:
            return []