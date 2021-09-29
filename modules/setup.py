#!"..\..\..\Automate the boring stuff\venv\Scripts\python.exe"
# Copyright 2021 Jaime Álvarez Fernández
import pathlib
import json
import logging

# web_check-->modules
#           |
#           |->storage-->logs
#                    |-->url_data


def setup(root):
    try:
        logging.basicConfig(filename=f'{root}\\logs\\log.txt', level=logging.DEBUG,
                            format='%(levelname)s - %(message)s')
    except FileNotFoundError:
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
    setup('..\\storage')
