from tkinter import *
from tkinter import ttk
import sqlite3
from urllib.request import urlopen as uReq
import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import numpy as np
import sys
import add_menu
import update_menu
import find_menu
import stats_menu

class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.db_file_name = 'book_list.db'
        self.set_up_db()

        stats_menu.StatsMenu(root)
       
        self.main_tree = ttk.Treeview(self)
        self.main_tree['columns'] = ("Book Title", "Author", "Pages", "Date Published", "Genre", "My Rating")

        self.main_tree.column("#0", width=0, stretch=NO)
        self.main_tree.column("Book Title", anchor=W, width=300 )
        self.main_tree.column("Author", anchor=W, width=120)
        self.main_tree.column("Pages", anchor=W, width=80)
        self.main_tree.column("Date Published", anchor=W, width=100)
        self.main_tree.column("Genre", anchor=W, width=100)
        self.main_tree.column("My Rating", anchor=W, width=80)

        self.main_tree.heading("#0", text="label", anchor=W)
        self.main_tree.heading("Book Title", text="Book Title", anchor=W)
        self.main_tree.heading("Author", text="Author", anchor=W)
        self.main_tree.heading("Pages", text="Pages", anchor=W)
        self.main_tree.heading("Date Published", text="Date Published", anchor=W)
        self.main_tree.heading("Genre", text="Genre", anchor=W)
        self.main_tree.heading("My Rating", text="My Rating", anchor=W)
        self.main_tree.pack(pady=20)
        
        delete_selected = Button(self, text="Delete Selected Books", width=50, command=lambda: self.remove_from_list())
        delete_selected.pack(pady=10)

        update_button = Button(self, text="Update Selected Book", width=50, command=self.show_update_menu)
        update_button.pack(pady=10)

        find_book = Button(self, text="Find A Book", width=50, command=self.show_find_menu )
        find_book.pack(pady=10)

        add_book_button = Button(self, text="Add A Book", width=50, command=self.show_add_menu)
        add_book_button.pack(pady=10)

        self.query_all_books()

    def set_up_db(self):
        conn = sqlite3.connect(self.db_file_name)
        c = conn.cursor()

        c.execute("""CREATE TABLE if not exists book_list (
            title text,
            author text,
            page_count integer,
            published_date integer,
            genre text DEFAULT '-',
            my_rating text DEFAULT '-',
            thumbnail_url text )""")

        conn.commit()
        conn.close()

    def query_all_books(self):
        try:
            conn = sqlite3.connect(self.db_file_name)
            c = conn.cursor()
            c.execute("SELECT *, oid FROM book_list")
            records = c.fetchall()
            conn.close()
            
            for record in records:
                oid = record[7]
                self.main_tree.insert(parent='', index='end', iid=oid, text="Parent", values=(record[:6]))

        except Exception as e:
            print(e)
    
    
    def remove_from_list(self):
        delete_list = self.main_tree.selection()
        for book_oid in delete_list:
            self.main_tree.delete(book_oid)
            self.delete_book(book_oid)

    def delete_book(self, book_oid):
        conn = sqlite3.connect(self.db_file_name)
        c = conn.cursor()
        c.execute("DELETE FROM book_list WHERE oid = (:selected_id)", 
        {
            'selected_id': book_oid
        })
        conn.commit()

    def show_add_menu(self):
        add_menu.AddMenu(self.main_tree, self.db_file_name)
    
    def show_update_menu(self):
        update_menu.UpdateMenu(self.main_tree, self.db_file_name)

    def show_find_menu(self):
        find_menu.FindMenu(self.main_tree, self.db_file_name)



if __name__ == "__main__":
    root = Tk()
    root.title('Book Tracker')
    root.geometry("800x460")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
