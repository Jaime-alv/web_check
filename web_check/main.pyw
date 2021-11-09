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
import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from checker import CompareUrl
from add_url import *
from tkscrolledframe import ScrolledFrame


class WebCheckGUI(tkinter.Tk):
    def __init__(self, root):
        super().__init__()
        self.root = root
        with pathlib.Path(f'{self.root}\\url_list.txt').open('r') as file:
            self.list_of_saved_url = json.load(file)
        style = tkinter.ttk.Style()
        style.configure('TNotebook.Tab', font=('bahnschrift', 13))
        style.configure('TNotebook', font=('bahnschrift', 10))
        icon_file = pathlib.Path('../image/icon_bw.png')
        background_image = pathlib.Path('../image/logo.png')
        self.icon = tkinter.PhotoImage(file=icon_file)
        self.logo = tkinter.PhotoImage(file=background_image)
        self.master_frame = tkinter.Frame(self)
        self.wm_iconphoto(False, self.icon)
        self.title('web check')
        self.master_frame.pack(expand=1, fill='both')
        self.minsize(width=400, height=480)
        self.for_delete = []

        # create the different tabs in the script
        self.tab_control = tkinter.ttk.Notebook(self.master_frame)
        self.tab_home = ttk.Frame(self.tab_control)
        self.tab_add_url = ttk.Frame(self.tab_control)
        self.tab_modify_url = ttk.Frame(self.tab_control)
        self.tab_delete_url = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_home, text='Home')
        self.tab_control.add(self.tab_add_url, text='Add url')
        self.tab_control.add(self.tab_modify_url, text='Modify url')
        self.tab_control.add(self.tab_delete_url, text='Delete url')
        self.tab_control.pack(expand=1, fill='both')

        self.main()

    # create everything
    def main(self):
        self.terminate()
        self.home()
        self.add_url()
        self.modify_url()
        self.create_radio_button()
        self.delete_url_tab()
        self.create_check_button()
        self.create_menu()

    def terminate(self):
        close_program = tkinter.Button(self.master_frame, fg='red', text='Close', command=self.destroy,
                                       font=('bahnschrift', 11))
        close_program.pack(side='bottom', anchor='e', padx=3, pady=3)

    # create home tab
    def home(self):
        panel = tkinter.Label(self.tab_home, image=self.logo)
        panel.image = self.logo
        panel.pack(pady=20)

        button_run_script = tkinter.Button(self.tab_home, text='Run!', width=6)
        button_run_script['command'] = self.run_script
        button_run_script['font'] = ('bahnschrift', 15, 'bold')
        button_run_script.pack(side='top', anchor='center', expand=1)
        label_copyright = tkinter.Label(self.tab_home, font=('bahnschrift', 10), fg='#686565')
        label_copyright['text'] = 'Copyright (C) 2021 Jaime Álvarez Fernández'
        label_copyright.pack(side='bottom', anchor='s')

    # Update both, modify url and delete url, by destroying frames and calling again.
    def refresh(self):
        self.modify_css.set('')
        self.new_url_string.set('')
        self.new_url_css.set('')
        self.modify_frame.destroy()
        self.delete_frame.destroy()
        self.modify_frame = self.scroll_frame_mod_url.display_widget(tkinter.Frame)
        self.delete_frame = self.scroll_frame_del_url.display_widget(tkinter.Frame)
        self.create_radio_button()
        self.create_check_button()

    def run_script(self):
        if len(self.list_of_saved_url) > 0:
            CompareUrl('..\\storage', self.list_of_saved_url)
            self.whats_new_file = pathlib.Path(f'{self.root}\\logs\\whats_new.txt')
            with self.whats_new_file.open('r') as file:
                # If there are more than 1 line in whats_new.txt, there are some changes that needs to be printed
                if len(file.readlines()) > 1:
                    self.whats_new()
                else:
                    messagebox.showinfo('Done', 'All checks done!')
        else:
            messagebox.showerror('Error!', 'List is empty!')

    # create a new window for displaying changes
    def whats_new(self):
        line_by_line = self.whats_new_file.open('r', encoding='utf-8').readlines()
        whats_new_window = tkinter.Toplevel(self)
        whats_new_window.title("What's new today?")
        whats_new_window.wm_iconphoto(False, self.icon)

        scroll_whats_new = ScrolledFrame(whats_new_window, width=450, height=250)
        scroll_whats_new.pack(side="top", expand=1, fill="both")
        scroll_whats_new.bind_arrow_keys(whats_new_window)
        scroll_whats_new.bind_scroll_wheel(whats_new_window)
        whats_new_frame = scroll_whats_new.display_widget(tkinter.Frame)

        for i in range(1, len(line_by_line)):
            if line_by_line[i].startswith(r'- http'):
                header = tkinter.Label(whats_new_frame, text=line_by_line[i], font=('bahnschrift', 10, 'bold'))
                header.pack(anchor='w')
            else:
                content = tkinter.Label(whats_new_frame, text=line_by_line[i], font=('bahnschrift', 10))
                content.pack(anchor='w', padx=10)

        close_window = tkinter.Button(whats_new_window, text='Close', command=whats_new_window.destroy,
                                      font=('bahnschrift', 12))
        close_window.pack(pady=4, side='bottom', anchor='s')

    # create add url tab
    def add_url(self):
        self.new_url_string = tkinter.StringVar()
        self.new_url_css = tkinter.StringVar()
        label_add_url = tkinter.Label(self.tab_add_url, text='Add new url: ', font=('bahnschrift', 11))
        label_add_url.pack(anchor='w', padx=10)
        entry_url = tkinter.Entry(self.tab_add_url)
        entry_url.pack(fill=tkinter.X, padx=10)
        entry_url.focus()
        entry_url["textvariable"] = self.new_url_string
        label_add_css = tkinter.Label(self.tab_add_url, text='Add unique css: ', font=('bahnschrift', 11))
        label_add_css.pack(anchor='w', padx=10)
        entry_css = tkinter.Entry(self.tab_add_url)
        entry_css.pack(fill=tkinter.X, padx=10)
        entry_css['textvariable'] = self.new_url_css

        batch_button = tkinter.Button(self.tab_add_url, text='Import file', font=('bahnschrift', 11))
        batch_button.pack(anchor='nw', expand=1, pady=20, padx=10)
        batch_button['command'] = self.add_batch_url

        submit_button = tkinter.Button(self.tab_add_url, text='Submit new url', font=('bahnschrift', 11), width=14)
        submit_button.pack(anchor='s', expand=1, ipady=2, pady=3)
        submit_button['command'] = self.add_new_url

    def add_batch_url(self):
        file = filedialog.askopenfilename(filetypes=(("text file", "*.txt"), ("all files", "*.*")))
        open_file = pathlib.Path(file)
        lines = open_file.read_text().splitlines()
        url_plus_css = re.compile(r'(?P<url>.*?)(\s)(?P<css>.*)')
        for line in lines:
            if len(line.split(' ', maxsplit=1)) > 1:
                mo = url_plus_css.search(line)
                if mo.group('url').startswith(r'http') and self.list_of_saved_url.get(mo.group('url'), None) is None:
                    try:
                        NewUrl(self.root, self.list_of_saved_url, mo.group('url'), mo.group('css').strip())
                    except Exception:
                        messagebox.showerror(title=None, message=f"Error with {mo.group('url')}!")
            elif line.startswith(r'http') and self.list_of_saved_url.get(line, None) is None:
                NewUrl(self.root, self.list_of_saved_url, line, None)
        messagebox.showinfo(f'Done', f'New urls successfully added')
        self.refresh()

    def add_new_url(self):
        url = self.new_url_string.get()
        if self.new_url_css.get() != '':
            unique_css = self.new_url_css.get()
        else:
            unique_css = None
        if url.startswith(r'http') and self.list_of_saved_url.get(url, None) is None:
            try:
                NewUrl(self.root, self.list_of_saved_url, url, unique_css)
                messagebox.showinfo(f'Done', f'New url successfully added:\n{url}')
                self.refresh()
            except Exception:
                messagebox.showerror(title=None, message='Error!')
        elif not url.startswith(r'http'):
            messagebox.showerror('Error!', 'Incorrect format.\nUrl needs to start with http:// or https://')
        else:
            messagebox.showwarning('Duplicate', f'{url}\nAlready stored in url_list.txt')

    # create modify url tab
    def modify_url(self):
        label_modify_css = tkinter.Label(self.tab_modify_url, text='Introduce new css:', font=('bahnschrift', 11))
        label_modify_css.pack(side='top', anchor='w', padx=10)

        self.modify_css = tkinter.StringVar()
        self.entry_new_css = tkinter.Entry(self.tab_modify_url)
        self.entry_new_css.pack(side='top', fill=tkinter.X, padx=10)
        self.entry_new_css.focus()
        self.entry_new_css["textvariable"] = self.modify_css

        label_modify_css = tkinter.Label(self.tab_modify_url, text='Click url to modify:', font=('bahnschrift', 11))
        label_modify_css.pack(side='top', anchor='w', padx=10)

        self.scroll_frame_mod_url = ScrolledFrame(self.tab_modify_url, width=450, height=250)
        self.scroll_frame_mod_url.pack(side="top", expand=1, fill="both", padx=10)
        self.scroll_frame_mod_url.bind_arrow_keys(self.tab_modify_url)
        self.scroll_frame_mod_url.bind_scroll_wheel(self.tab_modify_url)
        self.modify_frame = self.scroll_frame_mod_url.display_widget(tkinter.Frame)

        button_submit = tkinter.Button(self.tab_modify_url, text='Submit', font=('bahnschrift', 11), width=10)
        button_submit.pack(side='bottom', anchor='s', ipady=3, pady=2)
        button_submit['command'] = self.modify_this_url

    def create_radio_button(self):
        self.for_modify = []
        order = sorted(self.list_of_saved_url)
        pos = 1
        for index in range(len(order)):
            self.check_var = tkinter.StringVar()
            self.for_modify.append(self.check_var)
            rb = tkinter.Radiobutton(self.modify_frame, text=f"{pos:02}. {order[index]}",
                                     command=lambda i=index: self.mod_this(order[i]), value=order[index])
            rb.pack(anchor='w')
            pos += 1

    def mod_this(self, url):
        self.mod_this_url = url

    def modify_this_url(self):
        modify_css_selector(self.root, self.list_of_saved_url, self.mod_this_url, self.modify_css.get())
        self.modify_css.set('')
        messagebox.showinfo(title='Done', message=f'{self.mod_this_url}\nNew css selected.')

    # create delete tab
    def delete_url_tab(self):
        label_delete = tkinter.Label(self.tab_delete_url, text='Check url:', font=('bahnschrift', 11))
        label_delete.pack(side='top', anchor='w', padx=10)

        self.scroll_frame_del_url = ScrolledFrame(self.tab_delete_url, width=450, height=250)
        self.scroll_frame_del_url.pack(side="top", expand=1, fill="both", padx=10)
        self.scroll_frame_del_url.bind_arrow_keys(self.tab_modify_url)
        self.scroll_frame_del_url.bind_scroll_wheel(self.tab_modify_url)
        self.delete_frame = self.scroll_frame_del_url.display_widget(tkinter.Frame)

        frame_delete_button = tkinter.Frame(self.tab_delete_url)
        frame_delete_button.pack(side='bottom')
        submit_button = tkinter.Button(frame_delete_button, text='Delete', font=('bahnschrift', 11), width=10)
        submit_button.grid(row=0, column=1, ipady=2, pady=3, padx=1)
        submit_button['command'] = self.delete_only
        submit_button = tkinter.Button(frame_delete_button, text='Delete all', font=('bahnschrift', 11), width=10)
        submit_button.grid(row=0, column=0, ipady=2, pady=3, padx=1)
        submit_button['command'] = self.delete_all

    def create_check_button(self):
        self.true_false = []
        order = sorted(self.list_of_saved_url)
        pos = 1
        for index in range(len(order)):
            self.true_false.append(tkinter.BooleanVar())
            self.true_false[-1].set(False)
            c = tkinter.Checkbutton(self.delete_frame, text=f"{pos:02}. {order[index]}", variable=self.true_false[-1],
                                    command=lambda i=index: self.del_this(i))
            c.pack(anchor='w')
            pos += 1

    def delete_only(self):
        delete_url(self.root, self.list_of_saved_url, self.for_delete)
        self.refresh()
        messagebox.showinfo(title='Delete', message='Done')

    def delete_all(self):
        for url in self.list_of_saved_url:
            self.for_delete.append(url)
        delete_url(self.root, self.list_of_saved_url, self.for_delete)
        self.refresh()
        messagebox.showinfo(title='Delete', message='List clear')

    # add to, or remove from, list 'for_delete' the urls passed from create_check_button
    def del_this(self, i):
        order = sorted(self.list_of_saved_url)
        if self.true_false[i].get():
            self.for_delete.append(order[i])
        if not self.true_false[i].get() and order[i] in self.for_delete:
            self.for_delete.remove(order[i])

    def create_menu(self):
        menu = tkinter.Menu(self)

        new_item = tkinter.Menu(menu, tearoff=0)
        new_item.add_command(label='Reset url file', command=self.reset_url_file)
        new_item.add_command(label='Create batch file', command=self.create_batch_file)
        new_item.add_command(label='Create shortcut', command=self.shortcut)
        new_item.add_separator()
        new_item.add_command(label='About', command=self.about_script)
        new_item.add_separator()
        new_item.add_command(label='Close', command=self.destroy)

        menu.add_cascade(label='Options', menu=new_item)
        self.config(menu=menu)

    # re-write url_list.txt completely empty
    def reset_url_file(self):
        json_url_dict = {}
        with pathlib.Path(f'{self.root}\\url_list.txt').open('w') as f:
            json.dump(json_url_dict, f)
        logging.debug('New text file for json created')
        with pathlib.Path(f'{self.root}\\url_list.txt').open('r') as file:
            self.list_of_saved_url = json.load(file)
        self.refresh()
        messagebox.showinfo(title='Reset', message='Url file reset complete!')

    # create a batch file for checker.py
    def create_batch_file(self):
        main_file = pathlib.Path(f'checker.py').resolve()

        messagebox.showinfo(title='Where is it?', message='Path to python.exe in your virtual environment')
        python_exe = tkinter.filedialog.askopenfilename(filetypes=(("exe file", "*.exe"), ("all files", "*.*")))
        python_venv = pathlib.Path(python_exe).resolve()

        working_directory = pathlib.Path.cwd()

        messagebox.showinfo(title='Where do I save it?', message='Path for saving checker.bat')
        batch_file_location = tkinter.filedialog.askdirectory()
        pathlib.Path(f'{batch_file_location}\\checker.bat').open('w')
        batch_file = pathlib.Path(f'{batch_file_location}\\checker.bat')
        data = f'cd "{working_directory}"\n"{python_venv}" "{main_file}"'
        batch_file.write_text(data)

        messagebox.showinfo(title='Done', message='Success!')

    # create a batch file for main.pyw
    def shortcut(self):
        main_file = pathlib.Path(f'main.pyw').resolve()

        messagebox.showinfo(title='Where is it?', message='Path to pythonw.exe in your virtual environment')
        python_exe = tkinter.filedialog.askopenfilename(filetypes=(("exe file", "*.exe"), ("all files", "*.*")))
        python_venv = pathlib.Path(python_exe).resolve()

        working_directory = pathlib.Path.cwd()

        messagebox.showinfo(title='Where do I save it?', message='Path for saving web_check.bat')
        batch_file_location = tkinter.filedialog.askdirectory()
        pathlib.Path(f'{batch_file_location}\\web_check.bat').open('w')
        batch_file = pathlib.Path(f'{batch_file_location}\\web_check.bat')
        data = f'cd "{working_directory}"\n"{python_venv}" "{main_file}"'
        batch_file.write_text(data)

        messagebox.showinfo(title='Done', message='Success!')

    # create a new window with all info about the script
    def about_script(self):
        new_window = tkinter.Toplevel()
        new_window.title('About...')
        new_window.geometry('450x200')
        new_window.resizable(False, False)
        new_window.wm_iconphoto(False, self.icon)
        new_window.focus()
        font = ('bahnschrift', 10)
        script = 'Web check'
        contact = 'Contact: jaime.af.git@gmail.com'
        repository = 'Repository: https://github.com/Jaime-alv/web_check.git'
        version = 'Version: v1.2.0'
        license_script = 'License: GPL-3.0-or-later'
        author = 'Author: Jaime Álvarez Fernández'

        script_label = tkinter.Label(new_window, text=script, font=('bahnschrift', 13, 'bold'))
        script_label.pack(padx=10, pady=2, side='top', anchor='w')

        middle_frame = tkinter.Frame(new_window)
        middle_frame.pack(anchor='center')
        right_frame = tkinter.Frame(middle_frame)
        right_frame.pack(side='right')
        left_frame = tkinter.Frame(middle_frame)
        left_frame.pack(side='left')

        panel = tkinter.Label(left_frame, image=self.icon)
        panel.image = self.icon
        panel.pack(padx=10)

        contact_label = tkinter.Label(right_frame, text=contact, font=font)
        contact_label.pack(anchor='w', padx=10, pady=2)
        repo_label = tkinter.Label(right_frame, text=repository, font=font)
        repo_label.pack(anchor='w', padx=10, pady=2)
        version_label = tkinter.Label(right_frame, text=version, font=font)
        version_label.pack(anchor='w', padx=10, pady=2)
        license_label = tkinter.Label(right_frame, text=license_script, font=font)
        license_label.pack(anchor='w', padx=10, pady=2)
        author_label = tkinter.Label(right_frame, text=author, font=font)
        author_label.pack(anchor='w', padx=10, pady=2)

        close_window = tkinter.Button(new_window, text='Ok', font=('bahnschrift', 12), width=6, fg='red',
                                      command=new_window.destroy)
        close_window.pack(pady=4, anchor='s', side='bottom')


if __name__ == "__main__":
    directory = '..\\storage'
    try:
        logging.basicConfig(filename=pathlib.Path(f'{directory}\\logs\\log.txt'), level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        pathlib.Path(f'{directory}\\logs\\log.txt').open('w')
    except FileNotFoundError:
        create_folder(directory)
    WebCheckGUI(directory).mainloop()
