import json
import re

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def remove_url_and_str(url_list, domain_name):
    all_url = []
    BASE_URL = 'https://{}{}'
    for url in url_list:
        if re.match(regex, url):
            all_url.append(url)
        elif re.match(r'tel:\+\d+ \d+ \d+ \d+', url):
            url_list.remove(url)
        else:
            all_url.append(BASE_URL.format(domain_name, url))
    return all_url


def check_link_url_with_text(links, domain):
    result_dict = {
        'internal_links': [],
        'external_links': [],
    }
    get_links = [i.get('href') for i in links]
    get_texts = [link.get_text().strip() for link in links]
    get_all_link = remove_url_and_str(get_links, domain)
    for link, text, tag_name in zip(get_all_link, get_texts, links):
        if re.search(fr'https://{domain}/\w+', link) or re.search(fr'https://{domain}\S+', link):
            data = {'tag_name': tag_name.name, 'link': link, 'content': text}
            result_dict['internal_links'].append(data)
        elif re.search(fr'https://\w+.{domain}/\w+', link) or re.search(fr'https://\w+.{domain}', link):
            data = {'tag_name': tag_name.name, 'link': link, 'content': text}
            result_dict['internal_links'].append(data)
        else:
            data = {'tag_name': tag_name.name, 'link': link, 'content': text}
            result_dict['external_links'].append(data)
    return result_dict


def get_page_source(html_data):
    new_lst = []
    for data in html_data:
        if data.name in ['html', 'script', 'head', 'meta', 'title', 'style']:
            html_data.remove(data)
        else:
            new_lst.append(data)

    return new_lst


def connect_list(list_of_tag, result_list):
    sorted_list = list(dict.fromkeys(list_of_tag))
    dictOfWords = {i: [] for i in sorted_list}
    for i in result_list:
        if i['tag_name'] in dictOfWords:
            dictOfWords[i['tag_name']].append(i)
    return dictOfWords


def second_part_schema_data(schema_list):
    lst_data = []
    json_decond = json.loads(schema_list)
    for j in json_decond:
        dict_data = {
            '@context': j.get('@context', None),
            '@type': j.get('@type', None),
            'name': j.get('name', None),
            'author': j.get('author', None),
            'datePublished': j.get('datePublished', None),
            'description': j.get('description', None),
            'prepTime': j.get('prepTime', None),
        }
        lst_data.append(dict_data)
    return lst_data


def get_schema_data(schema_list):
    lst_data = []
    for i in schema_list:
        try:
            result_json = json.loads(i)
            dict_data = {
                '@context': result_json.get('@context', None),
                '@type': result_json.get('@type', None),
                'name': result_json.get('name', None),
                'author': result_json.get('author', None),
                'datePublished': result_json.get('datePublished', None),
                'description': result_json.get('description', None),
                'prepTime': result_json.get('prepTime', None),
            }
            lst_data.append(dict_data)
        except Exception as e:
            second = second_part_schema_data(i)
            return second
    return lst_data
