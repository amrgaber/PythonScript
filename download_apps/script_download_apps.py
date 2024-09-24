from time import sleep
import unittest
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import os
import re

download_path = "/home/amr/odoo_apps/Website/"
category_path = "https://apps.odoo.com/apps/modules/category/Reporting/browse?price=Free"
category_path_part_url = "https://apps.odoo.com/apps/modules/category/Reporting/browse/page/"

def check_not_downloaded(updated_link):
    # print('****before len', len(updated_link))
    last_updated_links = []
    i = 0
    for link_iterate in updated_link:
        exist = False
        for root, dirs, files in os.walk(download_path):
            for name in files:
                if name.startswith((link_iterate.split("/")[-1] + "-")):
                    exist = True
                    break
            if exist:
                break
        if not exist:
            i += 1
            last_updated_links.append(link_iterate)
    # print('**** after len', len(last_updated_links))
    return last_updated_links

def split_versions(all_links):
    updated_link = {}
    dct_links_formated = {'6.0': [], '7.0': [], '8.0': [], '9.0': [], '10.0': [], '11.0': [], '12.0': [], '13.0': [],
                          '14.0': [], '15.0': [], '16.0': []
                          }
    for link in all_links:
        version = link.split("/")[-2]
        if version in dct_links_formated.keys():
            dct_links_formated[version].append(link)

    for key, val in dct_links_formated.items():
        if val:
            # print('** before **', len(val))
            val = check_not_downloaded(val)
            # print('** after **', len(val))
            updated_link[key] = val
    return updated_link

def download_list_of_apps(options, lst_of_apps):
    for item_key in lst_of_apps.keys():
        print('item_key', item_key)
        if lst_of_apps[item_key]:
            change_path = download_path
            change_path += item_key
            options.set_preference("browser.download.dir", change_path)
            driver = webdriver.Firefox(options=options)
            for link_inner in lst_of_apps[item_key]:
                driver.get(link_inner)
                sleep(5)
                gotit = driver.find_element(By.XPATH, "//form[@class='oe_import']//a[contains(@itemprop,'downloadUrl')]")
                if gotit:
                    gotit.click()
                    sleep(15)

def extract_apps(page):
    driver.get(page)
    sleep(5)
    lst_elements = driver.find_elements(By.CSS_SELECTOR, 'div.loempia_app_entry')
    lst_apps = []
    for item in lst_elements:
        element = item.find_element(By.TAG_NAME, 'a')
        href = element.get_attribute('href')
        if href:
            lst_apps.append(href)
    return lst_apps

def loop_pages(lst_elements):
    lst_pages = []
    for element in lst_elements:
        if not element.text or element.text != 'PREV' or element.text != 'NEXT':
            href = element.get_attribute('href')
            if href:
                lst_pages.append(href)
    return set(lst_pages)

if __name__ == '__main__':
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.panel.shown", False)
    options.set_preference("browser.download.manager.focusWhenStarting", False)
    options.set_preference("browser.download.manager.closeWhenDone", True)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(.5)
    driver.get(category_path)
    sleep(5)
    ul_element = driver.find_element(By.CSS_SELECTOR, 'ul.pagination')
    # pages_items = ul_element.find_elements(By.TAG_NAME, 'a')
    pages_items = [1]
    if pages_items:
        pages_count = 10
        if pages_count:
            lst_pages = []
            for item in range(1, int(pages_count)+1):
                link = category_path_part_url + str(item)+"?order=Highest+Price&price=Free"
                lst_pages.append(link)

            lst_all_links = []
            for page in lst_pages:
                lst_of_apps = extract_apps(page)
                lst_all_links += lst_of_apps
            lst_of_apps = split_versions(lst_all_links)
            download_list_of_apps(options, lst_of_apps)

    # # lst_pages = loop_pages(lst_elements)