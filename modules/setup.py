#!"..\..\..\Automate the boring stuff\venv\Scripts\python.exe"
# Copyright 2021 Jaime Álvarez Fernández
import pathlib
import json
import logging


def setup():
    try:
        logging.basicConfig(filename='storage\\logging\\log.txt', level=logging.DEBUG,
                            format='%(levelname)s - %(message)s')
    except FileNotFoundError:
        if not pathlib.Path('..\\storage\\logging\\log.txt').exists():
            pathlib.Path('..\\storage\\logging').mkdir(parents=True, exist_ok=True)
            new_log = pathlib.Path('..\\storage\\logging\\log.txt').open('w')
            new_log.close()
            logging.warning('Log directory created')

        if not pathlib.Path('..\\storage\\url_data').exists():
            logging.error('No directory found')
            pathlib.Path('..\\storage\\url_data').mkdir(parents=True, exist_ok=True)
            logging.debug('directory created')

        if not pathlib.Path('..\\storage\\url_list.txt').exists():
            logging.error('No url_list.txt')
            pathlib.Path('..\\storage\\url_list.txt').open('w')
            json_url_dict = {}
            with pathlib.Path('..\\storage\\url_list.txt').open('w') as f:
                json.dump(json_url_dict, f)
            logging.debug('text file for json created')


if __name__ == "__main__":
    setup()
