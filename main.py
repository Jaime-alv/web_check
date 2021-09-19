#! python3
# Copyright 2021 Jaime Álvarez Fernández
import pathlib
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
            add_url.main(passed_argument[n], 'storage')
    try:
        with pathlib.Path('storage\\url_list.txt').open('r') as file:
            list_of_saved_url = json.load(file)
    except FileNotFoundError:
        setup.setup()
    for each_url in list_of_saved_url['url']:
        file_name = list_of_saved_url['url'][each_url]
        compare_url(each_url, file_name)


# compare to a saved version
def compare_url(url, file_name):
    new_url = requests.get(url)
    path = f'storage\\url_data\\{file_name}'
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
    try:
        logging.basicConfig(filename='storage\\logging\\log.txt', level=logging.DEBUG,
                            format='%(levelname)s - %(message)s')
    except FileNotFoundError:
        setup.setup()
    pathlib.Path('storage\\logging\\log.txt').open('w')
    logging.debug(pathlib.Path.cwd())
    logging.debug('main function')
    main()
