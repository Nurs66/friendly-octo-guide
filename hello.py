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
        'external_links': []
    }
    get_links = [i.get('href') for i in links]
    get_texts = [link.get_text().strip() for link in links]
    get_all_link = remove_url_and_str(get_links, domain)
    for link, text, tag_name in zip(get_all_link, get_texts, links):
        dict_tag_info = {
            tag_name.name: []
        }
        if re.search(fr'https://{domain}/\w+', link) or re.search(fr'https://{domain}\S+', link):
            data = {'tag_name': tag_name.name, 'link': link, 'content': text}
            dict_tag_info[tag_name.name].append(data)
            result_dict['internal_links'].append(dict_tag_info)
        elif re.search(fr'https://\w+.{domain}/\w+', link) or re.search(fr'https://\w+.{domain}', link):
            data = {'tag_name': tag_name.name, 'link': link, 'content': text}
            dict_tag_info[tag_name.name].append(data)
            result_dict['internal_links'].append(dict_tag_info)
        else:
            data = {'tag_name': tag_name.name, 'link': link, 'content': text}
            dict_tag_info[tag_name.name].append(data)
            result_dict['external_links'].append(dict_tag_info)
    return result_dict


def get_page_source(html_data):
    new_lst = []
    for data in html_data:
        if data.name in ['html', 'script', 'head', 'meta', 'title', 'style']:
            html_data.remove(data)
        else:
            new_lst.append(data)

    return new_lst
