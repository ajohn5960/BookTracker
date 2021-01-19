from tkinter import *
from tkinter import ttk
import sqlite3

class AddMenu(Frame):
    def __init__(self, main_tree, db_file_name, *args, **kwargs):
        self.main_tree = main_tree
        self.db_file_name = db_file_name
        self.add_menu = Tk()
        self.add_menu.title('Add A Book')

        self.title_label = Label(self.add_menu, text="Book Title: ", padx=10)
        self.title_label.grid(row=0, column=0)

        self.title= Entry(self.add_menu, width=50)
        self.title.grid(row=0, column=1,  padx=20, pady=10)

        self.author_label = Label(self.add_menu, text="Author Name: ", padx=10)
        self.author_label.grid(row=1, column=0)

        self.author = Entry(self.add_menu, width=50)
        self.author.grid(row=1, column=1,  padx=20, pady=10)

        self.pages_label = Label(self.add_menu, text="Number of Pages: ", padx=10)
        self.pages_label.grid(row=2, column=0)

        self.pages = Entry(self.add_menu, width=50)
        self.pages.grid(row=2, column=1,  padx=20, pady=10)

        self.published_date_label = Label(self.add_menu, text="Date Published: ", padx=10)
        self.published_date_label.grid(row=3, column=0)

        self.published_date = Entry(self.add_menu, width=50)
        self.published_date.grid(row=3, column=1,  padx=20, pady=10)

        self.genre_label = Label(self.add_menu, text="Genre: ", padx=10)
        self.genre_label.grid(row=4, column=0)

        self.genre = Entry(self.add_menu, width=50)
        self.genre.grid(row=4, column=1,  padx=20, pady=10)
        
        self.rating_label = Label(self.add_menu, text="My Rating: ", padx=10)
        self.rating_label.grid(row=5, column=0)

        self.frame = Frame(self.add_menu)
        self.frame.grid(row=5, column=1, padx=20, pady=10)

        self.selected_rating =IntVar()
        self.selected_rating.set(1)
        
        self.one = Radiobutton(self.frame, text=str(1),variable=self.selected_rating, value=1, command=lambda: self.selected_rating.set(1))
        self.one.grid(row=0, column=0, padx=5, pady=10)

        self.two = Radiobutton(self.frame, text=str(2),variable=self.selected_rating, value=2, command=lambda: self.selected_rating.set(2))
        self.two.grid(row=0, column=1, padx=5, pady=10)

        self.three = Radiobutton(self.frame, text=str(3),variable=self.selected_rating, value=3, command=lambda: self.selected_rating.set(3))
        self.three.grid(row=0, column=2, padx=5, pady=10)

        self.four = Radiobutton(self.frame, text=str(4),variable=self.selected_rating, value=4, command=lambda: self.selected_rating.set(4))
        self.four.grid(row=0, column=4, padx=5, pady=10)

        self.five = Radiobutton(self.frame, text=str(5),variable=self.selected_rating, value=5, command=lambda: self.selected_rating.set(5))
        self.five.grid(row=0, column=5, padx=5, pady=10)

        add_button = Button(self.add_menu, text="Add Book To List", width=50,  command=lambda: self.get_book_info())
        add_button.grid(row=6, column=0, columnspan=2, pady=10)
    

    def get_book_info(self):
        title = self.title.get()
        author = self.author.get()
        pages = int (self.pages.get())
        published_date = int(self.published_date.get())
        genre = self.genre.get()
        rating = self.selected_rating.get()
        url = " "
        record = [title, author, pages, published_date, genre, rating, url ]
        self.add_book(record)
        
        self.add_menu.destroy()

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