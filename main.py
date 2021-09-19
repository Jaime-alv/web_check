#! python3
# Copyright 2021 Jaime Álvarez Fernández
import pathlib
import requests
import webbrowser
import re
import filecmp
import sys
import json
import logging
from modules import add_url

try:
    logging.basicConfig(filename='storage\\logging\\log.txt', level=logging.DEBUG, format='%(levelname)s - %(message)s')
except FileNotFoundError:
    pathlib.Path('storage\\logging').mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename='storage\\logging\\log.txt', level=logging.DEBUG, format='%(levelname)s - %(message)s')
pathlib.Path('storage\\logging\\log.txt').open('w')


# TODO: check if url is valid
# TODO: check if passed argument is already in url_list.txt
# TODO: simplify version

def main(passed_argument):
    logging.debug(f'argument from sys {passed_argument}')
    if len(passed_argument) > 1:
        # call add_url.py
        with pathlib.Path('storage\\url_list.txt').open('r') as file:
            add_url = json.load(file)
        for n in range(1, len(passed_argument)):
            logging.debug(f'url to json: {passed_argument[n]}')
            add_url['url'].append(passed_argument[n])
        with pathlib.Path('storage\\url_list.txt').open('w') as file:
            json.dump(add_url, file)
    with pathlib.Path('storage\\url_list.txt').open('r') as file:
        list_of_saved_url = json.load(file)
        logging.debug(f'Stored url in json file {list_of_saved_url}')
    for each_url in list_of_saved_url['url']:
        check_url(each_url)


def domain_name(url):
    name = re.compile(r'(http(s)?://)?(www\.)?(?P<name>.*)(\.(es|com))(/((?P<header>(.*))[/.:]))?')
    seek_name = name.search(url)
    return seek_name.group('name'), seek_name.group('header')


# check url & store and save the page
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
    compare_url(url, path)


# compare to a saved version
def compare_url(url, path):
    new_url = requests.get(url)
    temp_file = pathlib.Path('storage\\temp.txt').open('wb')
    for chunk in new_url.iter_content(10000):
        temp_file.write(chunk)
    temp_file.close()
    compare_files = filecmp.cmp('storage\\temp.txt', path, shallow=False)
    if compare_files:
        temp_file.close()
        logging.critical(f"Equal to stored one")
    elif not compare_files:
        webbrowser.open(url)
        save_url(url, path)


# update the saved version
def save_url(url, path):
    open_url = pathlib.Path(path).open('wb')
    new_content_for_url = requests.get(url)
    for chunk in new_content_for_url.iter_content(10000):
        open_url.write(chunk)
    open_url.close()


if __name__ == "__main__":
    logging.debug(pathlib.Path.cwd())
    if not pathlib.Path('storage\\url_data').exists():
        logging.warning('No directory found')
        pathlib.Path('storage\\url_data').mkdir(parents=True, exist_ok=True)
        logging.debug('directory created')

    if not pathlib.Path('storage\\url_list.txt').exists():
        logging.warning('No url_list.txt')
        pathlib.Path('storage\\url_list.txt').open('w')
        url_list = []
        json_url_dict = {'url': url_list}
        with pathlib.Path('storage\\url_list.txt').open('w') as f:
            json.dump(json_url_dict, f)
        logging.debug('text file for json created')
        logging.debug('main function')
        main(sys.argv)

    else:
        logging.debug('main function')
        main(sys.argv)
