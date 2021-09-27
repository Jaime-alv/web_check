#!"..\..\..\Automate the boring stuff\venv\Scripts\python.exe"
# Copyright 2021 Jaime Álvarez Fernández
import re
import pathlib
import requests
import json
import logging
import bs4


def get_charset(charset):
    charset_pattern = re.compile(r'charset=(?P<charset>.*)')
    search_charset = charset_pattern.search(charset)
    return search_charset.group('charset')


class NewUrl:
    def __init__(self, url, css_selector, root):
        self.url = url
        self.css_selector = css_selector
        self.root = root
        self.main()

    def main(self):
        logging.critical(f'passed url: {self.url}')
        try:  # check if given url is valid or not
            requests.get(self.url).raise_for_status()
            with pathlib.Path(f'{self.root}\\url_list.txt').open('r') as f:
                list_of_saved_url = json.load(f)
            # check if given url is already in json file
            if list_of_saved_url.get(self.url, None) is None:
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
                list_of_saved_url.setdefault(self.url, additional_info)
                list_of_saved_url[self.url].setdefault('file_name', name)
                list_of_saved_url[self.url].setdefault('encoding', enc_charset)
                logging.info(f"{name} with encoding {enc_charset}")

                if self.css_selector is not None:
                    new_file = pathlib.Path(f'{self.root}\\url_data\\{name}.txt').open('w', encoding=enc_charset)
                    list_of_saved_url[self.url].setdefault('css_selector', self.css_selector)
                    with pathlib.Path(f'{self.root}\\url_list.txt').open('w') as f:
                        json.dump(list_of_saved_url, f)
                    bs4_object = bs4.BeautifulSoup(response.text, features="html.parser")
                    parsed_element = bs4_object.select(self.css_selector)
                    new_file.write(str(parsed_element[0].get_text()))

                elif self.css_selector is None:
                    new_file = pathlib.Path(f'{self.root}\\url_data\\{name}.txt').open('wb')
                    list_of_saved_url[self.url].setdefault('css_selector', None)
                    for chunk in response.iter_content(10000):
                        new_file.write(chunk)
                logging.debug(f'Stored url in json file {list_of_saved_url}')
                print(f"Everything ok with {name}")
        except:
            logging.error(f"Something went wrong with {self.url}")
            print('Error!')

    def domain_name(self):
        name = re.compile(r'(http(s)?://)?(www\.)?(?P<domain>.*)\.([a-zA-Z]+)(/(?P<header>[a-zA-Z_\-]+)(/.*)?)?')
        seek_name = name.search(self.url)
        return seek_name.group('domain'), seek_name.group('header')


if __name__ == "__main__":
    logging.basicConfig(filename='..\\storage\\logging\\log.txt', level=logging.DEBUG,
                        format='%(levelname)s - %(message)s')
    # add url manually
    print(
        'Add desired url, followed by a whitespace, followed by the unique css selector.\nurl needs to start with http:// or https://\n')
    answer_url = input('@: ')
    clean_answer = answer_url.split(' ', maxsplit=1)
    if len(clean_answer) == 2:
        NewUrl(clean_answer[0], clean_answer[1], '..\\storage')
    elif len(clean_answer) == 1:
        NewUrl(answer_url, None, '..\\storage')
