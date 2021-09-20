#! python3
# Copyright 2021 Jaime Álvarez Fernández
import pathlib
import bs4
import requests
import webbrowser
import filecmp
import sys
import json
import logging
from modules import add_url
from modules import setup


def main():
    passed_argument = sys.argv
    if len(passed_argument) > 1:
        logging.debug(f'argument from sys {passed_argument}')
        for n in range(1, len(passed_argument)):
            add_url.main(passed_argument[n], None, 'storage')
    try:
        with pathlib.Path('storage\\url_list.txt').open('r') as file:
            list_of_saved_url = json.load(file)
            for each_url in list_of_saved_url:
                file_name = list_of_saved_url[each_url]['file_name']
                css_selector = list_of_saved_url[each_url]['css_selector']
                logging.debug(f'url = {each_url}')
                logging.debug(f'file_name = {file_name}')
                logging.debug(f'selector = {css_selector}')
                compare_url(each_url, file_name, css_selector)
    except FileNotFoundError:
        logging.error('Running setup.py')
        setup.setup()


# compare to a saved version
def compare_url(url, file_name, css_selector):
    new_url = requests.get(url)
    path = f'storage\\url_data\\{file_name}.txt'
    if css_selector is not None:
        temp_file = pathlib.Path('storage\\temp.txt').open('w', encoding='utf-8')
        bs4_object = bs4.BeautifulSoup(new_url.text, features="html.parser")
        parsed_element = bs4_object.select(css_selector)
        temp_file.write(str(parsed_element[0].get_text()))
        temp_file.close()
    elif css_selector is None:
        temp_file = pathlib.Path('storage\\temp.txt').open('wb')
        for chunk in new_url.iter_content(10000):
            temp_file.write(chunk)
            temp_file.close()
    compare_files = filecmp.cmp('storage\\temp.txt', path, shallow=False)
    if compare_files:
        logging.warning(f"{url} Equal to stored one")
    elif not compare_files:
        logging.critical(f'Opening {url}. Differences found.')
        webbrowser.open(url)
        save_url(url, path, css_selector)


# update the saved version
def save_url(url, path, css_selector):
    logging.warning(f'Updating file with {url} in {path}')
    if css_selector is not None:
        new_url = requests.get(url)
        open_old_url = pathlib.Path(path).open('w', encoding='utf-8')
        bs4_object = bs4.BeautifulSoup(new_url.text, features="html.parser")
        parsed_element = bs4_object.select(css_selector)
        open_old_url.write(str(parsed_element[0].get_text()))
        open_old_url.close()

    elif css_selector is None:
        open_url = pathlib.Path(path).open('wb')
        new_content_for_url = requests.get(url)
        for chunk in new_content_for_url.iter_content(10000):
            open_url.write(chunk)
        open_url.close()


if __name__ == "__main__":
    try:
        logging.basicConfig(filename='storage\\logging\\log.txt', level=logging.DEBUG,
                            format='%(levelname)s - %(message)s')
        pathlib.Path('storage\\logging\\log.txt').open('w')
    except FileNotFoundError:
        setup.setup()
    logging.debug(pathlib.Path.cwd())
    logging.debug('main function')
    main()
