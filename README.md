# web_check
 A simple script that will warn you when there are new content in your preferred websites.

# What it does?
The script will check, when run, if there are any changes in the websites. If any changes are found, it will open a new 
browser tab.

Not every website can be scrap.
# How does it work?
After adding an url the script creates a copy of website's content in your hard drive.
When run again, it will compare the website against that stored content line by line, if there is any difference a new tab
will be open.

A lot of websites have some kind of calendar, that means, every day there will be changes in those websites. To avoid this, 
you can add a unique css selector to each stored url. With this unique identification, the script targets only specific 
parts of the website, and avoid unnecessary calls to browser.

If there is a change, a new back up file will be created at storage/url_data/backup

All urls are stored in a JSON file with all the needed information, including encoding.

# Set up
- Install python from https://www.python.org/

- Create a new virtual environment following the instructions in https://docs.python.org/3/library/venv.html

    `python3 -m venv /path/to/new/virtual/environment`
- Activate said venv
- Install requirements.txt

    `pip install -r /path/to/requirements.txt`
- Run modules/setup.py
- Script is ready!

# Automate the script
You can run main.py whenever you want, but that's tedious and forgettable.

### Batch file

