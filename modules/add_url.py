# Copyright 2021 Jaime Álvarez Fernández
import re
import pathlib
import requests
import json
import logging

logging.basicConfig(filename='..\\storage\\logging\\log.txt', level=logging.DEBUG, format='%(levelname)s - %(message)s')


# TODO: check if given url is valid or not
# TODO: check if given url is already in json file
# TODO: add url and path file to json
# TODO: return to main.py
def domain_name(url):
    name = re.compile(r'(http(s)?://)?(www\.)?(?P<name>.*)(\.(es|com))(/((?P<header>(.*))[/.:]))?')
    seek_name = name.search(url)
    return seek_name.group('name'), seek_name.group('header')


# json = {'url': {'correos': 'https://www.correos.com', }}
# json = {'url': {'name' : 'http://'}}


def check_url(url):
    logging.critical(f'passed url: {url}')
    try:
        requests.get(url).raise_for_status()
    except:
        logging.error(f"Something went wrong with {url}")
        print('Error!')
    name, header = domain_name(url)
    response = requests.get(url)
    with pathlib.Path('..\\storage\\url_list.txt').open('r') as f:
        list_of_saved_url = json.load(f)
    if header is None:
        if url not in list_of_saved_url['url'][name]:
            logging.warning(f'New file with name {name}.txt')
            save_to = pathlib.Path(f'..\\storage\\url_data\\{name}.txt').open('wb')
            for chunk in response.iter_content(10000):
                save_to.write(chunk)
    else:
        name = name + '_' + header
        if url not in list_of_saved_url['url'][name]:
            logging.warning(f'New file with name {name}.txt')
            save_to = pathlib.Path(f'storage\\url_data\\{name}.txt').open('wb')
            for chunk in response.iter_content(10000):
                save_to.write(chunk)


if __name__ == "__main__":
    # add url manually
    print('Add desired url\nurl needs to start with http:// or https://\n')
    answer_url = input('@: ')
    check_valid_url(answer_url)
