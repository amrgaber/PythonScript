from bs4 import BeautifulSoup
from html_element import HtmlElement


EXCEL_LIST = ['Property Type', 'Property Size',
              'Bedrooms', 'Bathrooms', 'title',
              'price', 'estimated_monthly_payment',
              'url', 'sub_title', 'description']


class Property(HtmlElement):


    def __init__(self, soup, tag):
        super().__init__(soup)
        self.tag = tag
        self.div = self.get_div_with_class()

    def get_div_with_class(self):
        return self.soup.find(self.tag, {'class': 'styles_desktop_content__jJfjX'})

    def sub_title(self, div):
        element = div.find('a', {'class': 'styles_desktop_subtitle__XntGT'})
        sub_title = {}
        if element:
            sub_title = {
                'sub_title': element.text,
            }
        return sub_title

    def get_subtitle(self):
        if self.div:
            return self.sub_title(self.div)
        else:
            return []

    def extract_content_info(self):
        title_element = self.div.find('h1', {'class': 'styles_desktop_title__QuRdg'})
        title = title_element.text if title_element else ""

        # Extract the property type, size, bedrooms, and bathrooms
        property_info = {}
        info_elements = self.div.find_all('div', {'class': 'styles_desktop_list__item__lF_Fh'})
        for element in info_elements:
            label_element = element.find('span', {'class': 'styles_desktop_list__label-text__0YJ8y'})
            value_element = element.find('p', {'class': 'styles_desktop_list__value__uIdMl'})
            if label_element and value_element:
                label = label_element.text.replace(':', '').strip()
                value = value_element.text.strip()
                property_info[label] = value

        return {'title': title, **property_info}

    def extract_property_info_price(self):
        # Extract the price
        price_element = self.div.find('p', {'class': 'styles_desktop_price__text__Eb_Ti'})
        price = price_element.text if price_element else ""

        # Extract the estimated monthly payment
        monthly_payment_element = self.div.find('a', {'data-testid': 'mortgage-estimate'})
        monthly_payment = monthly_payment_element.text if monthly_payment_element else ""

        return {'price': price, 'estimated_monthly_payment': monthly_payment}

    def extract_property_info_contact(self):
        # Extract the phone number
        phone_element = self.div.find('a', {'data-testid': 'bottom-actions-call-button'})
        phone = phone_element['href'].replace('tel:', '') if phone_element else ""

        # Extract the WhatsApp link
        whatsapp_element = self.div.find('a', {'data-testid': 'bottom-actions-whatsapp-button'})
        whatsapp = whatsapp_element['href'] if whatsapp_element else ""

        return {'phone': phone, 'whatsapp': whatsapp}

    def extract_agent_info_contact(self):
        # Find the specific div that contains the agent's information
        div = self.div.find('div', {'class': 'styles_desktop_agent__container__xqnBc'})
        if not div:
            return {}

        # Extract the agent's name and response time
        name_element = div.find('p')
        if name_element:
            name = name_element.contents[0]
            response_time = name_element.find('span').text if name_element.find('span') else ""
        else:
            name = ""
            response_time = ""

        return {'agent_name': name, 'agent_response_time': response_time}

    def extract_broker_info(self):
        div = self.div
        # Extract the broker's name
        broker_name_element = div.find('p', {'class': 'styles_desktop_broker__name__WARhz'})
        broker_name = broker_name_element.text if broker_name_element else ""

        # Extract the broker's properties
        broker_properties_element = div.find('a', {'class': 'styles_desktop_broker__link__FBuEn'})
        broker_properties = broker_properties_element.text if broker_properties_element else ""

        return {
            'broker_name': broker_name,
            'broker_properties': broker_properties
        }


    def extract_description(self):
        div = self.div
        article = div.find('article', {'data-testid': 'dynamic-sanitize-html'})
        description = article.text
        return {'description': description}


    def get_fixed_domain_data(self):
        # Get the fixed data from the page
        fixed_data = {'country': 'UAE',
                      'domain': 'propertyfinder.ae',
                      'language': 'en'
                      }
        return fixed_data

    def get_main_category(self, main_category):
        return {'Main Category': main_category}
