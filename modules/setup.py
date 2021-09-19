import pathlib
import json
import logging


def setup():
    try:
        logging.basicConfig(filename='..\\storage\\logging\\log.txt', level=logging.DEBUG,
                            format='%(levelname)s - %(message)s')
    except FileNotFoundError:
        logging.warning('No logging directory')
        pathlib.Path('..\\storage\\logging').mkdir(parents=True, exist_ok=True)
        logging.basicConfig(filename='storage\\logging\\log.txt', level=logging.DEBUG,
                            format='%(levelname)s - %(message)s')
        logging.debug('directory created')

    if not pathlib.Path('..\\storage\\url_data').exists():
        logging.warning('No directory found')
        pathlib.Path('..\\storage\\url_data').mkdir(parents=True, exist_ok=True)
        logging.debug('directory created')

    if not pathlib.Path('..\\storage\\url_list.txt').exists():
        logging.warning('No url_list.txt')
        pathlib.Path('..\\storage\\url_list.txt').open('w')
        url_list = {}
        json_url_dict = {'url': url_list}
        with pathlib.Path('..\\storage\\url_list.txt').open('w') as f:
            json.dump(json_url_dict, f)
        logging.debug('text file for json created')


if __name__ == "__main__":
    setup()