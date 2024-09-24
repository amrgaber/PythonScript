"""
Extract Location into multi columns  , extract string with comma into multiple columns
- BUG : we need to have all locations in first row
"""
from bs4 import BeautifulSoup
from html_element import HtmlElement

EXCEL_LIST_LOCATION = [f'location{i}' for i in range(1, 4)]
EXCEL_LIST = ['city', 'state', 'area']
EXCEL_LIST.extend(EXCEL_LIST_LOCATION)

class Location(HtmlElement):

    def __init__(self, soup, tag):
        super().__init__(soup)
        self.tag = tag
        self.div = self.get_div_with_class()

    def get_div_with_class(self):
        return self.soup.find(self.tag, {'class': 'styles_desktop_content__jJfjX'})

    def _extract_and_split_area(self):
        district_element = self.div.find('p', {'class': 'styles_desktop_subtitle__ZxS1V'})
        area = {'area': ""}
        if district_element:
            area = {
                'area': district_element.text or "",
            }
        return area

    def _extract_and_split_full_location(self):
        location_element = self.div.find('p', {'class': 'styles_desktop_full-name__44zGs'})
        location_parts = location_element.text.split(',') if location_element else []
        location_dict = {}
        for i, location in enumerate(location_parts):
            if i == 0:
                location_dict['city'] = location.strip()
            elif i == 1:
                location_dict['state'] = location.strip() if location else None
            else:
                location_dict[f'location{i-1}'] = location.strip() if location else None

        return location_dict

    def get_location(self):
        if self.div:
            return {**self._extract_and_split_area(), **self._extract_and_split_full_location()}
        else:
            return []