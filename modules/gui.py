import tkinter
from tkinter import ttk


class WebCheckGUI(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
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
        self.tab_add_url = ttk.Frame(tab_control)
        self.tab_modify_url = ttk.Frame(tab_control)
        self.tab_delete_url = ttk.Frame(tab_control)
        tab_control.add(self.tab_add_url, text='Add url')
        tab_control.add(self.tab_modify_url, text='Modify url')
        tab_control.add(self.tab_delete_url, text='Delete url')
        tab_control.pack(expand=1, fill='both')
        self.add_url()

    def terminate(self):
        self.close_program = tkinter.Button(self, fg='red', command=self.master.destroy)
        self.close_program['text'] = 'Close program'
        self.close_program['padx'] = 5
        self.close_program['pady'] = 5
        self.close_program.pack(side='bottom')

    def add_url(self):
        label_add_url = tkinter.Label(self.tab_add_url, text='Add new url: ')
        label_add_url.grid(column=0, row=0)
        self.entry_url = tkinter.Entry(self.tab_add_url)
        self.entry_url.grid(column=1, row=0, rowspan=1)
        label_add_css = tkinter.Label(self.tab_add_url, text='Add unique css: ')
        label_add_css.grid(column=0, row=1)
        self.entry_css = tkinter.Entry(self.tab_add_url)
        self.entry_css.grid(column=1, row=1, rowspan=1)


root = tkinter.Tk()
app = WebCheckGUI(root)
app.mainloop()
