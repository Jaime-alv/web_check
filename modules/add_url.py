#! python3
# Copyright 2021 Jaime Álvarez Fernández
import re
import pathlib
import requests
import json
import logging
import bs4


# TODO: check if given url is valid or not
# TODO: check if given url is already in json file
# TODO: add url and path file to json
# TODO: return to main.py
def domain_name(url):
    name = re.compile(r'(http(s)?://)?(www\.)?(?P<domain>.*)\.(([a-zA-Z]+)(/((?P<header>(.*))[/.:]))?)')
    seek_name = name.search(url)
    return seek_name.group('domain'), seek_name.group('header')


def main(url, css_selector, root):
    logging.critical(f'passed url: {url}')
    try:
        requests.get(url).raise_for_status()
        with pathlib.Path(f'{root}\\url_list.txt').open('r') as f:
            list_of_saved_url = json.load(f)
        if list_of_saved_url.get(url, None) is None:
            response = requests.get(url)
            domain, header = domain_name(url)

            if header is None:
                name = domain
            else:
                name = domain + '_' + header

            logging.warning(f'New file with name {name}.txt')
            additional_info = {}
            list_of_saved_url.setdefault(url, additional_info)
            list_of_saved_url[url].setdefault('file_name', name)

            if css_selector is not None:
                new_file = pathlib.Path(f'{root}\\url_data\\{name}.txt').open('w')
                list_of_saved_url[url].setdefault('css_selector', css_selector)
                with pathlib.Path(f'{root}\\url_list.txt').open('w') as f:
                    json.dump(list_of_saved_url, f)
                bs4_object = bs4.BeautifulSoup(response.text, features="html.parser")
                parsed_element = bs4_object.select(css_selector)
                new_file.write(str(parsed_element[0].get_text()))

            elif css_selector is None:
                new_file = pathlib.Path(f'{root}\\url_data\\{name}.txt').open('wb')
                list_of_saved_url[url].setdefault('css_selector', None)
                for chunk in response.iter_content(10000):
                    new_file.write(chunk)
            logging.debug(f'Stored url in json file {list_of_saved_url}')
    except:
        logging.error(f"Something went wrong with {url}")
        print('Error!')


if __name__ == "__main__":
    logging.basicConfig(filename='..\\storage\\logging\\log.txt', level=logging.DEBUG,
                        format='%(levelname)s - %(message)s')
    # add url manually
    print(
        'Add desired url, followed by a whitespace, followed by the unique css selector.\nurl needs to start with http:// or https://\n')
    answer_url = input('@: ')
    clean_answer = answer_url.split(' ', maxsplit=1)
    if len(clean_answer) == 2:
        main(clean_answer[0], clean_answer[1], '..\\storage')
    elif len(clean_answer) == 1:
        main(answer_url, None, '..\\storage')
