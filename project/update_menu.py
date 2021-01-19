from tkinter import *
from tkinter import ttk
import sqlite3

class UpdateMenu(Frame):
    def __init__(self, main_tree, db_file_name, *args, **kwargs):
        self.editor = Tk()
        self.editor.title('Update A Book')
        self.main_tree = main_tree
        self.db_file_name = db_file_name
        conn = sqlite3.connect(db_file_name)
        c = conn.cursor()
        

        try: 
            self.book_oid = main_tree.focus()
            c.execute("SELECT *, oid FROM book_list WHERE oid = (:book_id)", 
                    {
                        'book_id': self.book_oid
                    })
            records = c.fetchall()

            title_label = Label(self.editor, text="Book Title: ", padx=10)
            title_label.grid(row=0, column=0)

            self.title= Entry(self.editor, width=50)
            self.title.grid(row=0, column=1,  padx=20, pady=10)

            author_label = Label(self.editor, text="Author Name: ", padx=10)
            author_label.grid(row=1, column=0)

            self.author = Entry(self.editor, width=50)
            self.author.grid(row=1, column=1,  padx=20, pady=10)

            pages_label = Label(self.editor, text="Number of Pages: ", padx=10)
            pages_label.grid(row=2, column=0)

            self.page_count = Entry(self.editor, width=50)
            self.page_count.grid(row=2, column=1,  padx=20, pady=10)

            published_date_label = Label(self.editor, text="Date Published: ", padx=10)
            published_date_label.grid(row=3, column=0)

            self.published_date = Entry(self.editor, width=50)
            self.published_date.grid(row=3, column=1,  padx=20, pady=10)

            genre_label = Label(self.editor, text="Genre: ", padx=10)
            genre_label.grid(row=4, column=0)

            self.genre = Entry(self.editor, width=50)
            self.genre.grid(row=4, column=1,  padx=20, pady=10)

            rating_label = Label(self.editor, text="Rating: ", padx=10)
            rating_label.grid(row=5, column=0)

            frame = Frame(self.editor)
            frame.grid(row=5, column=1, padx=20, pady=10)

            self.selected_rating =IntVar()
            self.selected_rating.set(None)

            one = Radiobutton(frame, text=str(1),variable=self.selected_rating, value=1, command=lambda: self.selected_rating.set(1))
            one.grid(row=0, column=0, padx=5, pady=10)
        

            two = Radiobutton(frame, text=str(2),variable=self.selected_rating, value=2, command=lambda: self.selected_rating.set(2))
            two.grid(row=0, column=1, padx=5, pady=10)

            three = Radiobutton(frame, text=str(3),variable=self.selected_rating, value=3, command=lambda: self.selected_rating.set(3))
            three.grid(row=0, column=2, padx=5, pady=10)

            four = Radiobutton(frame, text=str(4),variable=self.selected_rating, value=4, command=lambda: self.selected_rating.set(4))
            four.grid(row=0, column=4, padx=5, pady=10)

            five = Radiobutton(frame, text=str(5),variable=self.selected_rating, value=5, command=lambda: self.selected_rating.set(5))
            five.grid(row=0, column=5, padx=5, pady=10)

            self.title.insert(0, records[0][0])
            self.author.insert(0, records[0][1])
            self.page_count.insert(0, records[0][2])
            self.published_date.insert(0, records[0][3])
            self.genre.insert(0, records[0][4])

           
            save_button = Button(self.editor, text="Save", width=50,  command=lambda: self.update_tree())
            save_button.grid(row=6, column=0, columnspan=2, pady=10)

        except Exception as e:
            print(e)


    def update_tree(self):
        page_count = self.page_count.get()

        if self.is_valid_page(page_count):
            page_count = int(page_count)
        else:
            page_count = '-'

        record = [ self.title.get(),
                    self.author.get(),
                    page_count,
                    self.published_date.get(),
                    self.genre.get(),
                    self.selected_rating.get()]
        ttk.Treeview.item( self.main_tree, self.book_oid, values=(record))
        self.update_book(self.book_oid, record)

        self.editor.destroy()

    def update_book(self, book_oid, record):
        conn = sqlite3.connect(self.db_file_name)
        c = conn.cursor()
        c.execute("""UPDATE book_list SET
                title = :title,
                author = :author,
                page_count = :page_count,
                published_date = :published_date,
                genre = :genre,
                my_rating = :my_rating

                WHERE oid = :book_id""", 
                {
                    'title': record[0],
                    'author' : record[1],
                    'page_count' : record[2],
                    'published_date' : record[3],
                    'genre' : record[4], 
                    'my_rating' : record[5],
                    'book_id' : book_oid
                })

        conn.commit()
        conn.close()

    def is_valid_page(self,value):
        try:
            value = int(value)
            if value >= 0:
                return True
            else:
                return False
        except ValueError:
            return False