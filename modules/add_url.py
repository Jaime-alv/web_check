# Copyright 2021 Jaime Álvarez Fernández
import re
import pathlib
import requests
import json
import logging

logging.basicConfig(filename='storage\\logging\\log.txt', level=logging.DEBUG, format='%(levelname)s - %(message)s')


# TODO: check if given url is valid or not
# TODO: check if given url is already in json file
# TODO: add url and path file to json
# TODO: return to main.py
def domain_name(url):
    name = re.compile(r'(http(s)?://)?(www\.)?(?P<name>.*)(\.(es|com))(/((?P<header>(.*))[/.:]))?')
    seek_name = name.search(url)
    return seek_name.group('name'), seek_name.group('header')


def check_url(url):
    logging.critical(f'passed url: {url}')
    response = requests.get(url)
    try:
        response.raise_for_status()
    except:
        logging.error(f"Something went wrong with {url}")
        print('Error!')
    name, header = domain_name(url)
    if header is None:
        if not pathlib.Path(f'storage\\url_data\\{name}.txt').exists():
            logging.warning(f'New file with name {name}.txt')
            save_to = pathlib.Path(f'storage\\url_data\\{name}.txt').open('wb')
            for chunk in response.iter_content(10000):
                save_to.write(chunk)
            save_to.close()
        path = f'storage\\url_data\\{name}.txt'
    else:
        if not pathlib.Path(f'storage\\url_data\\{name}_{header}.txt').exists():
            logging.warning(f'New file with name {name}_{header}.txt')
            save_to = pathlib.Path(f'storage\\url_data\\{name}_{header}.txt').open('wb')
            for chunk in response.iter_content(10000):
                save_to.write(chunk)
            save_to.close()
        path = f'storage\\url_data\\{name}_{header}.txt'


if __name__ == "__main__":
    # add url manually
    print('Add desired url')
