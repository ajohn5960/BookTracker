from tkinter import *
from tkinter import ttk
import sqlite3
from urllib.request import urlopen as uReq
import json
from dotenv import load_dotenv
load_dotenv()
import os

class FindMenu(Frame):
    def __init__(self, main_tree, db_file_name, *args, **kwargs):
        self.main_tree = main_tree
        self.find_menu = Tk()
        self.find_menu.title('Find A Book')
        self.db_file_name = db_file_name
        
        self.API_KEY = os.getenv("API_KEY")

        title_label = Label(self.find_menu, text="Book Title", padx=10)
        title_label.grid(row=0, column=0)

        self.title = Entry(self.find_menu, width=50)
        self.title.grid(row=0, column=1,  padx=20, pady=10)

        author_label = Label(self.find_menu, text="Author Name", padx=10)
        author_label.grid(row=1, column=0)

        self.author = Entry(self.find_menu, width=50)
        self.author.grid(row=1, column=1,  padx=20, pady=10)

        get_book_button = Button(self.find_menu, text="Search Books", width=50, command= self.show_search_result)
        get_book_button.grid(row=2, column=0, columnspan=2,  padx=20, pady=10)


        self.tree = ttk.Treeview(self.find_menu)
        self.tree['columns'] = ("Book Title", "Author", "Pages", "Date Published", "Genre")

        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("Book Title", anchor=W, width=120)
        self.tree.column("Author", anchor=CENTER, width=120)
        self.tree.column("Pages", anchor=W, width=80)
        self.tree.column("Date Published", anchor=W, width=100)
        self.tree.column("Genre", anchor=W, width=100)

        self.tree.heading("#0", text="label", anchor=W)
        self.tree.heading("Book Title", text="Book Title", anchor=W)
        self.tree.heading("Author", text="Author", anchor=CENTER)
        self.tree.heading("Pages", text="Pages", anchor=W)
        self.tree.heading("Date Published", text="Date Published", anchor=W)
        self.tree.heading("Genre", text="Genre", anchor=W)


    def show_search_result(self):
        try:
            self.tree.grid(row=3, column=0, columnspan =2, padx=20, pady=10)
    
            title_input = str(self.title.get())
            title_input = title_input.replace(" ", "+")

          
            author_input = str(self.author.get())
            author_input = author_input.replace(" ", "+")
            
            book_list = self.get_all_books(title_input, author_input)

            add_button = Button(self.find_menu, text="Add Selected To Book List", width=50, command=lambda: self.add_selected_books(self.tree.selection(), book_list) )
            add_button.grid(row=4, column=0, columnspan=2,  padx=20, pady=10)

        except Exception as e:
                print(e)


    def get_all_books(self, title_input, author_input):
        try:
            url = 'https://www.googleapis.com/books/v1/volumes?q={search_title}+inauthor:{search_author}&key={APIKey}'.format(search_title = title_input, search_author = author_input, APIKey = self.API_KEY)
            uClient = uReq(url)
            page_html = uClient.read()
            uClient.close()
            book_json = json.loads(page_html)

            book_list = []
            book_index = 0 

            for item in book_json["items"]:
                book_title = item["volumeInfo"].get("title", "-")
                book_authors = item["volumeInfo"].get("authors", "-")
                authors_str = ', '.join(book_authors)  
                book_authors = authors_str
                page_count = item["volumeInfo"].get("pageCount", "-")
                published_date =item["volumeInfo"].get("publishedDate", "-")
                if 'imageLinks' in item["volumeInfo"]:
                    thumbnail_url = item["volumeInfo"]["imageLinks"].get("smallThumbnail", "-")
                else:
                    thumbnail_url = " "
                genre_list = item["volumeInfo"].get("categories", "-")
                genre_str = ', '.join(genre_list)  
                my_rating = "-"
                
                book = [book_title, book_authors, page_count, published_date, genre_str,my_rating, thumbnail_url]
                book_list.append(book)
                self.tree.insert(parent='', index='end', iid = book_index , text="Parent", values=(book[:6]))
                book_index += 1

            return book_list

        except KeyError:
            print("KeyError")


    def add_selected_books(self, selected_books, book_list):
        for book_index in selected_books:
            index = int(book_index)
            self.add_book(book_list[index])
            self.find_menu.destroy()


    def add_book(self, record):
        try:
            conn = sqlite3.connect(self.db_file_name)
            c = conn.cursor()
            c.execute("INSERT INTO book_list VALUES (:add_book_title, :add_book_author, :add_page_count, :add_published_date, :add_genre, :add_rating, :add_thumbnail_url)",
                {
                    'add_book_title' : record[0],
                    'add_book_author' : record[1],
                    'add_page_count' : record[2],
                    'add_published_date' : record[3],
                    'add_genre' : record[4], 
                    'add_rating' : record[5],
                    'add_thumbnail_url' : record[6]
                })
            book_oid = c.lastrowid
            self.main_tree.insert(parent='', index='end', iid=book_oid, text="Parent", values=(record[:6]))
            conn.commit()
            conn.close()

        except Exception as e:
                print(e)


