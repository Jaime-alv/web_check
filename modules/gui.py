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
        self.master.geometry('500x300')
        self.pack(expand=1, fill='both')
        self.master.title('web check')
        self.label = tkinter.Label(self)
        self.label['text'] = 'Web check'
        self.label['font'] = ("Arial Bold", 15)
        self.for_delete = []
        self.label.pack()
        self.tab_control = tkinter.ttk.Notebook(self)
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

    def main(self):
        self.terminate()
        self.home()
        self.add_url()
        self.modify_url()
        self.create_radio_button()
        self.delete_url_tab()
        self.create_check_button()

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

    def refresh(self):
        self.modify_frame.destroy()
        self.delete_frame.destroy()
        self.modify_frame = tkinter.Frame(self.tab_modify_url)
        self.modify_frame.pack(expand=1, fill='both')
        self.delete_frame = tkinter.Frame(self.tab_delete_url)
        self.delete_frame.pack(expand=1, fill='both')
        self.create_radio_button()
        self.create_check_button()

    def run_script(self):
        if len(self.list_of_saved_url) > 0:
            CompareUrl('..\\storage', self.list_of_saved_url)
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
        submit_button.pack(anchor='center', expand=1, ipadx=100, ipady=5)
        submit_button['command'] = self.add_new_url

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
            except:
                messagebox.showerror(title=None, message='Error!')
        elif not url.startswith(r'http'):
            messagebox.showerror('Error!', 'Incorrect format.\nUrl needs to start with http:// or https://')
        else:
            messagebox.showwarning('Duplicate', f'{url}\nAlready stored in url_list.txt')

    def modify_url(self):
        label_modify_css = tkinter.Label(self.tab_modify_url, text='Introduce new css:')
        label_modify_css.pack(side='top', anchor='w')
        self.modify_css = tkinter.StringVar()
        self.entry_new_css = tkinter.Entry(self.tab_modify_url)
        self.entry_new_css.pack(side='top', fill=tkinter.X)
        self.entry_new_css["textvariable"] = self.modify_css
        label_modify_css = tkinter.Label(self.tab_modify_url, text='Click url to modify:')
        label_modify_css.pack(side='top', anchor='w')
        self.modify_frame = tkinter.Frame(self.tab_modify_url)
        self.modify_frame.pack(expand=1, fill='both')
        button_submit = tkinter.Button(self.tab_modify_url, text='Submit')
        button_submit.pack(side='bottom', anchor='s')
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
        ModifyCssGUI(self.root, self.list_of_saved_url, self.mod_this_url, self.modify_css.get())
        messagebox.showinfo(title='Done', message=f'{self.mod_this_url}\nNew css selected.')

    def delete_url_tab(self):
        self.delete_frame = tkinter.Frame(self.tab_delete_url)
        self.delete_frame.pack(expand=1, fill='both')
        submit_button = tkinter.Button(self.tab_delete_url, text='Delete')
        submit_button.pack(side='bottom', anchor='s', ipadx=50, ipady=5)
        submit_button['command'] = self.delete_only
        submit_button = tkinter.Button(self.tab_delete_url, text='Delete all')
        submit_button.pack(side='bottom', anchor='s', ipadx=43, ipady=5)
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
        DeleteUrlGUI(self.root, self.list_of_saved_url, self.for_delete)
        self.refresh()
        messagebox.showinfo(title='Delete', message='Done')

    def delete_all(self):
        for url in self.list_of_saved_url:
            self.for_delete.append(url)
        DeleteUrlGUI(self.root, self.list_of_saved_url, self.for_delete)
        self.refresh()
        messagebox.showinfo(title='Delete', message='List clear')

    def del_this(self, i):
        order = sorted(self.list_of_saved_url)
        if self.true_false[i].get():
            self.for_delete.append(order[i])
        if not self.true_false[i].get() and order[i] in self.for_delete:
            self.for_delete.remove(order[i])

    def create_menu(self):
        menu = tkinter.Menu(self.master)
        menu.add_command(label='About')
        self.master.config(menu=menu)


if __name__ == "__main__":
    window = tkinter.Tk()
    app = WebCheckGUI(window, '..\\storage')
    app.mainloop()
