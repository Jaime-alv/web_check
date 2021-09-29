#!"..\..\Automate the boring stuff\venv\Scripts\python.exe"
# Copyright 2021 Jaime Álvarez Fernández
import pathlib
import bs4
import requests
import webbrowser
import filecmp
import json
import logging
from modules.add_url import NewUrl
from modules import setup
import shutil


class CompareUrl:
    def __init__(self, stored_url):
        print('Running...')
        self.list_of_saved_url = stored_url
        for each_url in self.list_of_saved_url:
            self.file_name = self.list_of_saved_url[each_url]['file_name']
            self.css_selector = self.list_of_saved_url[each_url]['css_selector']
            self.charset = self.list_of_saved_url[each_url]['encoding']
            self.url = each_url
            self.path = f'storage\\url_data\\{self.file_name}.txt'
            logging.info(f'url = {self.url}')
            logging.info(f'file_name = {self.file_name}')
            logging.info(f'selector = {self.css_selector}')
            self.compare_url()

    def compare_url(self):
        new_url = requests.get(self.url)
        if self.css_selector is not None:
            temp_file = pathlib.Path('storage\\temp.txt').open('w', encoding=self.charset)
            bs4_object = bs4.BeautifulSoup(new_url.text, features="html.parser")
            parsed_element = bs4_object.select(self.css_selector)
            temp_file.write(str(parsed_element[0].get_text()))
            temp_file.close()
        elif self.css_selector is None:
            temp_file = pathlib.Path('storage\\temp.txt').open('wb')
            for chunk in new_url.iter_content(10000):
                temp_file.write(chunk)
                temp_file.close()
        compare_files = filecmp.cmp('storage\\temp.txt', self.path, shallow=False)
        if compare_files:
            logging.warning(f"{self.url} Equal to stored one")
        elif not compare_files:
            logging.critical(f'Opening {self.url}. Differences found.')
            webbrowser.open(self.url)
            self.save_url()

    def save_url(self):
        logging.warning(f'Updating file with {self.url} in {self.path}')
        shutil.move(self.path, f'storage\\url_data\\backup\\{self.file_name}_backup.txt')
        if self.css_selector is not None:
            new_url = requests.get(self.url)
            open_old_url = pathlib.Path(self.path).open('w', encoding=self.charset)
            bs4_object = bs4.BeautifulSoup(new_url.text, features="html.parser")
            parsed_element = bs4_object.select(self.css_selector)
            open_old_url.write(str(parsed_element[0].get_text()))
            open_old_url.close()

        elif self.css_selector is None:
            open_url = pathlib.Path(self.path).open('wb')
            new_content_for_url = requests.get(self.url)
            for chunk in new_content_for_url.iter_content(10000):
                open_url.write(chunk)
            open_url.close()


def main():
    try:
        with pathlib.Path('storage\\url_list.txt').open('r') as file:
            list_of_saved_url = json.load(file)
        if len(list_of_saved_url) == 0:
            print('List is empty')
            NewUrl('storage', list_of_saved_url)
        else:
            CompareUrl(list_of_saved_url)
    except FileNotFoundError:
        logging.error('Running setup.py')
        setup.setup('storage')


if __name__ == "__main__":
    try:
        logging.basicConfig(filename='storage\\logs\\log.txt', level=logging.DEBUG,
                            format='%(levelname)s - %(message)s')
        pathlib.Path('storage\\logs\\log.txt').open('w')
    except FileNotFoundError:
        setup.setup('storage')
    logging.debug(pathlib.Path.cwd())
    logging.debug('main function')
    main()
