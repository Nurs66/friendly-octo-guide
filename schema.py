import json
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from hello import get_schema_data
from main import scrape_selenium

JSON_TEMPLATE = {
    "id": None,
    "website_id": None,
    "url": None,
    "tag": {
        "tags": None,
        "title": None,
        "description": None,
        # "h1": None,
        "canonical": None,
        "robots": []
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

BASE_URL = 'https://www.akademikliniken.no/hva-vi-gjor/har/hartap/'
options = Options()
options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
driver = webdriver.Chrome(executable_path='/home/nursultan/Desktop/test/chromedriver', options=options)
driver.get(BASE_URL)
domain = urlparse(BASE_URL).netloc
driver.maximize_window()
html_source = driver.page_source


def scrape_schema(content, json_template):
    soup = BeautifulSoup(content, 'html.parser')
    schema_html = soup.findAll('script', {'type': 'application/ld+json'})

    schema_data = get_schema_data(schema_html)
    json_template['schema'] = schema_data
    with open('data.json', 'w') as file:
        json.dump(json_template, file)
    print(json_template)


template = scrape_selenium(html_source, JSON_TEMPLATE)

scrape_schema(html_source, template)
