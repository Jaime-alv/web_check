# Copyright (C) 2021 Jaime Álvarez Fernández
import pathlib
import bs4
import requests
import webbrowser
import filecmp
import json
import logging
import shutil


class CompareUrl:
    def __init__(self, root, stored_url):
        self.root = root
        self.list_of_saved_url = stored_url
        # iterate through all saved urls in url_list.txt
        for each_url in self.list_of_saved_url:
            self.file_name = self.list_of_saved_url[each_url]['file_name']
            self.css_selector = self.list_of_saved_url[each_url]['css_selector']
            self.charset = self.list_of_saved_url[each_url]['encoding']
            self.url = each_url
            self.path = f'{self.root}\\url_data\\{self.file_name}.txt'
            logging.info(f'url = {self.url}')
            logging.info(f'file_name = {self.file_name}')
            logging.info(f'selector = {self.css_selector}')
            self.compare_url()

    # new temp file for comparing websites
    def compare_url(self):
        new_url = requests.get(self.url)

        if self.css_selector is not None:
            self.temp_file = pathlib.Path(f'{self.root}\\url_data\\temp.txt').open('w', encoding=self.charset)
            bs4_object = bs4.BeautifulSoup(new_url.text, features="html.parser")
            parsed_element = bs4_object.select(self.css_selector)
            self.temp_file.write(str(parsed_element[0].get_text()))
            self.temp_file.close()

        elif self.css_selector is None:
            self.temp_file = pathlib.Path(f'{self.root}\\url_data\\temp.txt').open('wb')
            for chunk in new_url.iter_content(10000):
                self.temp_file.write(chunk)
            self.temp_file.close()

        compare_files = filecmp.cmp(f'{self.root}\\url_data\\temp.txt', self.path, shallow=False)
        if compare_files:
            logging.warning(f"{self.url} Equal to stored one")
        elif not compare_files:
            logging.critical(f'Opening {self.url}. Differences found.')
            webbrowser.open(self.url)
            # todo: prompt differences in terminal
            self.save_url()

    def prompt_differences(self):
        new_file = pathlib.Path(f'{self.root}\\url_data\\temp.txt').open('r')
        new_file_by_line = new_file.readlines()
        old_file = pathlib.Path(f'{self.root}\\url_data\\{self.file_name}.txt').open('r')
        old_file_by_line = old_file.readlines()
        for line in new_file_by_line:
            if line not in old_file_by_line:
                print(line)

    # update stored file with new text and create backup with old text
    def save_url(self):
        logging.warning(f'Updating file with {self.url} in {self.path}')
        shutil.move(self.path, f'{self.root}\\url_data\\backup\\{self.file_name}_backup.txt')
        backup = pathlib.Path(f'{self.root}\\url_data\\backup\\{self.file_name}_backup.txt').open('r')
        backup.close()

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


if __name__ == "__main__":
    directory = '..\\storage'
    try:
        logging.basicConfig(filename=f'{directory}\\logs\\log.txt', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        pathlib.Path('../storage/logs/log.txt').open('w')
        with pathlib.Path(f'{directory}\\url_list.txt').open('r') as file:
            list_of_saved_url = json.load(file)
        if len(list_of_saved_url) == 0:
            print('List is empty')
            input()
        else:
            logging.debug(pathlib.Path.cwd())
            logging.debug('main function')
            print('Running...')
            CompareUrl(directory, list_of_saved_url)
    except FileNotFoundError:
        logging.error('Run main script first!')
        input()
