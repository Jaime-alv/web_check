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
    name = re.compile(r'(http(s)?://)?(www\.)?(?P<domain>.*)(\.(es|com))(/((?P<header>(.*))[/.:]))?')
    seek_name = name.search(url)
    return seek_name.group('domain'), seek_name.group('header')


# json = {'https://www.correos.com' : info }
# info = {'css_selector' : 'whatever', 'filename' : 'correos.txt'}


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
            info = {'css_selector': None, 'filename': ''}
            list_of_saved_url.setdefault(url, info)
            list_of_saved_url['filename'] = name + '.txt'
            if css_selector is not None:
                list_of_saved_url['css_selector'] = css_selector
            with pathlib.Path(f'{root}\\url_list.txt').open('w') as f:
                json.dump(list_of_saved_url, f)
            if css_selector is None:
                save_to = pathlib.Path(f'{root}\\url_data\\{name}.txt').open('wb')
                for chunk in response.iter_content(10000):
                    save_to.write(chunk)
            else:
                save_to = pathlib.Path(f'{root}\\url_data\\{name}.txt').open('w')
                bs4_object = bs4.BeautifulSoup(response.text, features="html.parser")
                element = bs4_object.select(css_selector)
                save_to.write(element[0].text)

            logging.debug(f'Stored url in json file {list_of_saved_url}')
    except:
        logging.error(f"Something went wrong with {url}")
        print('Error!')


if __name__ == "__main__":
    logging.basicConfig(filename='..\\storage\\logging\\log.txt', level=logging.DEBUG,
                        format='%(levelname)s - %(message)s')
    # add url manually
    print('Add desired url\nurl needs to start with http:// or https://\n')
    answer_url = input('@: ')
    if len(answer_url.split(' ', 2)) == 2:
        main(answer_url.split(' ')[0], answer_url.split(' ')[1], '..\\storage')
    elif len(answer_url.split(' ')) == 1:
        main(answer_url.split(' ')[0], None, '..\\storage')
