from selenium import webdriver
# from scraper import get_listing_urls,  extract_property_info
from WebDriverConfig import WebDriverConfig
from property_service import PropertyService
from url_types import BuyURL,RentURL,CommercialRentURL
from pyexcel_ods3 import save_data
from helpers import prepare_data_for_spreadsheet, ordered_keys
from config import buy_url, rent_url, commercial_rent_url
from pprint import pprint

def main():
    # Chrome Options
    with WebDriverConfig.create_and_get_driver() as driver:
        new_list = [ordered_keys]
        for url_object in [BuyURL(buy_url), RentURL(rent_url), CommercialRentURL(commercial_rent_url)]:
            property_service = PropertyService(driver, url_object)
            property_lst = property_service.fetch_property_data()
            list_of_lists = prepare_data_for_spreadsheet(property_lst)
            print('list_of_lists', list_of_lists)
            for s in list_of_lists:
                new_list.append(s)
        data_dict = {"Sheet 1": new_list}
        save_data("test_names.ods", data_dict)

    # Create an instance of the Property class
    # property = Property(driver)
    # # Get the listing URLs
    # listing_urls = property.get_listing_urls()
    # print(f"Found {len(listing_urls)} property URLs")
    # driver.quit()

print("________starting crawling___________")
main()
print("________crawling completed___________")