#!"..\..\..\Automate the boring stuff\venv\Scripts\python.exe"
# Copyright 2021 Jaime Álvarez Fernández
import json
import pathlib


def show_stored_url(stored_url):
    order = sorted(stored_url)
    index = 1
    print('00. Delete all')
    for http in order:
        print(f"{index:02}. {http}")
        index += 1
    print('Which url do you want to delete?')
    while True:
        url_number = input('#: ')
        if url_number.isdigit() and 0 < int(url_number) <= (index - 1):
            if order[(int(url_number) - 1)] in stored_url:
                pathing = stored_url[order[(int(url_number) - 1)]]['file_name']
                file = pathlib.Path(f'..\\storage\\url_data\\{pathing}.txt')
                pathlib.Path.unlink(file)
                del list_of_saved_url[order[(int(url_number) - 1)]]
                with pathlib.Path(f'..\\storage\\url_list.txt').open('w') as overwrite:
                    json.dump(stored_url, overwrite)
                break
        elif url_number.isdigit() and (url_number == '00' or url_number == '0'):
            url_data = pathlib.Path('..\\storage\\url_data')
            for file in url_data.iterdir():
                pathlib.Path.unlink(file)
            clean_dict = {}
            with pathlib.Path(f'..\\storage\\url_list.txt').open('w') as overwrite:
                json.dump(clean_dict, overwrite)
            break
        else:
            print('Error! Enter a valid input')


if __name__ == "__main__":
    print('delete url from list')
    with pathlib.Path(f'..\\storage\\url_list.txt').open('r') as f:
        list_of_saved_url = json.load(f)
    if len(list_of_saved_url) > 0:
        show_stored_url(list_of_saved_url)
    else:
        print('List is empty!')
