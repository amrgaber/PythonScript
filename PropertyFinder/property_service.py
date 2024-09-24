from bs4 import BeautifulSoup
import time
from Amenity import Amenity
from location import Location
from property import Property
from url_types import BaseURL
from property_reference import PropertyReference
from permit_number import PermitNumber

class PropertyService:

    def __init__(self, driver, url_object: BaseURL):
        self.driver = driver
        self.url_object = url_object

    def fetch_property_data(self):
        listing_urls = self._get_listing_urls()
        property_lst = []
        for listing_url in listing_urls:
            property_info = self._get_property_info(listing_url)
            property_lst.append(property_info)
        return property_lst

    def get_soup(self, url):
        self.driver.get(url)
        time.sleep(3)
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def _get_listing_urls(self):
        property_urls = []
        main_category_url = self.url_object.url
        url_start_with = 'https://www.propertyfinder.ae/en/plp/'
        for i in range(1, 5):  # Loop over the first 3 pages
            full_url = f"{main_category_url}?page={i}"  # Append the page number to the URL
            soup = self.get_soup(full_url)
            # Get the first 5 property URLs from each page
            page_property_urls = [a['href'] for a in soup.find_all('a', href=True) if
                                  a['href'].startswith(url_start_with)][:5]
            property_urls.extend(page_property_urls)
        return property_urls

    def _get_property_info(self, url):
        # Get the property info from the URL and store it in the property_info dictionary
        property_info = {'url': url}
        # property_info = {}
        soup = self.get_soup(url)

        # Location
        location = Location(soup, 'div')
        location_info = location.get_location()
        property_info.update(location_info)

        # Amenity
        amenity = Amenity(soup, 'div')
        if amenity:
            amenities = amenity.get_amenities()
            property_info.update(amenities)

        # Property Reference
        property_reference = PropertyReference(soup, 'div')
        extract_property_details = property_reference.extract_property_details()
        property_info.update(extract_property_details)

        # Permit Number
        dld_permit_number = PermitNumber(soup, 'div')
        permit_number = dld_permit_number.extract_permit_and_qr_link()
        property_info.update(permit_number)

        # Property Info
        property_data = Property(soup, 'div')
        if property_data:
            domain_data = property_data.get_fixed_domain_data()
            main_category_dct = property_data.get_main_category(self.url_object.category)
            content = property_data.extract_content_info()
            subtitle = property_data.get_subtitle()
            price = property_data.extract_property_info_price()
            agent_info = property_data.extract_property_info_contact()
            agent_info_2 = property_data.extract_agent_info_contact()
            broker = property_data.extract_broker_info()
            desc = property_data.extract_description()
            property_info.update({'Created On': time.ctime(), 'Updated On': time.ctime()})
            property_info.update(domain_data)
            property_info.update(main_category_dct)
            property_info.update(content)
            property_info.update(subtitle)
            property_info.update(price)
            property_info.update(agent_info)
            property_info.update(agent_info_2)
            property_info.update(broker)
            property_info.update(desc)
        return property_info

