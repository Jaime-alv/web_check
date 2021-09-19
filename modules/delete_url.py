#! python3
# Copyright 2021 Jaime Álvarez Fernández
import json
import pathlib


def show_stored_url():
    with pathlib.Path(f'..\\storage\\url_list.txt').open('r') as f:
        list_of_saved_url = json.load(f)
    index = 1
    for http in list_of_saved_url['url']:
        print(f"{str(index)}. {list_of_saved_url['url'].get(http)[:-4]}")
        index += 1
    print('Which url do you want to delete?')
    delete = input('#: ')
    with pathlib.Path(f'..\\storage\\url_list.txt').open('w') as f:




if __name__ == "__main__":
    print('delete url from list')
    show_stored_url()