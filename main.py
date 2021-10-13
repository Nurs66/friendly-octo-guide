import json
import time
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from hello import check_link_url_with_text, get_page_source

JSON_TEMPLATE = {
    "id": None,
    "website_id": None,
    "url": None,
    "tag": {
        'tags': None
    },
    "schema": None,
    "og": {
        "title": None,
        "description": None,
        "url": None,
        "image": {
            "url": None,
            "secure_url": None,
            "type": None,
            "width": None,
            "height": None,
            "alt": None
        }
    },
    "twitter": {
        "title": None,
        "description": None,
        "image": {
            "url": None,
            "alt": None
        }
    },
    "article": {
        "publisher": None,
        "author": None
    },
    "status_code": None,
    "last_scraped": None,
    "header": {
        "viewport": None,
        "charset": None,
        "language": None
    },
    "content": {
        "number_internal_links": None,
        "number_external_links": None,
        "text_length": None
    }
}

BASE_URL = 'https://24sevenoffice.com/no/regnskapsforer/tids-og-oppdragsstyring/'
options = Options()
options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
driver = webdriver.Chrome(executable_path='/home/nursultan/Desktop/test/chromedriver', options=options)
driver.get(BASE_URL)
domain = urlparse(BASE_URL).netloc
driver.maximize_window()
html_source = driver.page_source


def scrape_selenium(content, json_template):
    json_template['id'] = 1
    json_template['website_id'] = 1
    json_template['url'] = driver.current_url

    soup = BeautifulSoup(content, 'html.parser')

    tag_a = soup.findAll(['a', 'link'])
    all_tag_name = list(all_html for all_html in soup.find_all())
    data_page = get_page_source(all_tag_name)

    def clear_property(raw_str):
        return raw_str.split('=')[1].strip('"')

    def clear_property_key(raw_str):
        return raw_str.split('=')[0].strip('"')

    some_lst = []
    for tag in data_page:
        key = ''
        value = ''
        property_list = re.findall(r'\S*="[^=]*"', str(tag))
        for prop in property_list:
            key = clear_property_key(prop)
            value = clear_property(prop)

        dict_page_source = {
            tag.name: []
        }

        tag_data_dict = {
            'tag_name': tag.name,
            key: value
        }
        dict_page_source[tag.name].append(tag_data_dict)
        some_lst.append(dict_page_source)

    data = check_link_url_with_text(tag_a, domain)
    print('===============================')
    json_template['tag']['tags'] = data
    json_template['tag']['page_content'] = some_lst
    with open('data.json', 'w') as file:
        json.dump(json_template, file)
    print(json_template)


scrape_selenium(html_source, JSON_TEMPLATE)
