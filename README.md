# web check
 A simple script that will warn you when there are new content in your favourite websites.

![logo](image/logo_new.png)

# What it does
The script will check, when run, if there are any changes in the websites. If any changes are found, it will open a new 
browser tab.

**Not every website can be scrap.**
# How does it work?
After adding an url the script creates a copy of website's content in your hard drive.
When run again, it will compare the website against that stored content line by line, if there is any difference a new tab
will be open.

A lot of websites have some kind of calendar, that means, every day there will be changes in those websites. To avoid this, 
you can add a unique css selector to each stored url. With this unique identification, the script targets only specific 
parts of the website, and avoid unnecessary calls to browser.

If there is a change, a new back up file will be created at storage/url_data/backup.

All urls are stored in a JSON file with all the needed information, including encoding.

#### How to get the unique css selector
Go to the website, right click in the zone you want the script to check. Go to inspect mode.
Hover your mouse until you see (usually in blue) everything you want. Right click and copy selector.
Paste that in the css field in add url, or modify url.

# Set up
- Install python from https://www.python.org/ (_built under python 3.9_)

- Create a new virtual environment following the instructions in https://docs.python.org/3/library/venv.html

    `python3 -m venv /path/to/new/virtual/environment`
- Activate said venv
- Install requirements.txt

    `pip install -r /path/to/requirements.txt`
- Script is ready!
# Running the script
Once everything is installed, launch the script with web_check/main.py. There are four tabs.

![home](image/doc/home.png?raw=true)
- 'Home': it's the main tab. From here you can launch checker.py with the button _Run!_. Checker.py it's in charge of all 
the logic. It will access your stored url and compare it with the actual website.
- 'Add url': From this tab, you can add a new url for checking, and its unique css selector.

  **Important:** url have to start with _http://_ or _https://_. Hit _Submit new url_ and the script will make all
necessary checks.

  There is a second option, _Import file_.
Import file will let you select a .txt file with several urls, and all of them will be stored.

  The txt file needs to follow the structure: url(white space)css selector. One url per line.
  
  `https://github.com/ body > div.application-main > div > div > div > div > div > main`
  
  `https://www.reddit.com/ #SHORTCUT_FOCUSABLE_DIV`
  
  `https://postal.fsc.ccoo.es/Inicio #divMainContent`

- 'Modify url': If you need to change an url css selector, you can do it from here. Enter a new css selector, or leave it
empty for capturing the whole site, and hit _submit_.
- 'Delete url': Two options for deleting. Check one, or several, urls and hit _delete_. _Delete all_ will delete all urls stored.

At the **Options**' menu, it's possible to reset the url_list.txt if, for some reason, the file can't be read with 'reset url'.
'Create batch file' will let automate the script, for faster use.
### Automate the script
There is no need to run web_check/main.py every time you want to check your websites, for that, only checker.py is required.

You can run checker.py manually whenever you want, but that's tedious and forgettable, first you would have to activate 
a virtual environment, and then, run checker.py.
With 'Create batch file' you only have to point where python.exe is (the virtual environment one) and a directory where 
the file will be created.

After all, it's easier to run directly **web_check.bat** or add the batch file to windows' task scheduler.

###### Copyright (C) 2021 Jaime Álvarez Fernández
