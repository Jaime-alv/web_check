#!"..\..\..\Automate the boring stuff\venv\Scripts\python.exe"
# Copyright 2021 Jaime Álvarez Fernández
import re
import pathlib
import sys
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
        logging.basicConfig(filename=f'{self.root}\\logs\\log.txt', level=logging.DEBUG,
                            format='%(levelname)s - %(message)s')
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
                for chunk in response.iter_content(10000):
                    new_file.write(chunk)
            logging.debug(f'Stored url in json file {self.list_of_saved_url}')
            print(f"Everything ok with {name}")
        except Exception:
            logging.error(f"Something went wrong with {self.url}")
            response = requests.get(self.url)
            logging.error(f"Response from request = {response}")
            print('Error!')

    def domain_name(self):
        name = re.compile(r'(http(s)?://)?(www\.)?(?P<domain>.*)\.([a-zA-Z]+)(/(?P<header>[a-zA-Z_\-]+)(/.*)?)?')
        seek_name = name.search(self.url)
        return seek_name.group('domain'), seek_name.group('header')


def get_charset(charset):
    charset_pattern = re.compile(r'charset=(?P<charset>.*)')
    search_charset = charset_pattern.search(charset)
    return search_charset.group('charset')


class DeleteUrl:
    def __init__(self, root, list_of_saved_url):
        self.root = root
        self.list_of_saved_url = list_of_saved_url
        if len(self.list_of_saved_url) > 0:
            self.delete_stored_url()
        else:
            print('List is empty!')

    def delete_stored_url(self):
        order = sorted(self.list_of_saved_url)
        index = 1
        print('00. Delete all')
        for http in order:
            print(f"{index:02}. {http}")
            index += 1
        print('Which url do you want to delete?')
        while True:
            url_number = input('#: ')
            if url_number.isdigit() and 0 < int(url_number) <= (index - 1):
                pathing = self.list_of_saved_url[order[(int(url_number) - 1)]]['file_name']
                file = pathlib.Path(f'{self.root}\\url_data\\{pathing}.txt')
                backup_file = pathlib.Path(f'{self.root}\\url_data\\backup\\{pathing}.txt')
                if file.exists():
                    pathlib.Path.unlink(file)
                if backup_file.exists():
                    pathlib.Path.unlink(backup_file)
                del self.list_of_saved_url[order[(int(url_number) - 1)]]
                with pathlib.Path(f'{self.root}\\url_list.txt').open('w') as overwrite:
                    json.dump(self.list_of_saved_url, overwrite)
                break
            elif url_number.isdigit() and int(url_number) == 0:
                url_data = pathlib.Path(f'{self.root}\\url_data')
                for file in url_data.iterdir():
                    if file.is_file():
                        pathlib.Path.unlink(file)
                for file in pathlib.Path(f"{self.root}\\url_data\\backup").iterdir():
                    if file.is_file():
                        pathlib.Path.unlink(file)
                clean_dict = {}
                with pathlib.Path(f'{self.root}\\url_list.txt').open('w') as overwrite:
                    json.dump(clean_dict, overwrite)
                break
            elif url_number.lower() == 'exit':
                sys.exit()
            else:
                print('Error! Enter a valid input.')


class ModifyCss:
    def __init__(self, root, list_of_saved_url):
        self.root = root
        self.list_of_saved_url = list_of_saved_url
        self.modify()

    def modify(self):
        order = sorted(self.list_of_saved_url)
        index = 1
        for url in order:
            print(f"{index:02}. {url}")
            index += 1
        print('Which url do you want to modify its css selector?')
        while True:
            url_number = input('#: ')
            if url_number.isdigit() and 0 < int(url_number) < index:
                print('Fill in new css selector.')
                new_css = input('@: ')
                switched_url = self.list_of_saved_url[order[(int(url_number) - 1)]]
                logging.warning(f"New css selector for {switched_url['file_name']}")
                logging.info(f"old: {switched_url['css_selector']}, new: {new_css}")
                switched_url['css_selector'] = new_css
                with pathlib.Path(f'{self.root}\\url_list.txt').open('w') as overwrite:
                    json.dump(self.list_of_saved_url, overwrite)
                break
            elif url_number.lower() == 'exit':
                sys.exit()
            else:
                print('Error! Enter a valid input.')


if __name__ == "__main__":
    try:
        logging.basicConfig(filename='..\\storage\\logs\\log.txt', level=logging.DEBUG,
                            format='%(levelname)s - %(message)s')
        with pathlib.Path(f'..\\storage\\url_list.txt').open('r') as json_file:
            stored_url = json.load(json_file)
    except FileNotFoundError:
        print('There is an error with some files, run setup.py')
    print("""
1. Add url
2. Modify url
3. Delete url
    """)
    answer = input('#: ')
    if answer == '1':
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
    elif answer == '2':
        ModifyCss('..\\storage', stored_url)
    elif answer == '3':
        DeleteUrl('..\\storage', stored_url)
