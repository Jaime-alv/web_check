#! python3
# Copyright 2021 Jaime Álvarez Fernández
import re
import pathlib
import requests
import json
import logging


# TODO: check if given url is valid or not
# TODO: check if given url is already in json file
# TODO: add url and path file to json
# TODO: return to main.py
def domain_name(url):
    name = re.compile(r'(http(s)?://)?(www\.)?(?P<name>.*)(\.(es|com))(/((?P<header>(.*))[/.:]))?')
    seek_name = name.search(url)
    return seek_name.group('name'), seek_name.group('header')


# json = {'url': {'https://www.correos.com' : 'correos' }}
# json = {'url': {'name' : 'http://'}}


def main(url, root):
    logging.critical(f'passed url: {url}')
    try:
        requests.get(url).raise_for_status()
    except:
        logging.error(f"Something went wrong with {url}")
        print('Error!')
    with pathlib.Path(f'{root}\\url_list.txt').open('r') as f:
        list_of_saved_url = json.load(f)
    if list_of_saved_url['url'].get(url, None) is None:
        response = requests.get(url)
        name, header = domain_name(url)
        if header is None:
            name = name
        else:
            name = name + '_' + header
        logging.warning(f'New file with name {name}.txt')
        list_of_saved_url['url'].setdefault(url, name + '.txt')
        with pathlib.Path(f'{root}\\url_list.txt').open('w') as f:
            json.dump(list_of_saved_url, f)
        save_to = pathlib.Path(f'{root}\\url_data\\{name}.txt').open('wb')
        for chunk in response.iter_content(10000):
            save_to.write(chunk)
        logging.debug(f'Stored url in json file {list_of_saved_url}')


if __name__ == "__main__":
    logging.basicConfig(filename='..\\storage\\logging\\log.txt', level=logging.DEBUG,
                        format='%(levelname)s - %(message)s')
    # add url manually
    print('Add desired url\nurl needs to start with http:// or https://\n')
    answer_url = input('@: ')
    main(answer_url, '..\\storage')
