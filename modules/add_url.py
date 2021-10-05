#!"..\..\..\Automate the boring stuff\venv\Scripts\python.exe"
# Copyright 2021 Jaime Álvarez Fernández
import re
import pathlib
import requests
import json
import logging
import bs4


class NewUrl:
    def __init__(self, root, list_of_saved_url, add_url, add_css):
        self.url = add_url
        self.css_selector = add_css
        self.root = root
        self.list_of_saved_url = list_of_saved_url
        self.main()

    def main(self):
        logging.critical(f'passed url: {self.url}')
        try:  # check if given url is valid or not
            requests.get(self.url).raise_for_status()
            response = requests.get(self.url)
            pass_charset = response.headers['Content-Type']
            domain, header = self.domain_name()
            enc_charset = get_charset(pass_charset)

            if header is None:
                name = domain
            else:
                name = domain + '_' + header

            logging.warning(f'New file with name {name}.txt')
            additional_info = {}
            self.list_of_saved_url.setdefault(self.url, additional_info)
            self.list_of_saved_url[self.url].setdefault('file_name', name)
            self.list_of_saved_url[self.url].setdefault('encoding', enc_charset)
            logging.info(f"{name} with encoding {enc_charset}")

            if self.css_selector is not None:
                new_file = pathlib.Path(f'{self.root}\\url_data\\{name}.txt').open('w', encoding=enc_charset)
                self.list_of_saved_url[self.url].setdefault('css_selector', self.css_selector)
                with pathlib.Path(f'{self.root}\\url_list.txt').open('w') as f:
                    json.dump(self.list_of_saved_url, f)
                bs4_object = bs4.BeautifulSoup(response.text, features="html.parser")
                parsed_element = bs4_object.select(self.css_selector)
                new_file.write(str(parsed_element[0].get_text()))

            elif self.css_selector is None:
                new_file = pathlib.Path(f'{self.root}\\url_data\\{name}.txt').open('wb')
                self.list_of_saved_url[self.url].setdefault('css_selector', None)
                with pathlib.Path(f'{self.root}\\url_list.txt').open('w') as f:
                    json.dump(self.list_of_saved_url, f)
                for chunk in response.iter_content(10000):
                    new_file.write(chunk)
            logging.debug(f'Stored url in json file {self.list_of_saved_url}')
            logging.info(f"Everything ok with {name}")
        except Exception:
            logging.error(f"Something went wrong with {self.url}")
            response = requests.get(self.url)
            logging.error(f"Response from request = {response}")

    def domain_name(self):
        name = re.compile(r'(http(s)?://)?(www\.)?(?P<domain>.*)\.([a-zA-Z]+)(/(?P<header>[a-zA-Z_\-]+)(/.*)?)?')
        seek_name = name.search(self.url)
        return seek_name.group('domain'), seek_name.group('header')


def get_charset(charset):
    charset_pattern = re.compile(r'charset=(?P<charset>.*)')
    search_charset = charset_pattern.search(charset)
    return search_charset.group('charset')


class ModifyCssGUI:
    def __init__(self, root, list_of_saved_url, url, modify_css):
        self.root = root
        self.list_of_saved_url = list_of_saved_url
        self.url = url
        self.modify_css = modify_css

        if self.modify_css != '':
            self.modified_css = self.modify_css
        else:
            self.modified_css = None
        logging.warning(f"New css selector for {self.list_of_saved_url[url]['file_name']}")
        logging.info(f"old: {self.list_of_saved_url[url]['css_selector']}, new: {self.modify_css}")
        self.list_of_saved_url[url]['css_selector'] = self.modified_css
        with pathlib.Path(f'{self.root}\\url_list.txt').open('w') as overwrite:
            json.dump(self.list_of_saved_url, overwrite)


class DeleteUrlGUI:
    def __init__(self, root, list_of_saved_url, for_delete):
        self.root = root
        self.list_of_saved_url = list_of_saved_url
        self.for_delete = for_delete
        for element in for_delete:
            file_name = list_of_saved_url[element]['file_name']
            file = pathlib.Path(f'{self.root}\\url_data\\{file_name}.txt')
            backup_file = pathlib.Path(f'{self.root}\\url_data\\backup\\{file_name}_backup.txt')
            pathlib.Path.unlink(file, missing_ok=True)
            pathlib.Path.unlink(backup_file, missing_ok=True)
            del self.list_of_saved_url[element]
        with pathlib.Path(f'{self.root}\\url_list.txt').open('w') as overwrite:
            json.dump(self.list_of_saved_url, overwrite)


class CreateFolder:
    def __init__(self, root):
        self.root = root
        if not pathlib.Path(f'{self.root}\\logs\\log.txt').exists():
            pathlib.Path(f'{self.root}\\logs').mkdir(parents=True, exist_ok=True)
            new_log = pathlib.Path(f'{self.root}\\logs\\log.txt').open('w')
            new_log.close()
            logging.warning('Log directory created')

        if not pathlib.Path(f'{self.root}\\url_data').exists():
            logging.error('No directory found')
            pathlib.Path(f'{self.root}\\url_data').mkdir(parents=True, exist_ok=True)
            pathlib.Path(f'{self.root}\\url_data\\backup').mkdir(parents=True, exist_ok=True)
            logging.debug('directory created')

        if not pathlib.Path(f'{self.root}\\url_list.txt').exists():
            logging.error('No url_list.txt')
            pathlib.Path(f'{self.root}\\url_list.txt').open('w')
            json_url_dict = {}
            with pathlib.Path(f'{self.root}\\url_list.txt').open('w') as f:
                json.dump(json_url_dict, f)
            logging.debug('text file for json created')


if __name__ == "__main__":
    try:
        logging.basicConfig(filename='..\\storage\\logs\\log.txt', level=logging.DEBUG,
                            format='%(levelname)s - %(message)s')
        with pathlib.Path(f'..\\storage\\url_list.txt').open('r') as json_file:
            stored_url = json.load(json_file)
    except FileNotFoundError:
        CreateFolder('..\\storage')

    print('Add desired url.')
    print('Url needs to start with http:// or https://')
    new_url = input('@: ')
    print('Add unique css selector.')
    css = input('css: ')
    if css != '':
        css_selector = css
    else:
        css_selector = None
    if stored_url.get(new_url, None) is None:
        result = NewUrl('..\\storage', stored_url, new_url, css_selector)
