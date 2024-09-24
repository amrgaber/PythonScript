from urllib.parse import urlparse
main_url_EXCEL_LIST = ['Created On', 'Updated On', 'country', 'domain', 'language', 'Main Category']
from property import EXCEL_LIST as property_EXCEL_LIST
from agent import EXCEL_LIST as agent_EXCEL_LIST
from Amenity import EXCEL_LIST as amenity_EXCEL_LIST
from location import EXCEL_LIST as location_EXCEL_LIST
from property_reference import EXCEL_LIST as property_reference_EXCEL_LIST
from permit_number import EXCEL_LIST as dld_permit_number_EXCEL_LIST

# Create an ordered list of keys for the Excel sheet
ordered_keys = main_url_EXCEL_LIST
ordered_keys.extend(location_EXCEL_LIST)
ordered_keys.extend(property_EXCEL_LIST)
ordered_keys.extend(agent_EXCEL_LIST)
ordered_keys.extend(amenity_EXCEL_LIST)
ordered_keys.extend(property_reference_EXCEL_LIST)
ordered_keys.extend(dld_permit_number_EXCEL_LIST)

def prepare_data_for_spreadsheet(data):
    rows = []

    for d in data:
        row = [d.get(key, "") for key in ordered_keys]
        rows.append(row)

    return rows

def extract_keys_from_url(self, url, keys):
    parsed_url = urlparse(url)

    # Split the path and netloc into parts
    path_parts = parsed_url.path.split('/')
    netloc_parts = parsed_url.netloc.split('.')

    # Remove empty strings from the list
    all_parts = [part for part in netloc_parts + path_parts if part]

    # Create a dictionary with the keys and their corresponding values
    key_value_dict = {key: all_parts[i] for i, key in enumerate(keys) if i < len(all_parts)}

    return key_value_dict