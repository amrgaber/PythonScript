from html_element import HtmlElement

EXCEL_LIST = ['DLD Permit Number', 'QR Link']

class PermitNumber(HtmlElement):

    def __init__(self, soup, tag):
        super().__init__(soup)
        self.tag = tag
        self.div = self.get_div_with_class()

    def get_div_with_class(self):
        return self.soup.find(self.tag, {'class': 'styles_desktop_content__jJfjX'})

    def extract_permit_and_qr_link(self):
        details = {}
        title_container = self.div.find('div', {'class': 'styles_desktop_title__container__OB4lf'})
        if title_container:
            key = title_container.find('p').text.replace(':', '')
            permit_number_container = self.div.find('a', {'class': 'styles_desktop_number__LN86z'})
            if permit_number_container:
                value = permit_number_container.find('p').text
                details[key] = value

        qr_link_container = self.div.find('a', {'class': 'styles_desktop_qr__tHSp0'})
        if qr_link_container:
            details['QR Link'] = qr_link_container['href']

        return details