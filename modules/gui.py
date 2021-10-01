import tkinter
from tkinter import ttk
from tkinter import messagebox
from main import CompareUrl
from add_url import *
import json
import pathlib


class WebCheckGUI(tkinter.Frame):
    def __init__(self, master, root):
        super().__init__(master)
        self.root = root
        with pathlib.Path(f'{self.root}\\url_list.txt').open('r') as file:
            self.list_of_saved_url = json.load(file)
        self.master = master
        self.master.geometry('300x300')
        self.pack(expand=1, fill='both')
        self.master.title('web check')
        self.label = tkinter.Label(self)
        self.label['text'] = 'Web check'
        self.label['font'] = ("Arial Bold", 15)
        self.label.pack()
        self.create_tab()
        self.terminate()

    def create_tab(self):
        tab_control = tkinter.ttk.Notebook(self)
        self.tab_home = ttk.Frame(tab_control)
        self.tab_add_url = ttk.Frame(tab_control)
        self.tab_modify_url = ttk.Frame(tab_control)
        self.tab_delete_url = ttk.Frame(tab_control)
        tab_control.add(self.tab_home, text='Home')
        tab_control.add(self.tab_add_url, text='Add url')
        tab_control.add(self.tab_modify_url, text='Modify url')
        tab_control.add(self.tab_delete_url, text='Delete url')
        tab_control.pack(expand=1, fill='both')
        self.home()
        self.add_url()

    def terminate(self):
        close_program = tkinter.Button(self, fg='red', command=self.master.destroy)
        close_program['text'] = 'Close program'
        close_program['padx'] = 5
        close_program['pady'] = 5
        close_program.pack(side='bottom')

    def home(self):
        button_run_script = tkinter.Button(self.tab_home, text='Run')
        button_run_script['command'] = self.run_script
        button_run_script['font'] = ("Arial Bold", 15)
        button_run_script.pack(anchor='center', expand=1, ipadx=20, ipady=5)
        label_github = tkinter.Label(self.tab_home)
        label_github['text'] = 'https://github.com/Jaime-alv/web_check.git'
        label_github.pack(side='bottom')

    def run_script(self):
        if len(self.list_of_saved_url) > 0:
            result = CompareUrl('..\\storage', self.list_of_saved_url)
            if result:
                messagebox.showinfo('Done', 'All checks done!')
        else:
            messagebox.showerror('Error!', 'List is empty!')

    def add_url(self):
        self.new_url_string = tkinter.StringVar()
        self.new_url_css = tkinter.StringVar()
        label_add_url = tkinter.Label(self.tab_add_url, text='Add new url: ')
        label_add_url.pack(anchor='w')
        entry_url = tkinter.Entry(self.tab_add_url)
        entry_url.pack(fill=tkinter.X)
        entry_url["textvariable"] = self.new_url_string
        label_add_css = tkinter.Label(self.tab_add_url, text='Add unique css: ')
        label_add_css.pack(anchor='w')
        entry_css = tkinter.Entry(self.tab_add_url)
        entry_css.pack(fill=tkinter.X)
        entry_css['textvariable'] = self.new_url_css
        submit_button = tkinter.Button(self.tab_add_url, text='Submit new url')
        submit_button.pack(anchor='center', expand=1, ipadx=20, ipady=5)
        submit_button['command'] = self.add_new_url

    def add_new_url(self):
        url = self.new_url_string.get()
        if self.new_url_css.get() != '':
            unique_css = self.new_url_css.get()
        else:
            unique_css = None
        if url.startswith(r'http') and self.list_of_saved_url.get(url, None) is None:
            add = NewUrl(self.root, self.list_of_saved_url, url, unique_css)
            if add:
                messagebox.showinfo(f'Done', f'New url successfully added:\n{url}')
        elif not url.startswith(r'http'):
            messagebox.showerror('Error!', 'Incorrect format.\nUrl needs to start with http:// or https://')
        else:
            messagebox.showinfo('Duplicate', f'{url}\nAlready stored in url_list.txt')

    def create_menu(self):
        menu = tkinter.Menu(self.master)
        menu.add_command(label='About')
        self.master.config(menu=menu)


if __name__ == "__main__":
    window = tkinter.Tk()
    app = WebCheckGUI(window, '..\\storage')
    app.mainloop()
