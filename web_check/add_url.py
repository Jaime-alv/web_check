# Web check
# A simple script that will warn you when there are new content in your favourite websites.
# Copyright (C) 2021 Jaime Alvarez Fernandez
# Contact: jaime.af.git@gmail.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ==========================================================================
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
            enc_charset = self.get_charset(pass_charset)

            if header is None:
                name = domain
            else:
                name = domain + '_' + header
            # create file with a unique name
            logging.warning(f'New file with name {name}.txt')
            additional_info = {}
            self.list_of_saved_url.setdefault(self.url, additional_info)
            self.list_of_saved_url[self.url].setdefault('file_name', name)
            self.list_of_saved_url[self.url].setdefault('encoding', enc_charset)
            logging.info(f"{name} with encoding {enc_charset}")

            # only look at the hash
            if self.css_selector is not None:
                new_file = pathlib.Path(f'{self.root}\\url_data\\{name}.txt').open('w', encoding=enc_charset)
                self.list_of_saved_url[self.url].setdefault('css_selector', self.css_selector)
                with pathlib.Path(f'{self.root}\\url_list.txt').open('w') as f:
                    json.dump(self.list_of_saved_url, f)
                bs4_object = bs4.BeautifulSoup(response.text, features="html.parser")
                parsed_element = bs4_object.select(self.css_selector)
                new_file.write(str(parsed_element[0].get_text()))

            # save the whole url
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

    # create file name with different parts from the given url
    def domain_name(self):
        name = re.compile(r'(http(s)?://)?(www\.)?(?P<domain>.*)\.([a-zA-Z]+)(/(?P<header>[a-zA-Z_\-]+)(/.*)?)?')
        seek_name = name.search(self.url)
        return seek_name.group('domain'), seek_name.group('header')

    # get encoding from website
    def get_charset(self, charset):
        charset_pattern = re.compile(r'charset=(?P<charset>.*)')
        search_charset = charset_pattern.search(charset)
        return search_charset.group('charset')


# add new css for a saved url
def modify_css_selector(root, list_of_saved_url, url, modify_css):
    if modify_css != '':
        modified_css = modify_css
    else:
        modified_css = None
    logging.warning(f"New css selector for {list_of_saved_url[url]['file_name']}")
    logging.info(f"old: {list_of_saved_url[url]['css_selector']}, new: {modify_css}")
    list_of_saved_url[url]['css_selector'] = modified_css
    with pathlib.Path(f'{root}\\url_list.txt').open('w') as overwrite:
        json.dump(list_of_saved_url, overwrite)


# delete a list of urls
def delete_url(root, list_of_saved_url, for_delete):
    for element in for_delete:
        file_name = list_of_saved_url[element]['file_name']
        file = pathlib.Path(f'{root}\\url_data\\{file_name}.txt')
        backup_file = pathlib.Path(f'{root}\\url_data\\backup\\{file_name}_backup.txt')
        pathlib.Path.unlink(file, missing_ok=True)
        pathlib.Path.unlink(backup_file, missing_ok=True)
        del list_of_saved_url[element]
    with pathlib.Path(f'{root}\\url_list.txt').open('w') as overwrite:
        json.dump(list_of_saved_url, overwrite)


# where things will be stored
def create_folder(root):
    if not pathlib.Path(f'{root}\\logs\\log.txt').exists():
        pathlib.Path(f'{root}\\logs').mkdir(parents=True, exist_ok=True)
        new_log = pathlib.Path(f'{root}\\logs\\log.txt').open('w')
        new_log.close()
        logging.warning('Log directory created')

    if not pathlib.Path(f'{root}\\url_data').exists():
        logging.error('No directory found')
        pathlib.Path(f'{root}\\url_data').mkdir(parents=True, exist_ok=True)
        pathlib.Path(f'{root}\\url_data\\backup').mkdir(parents=True, exist_ok=True)
        logging.debug('directory created')

    if not pathlib.Path(f'{root}\\url_list.txt').exists():
        logging.error('No url_list.txt')
        pathlib.Path(f'{root}\\url_list.txt').open('w')
        json_url_dict = {}
        with pathlib.Path(f'{root}\\url_list.txt').open('w') as f:
            json.dump(json_url_dict, f)
        logging.debug('text file for json created')


if __name__ == "__main__":
    try:
        logging.basicConfig(filename='../storage/logs/log.txt', level=logging.DEBUG,
                            format='%(levelname)s - %(message)s')
        with pathlib.Path(f'../storage/url_list.txt').open('r') as json_file:
            stored_url = json.load(json_file)
    except FileNotFoundError:
        create_folder('..\\storage')

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
