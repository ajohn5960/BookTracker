from tkinter import *
from tkinter import ttk
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import numpy as np

class StatsMenu(Frame):
    def __init__(self, root, *args, **kwargs):
        self.root = root

        main_menu = Menu(root)
        root.config(menu=main_menu)

        file_menu = Menu(main_menu)
        main_menu.add_cascade(label="Get Stats", menu=file_menu)
        file_menu.add_cascade(label="Books By Genre Pie Chart", command=self.show_pie_chart)
        file_menu.add_cascade(label="Books By Rating Bar Graph", command=self.show_bar_graph)
        file_menu.add_cascade(label="Books By Count Page Table", command=self.show_pages_table)


    def show_pie_chart(self):
        genre_list = self.query_all_genre()
        test = self.genre_list_to_dict(genre_list)
        print(test)
        genre_list = self.tuple_to_list(genre_list)
        genre_dict = self.book_count_by_genre(genre_list)
        
            
        if genre_dict.get("-") != None:
            genre_dict["Genre Not Specified"] = genre_dict.pop("-", "")

        labels = genre_dict.keys()

        num_books_per_genre = []
        for genre in genre_dict:
            num_books_per_genre.append(genre_dict.get(genre))

        fig1, ax1 = plt.subplots()

        wedges1, texts1, autotexts1= ax1.pie(num_books_per_genre,autopct=lambda pct: self.format_wedge_label(pct, num_books_per_genre),  
                shadow=True, startangle=90,  textprops=dict(color="black"), center=(3, 3))


        ax1.axis('equal') 
        ax1.set_title("Percentage of Books Read in Each Genre (Number of Books)")


        ax1.legend(wedges1, labels,
                title="Genre",
                bbox_to_anchor=[0.75, 0.5], loc='center left')
        plt.show()

    def query_all_genre(self):
        try:
            conn = sqlite3.connect('book_list.db')
            c = conn.cursor()
            c.execute('''
                SELECT genre 
                FROM book_list
            ''')
            genre_list = c.fetchall()
            conn.close()
            return genre_list

        except Exception as e:
            print(e)

    def tuple_to_list(self, genre_list):
        final_list = []
        for genre_tuple in genre_list:
            if isinstance(genre_tuple, str):
                final_list.append(genre_tuple)
            else:
                for genre in genre_tuple:
                    final_list.append(genre)
        return final_list

  
    def book_count_by_genre(self, genre_list):
        genre_dict = { }
        for genre in genre_list:
            if genre_dict.get(genre) == None:
                genre_dict[genre] = 1
            else:
                genre_dict[genre] += 1
        
        return genre_dict


    def format_wedge_label(self, pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return "{:.1f}%\n({:d} )".format(pct, absolute)    

    def show_bar_graph(self):
        test_list = self.query_all_ratings()
        ratings_dict = self.num_books_per_rating(test_list)

        labels = ratings_dict.keys()
        values = ratings_dict.values()

        x = np.arange(len(labels))  # the label locations

        fig, ax = plt.subplots()
        rects1 = ax.bar( x, height = values, width=0.8, bottom=0,align='center', data=values)

        ax.set_ylabel('Number of Books')
        ax.set_xlabel('My Rating')
        ax.set_title('Number of Books Per Rating')
        ax.set_xticks(x)

        ax.set_xticklabels(fontsize = 10, labels=labels,  ha='center')
        plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places

    
        self.autolabel(rects1, ax)
        fig.tight_layout()

        plt.show()

    def query_all_ratings(self):
        try:
            conn = sqlite3.connect('book_list.db')
            c = conn.cursor()
            c.execute('''
                SELECT my_rating 
                FROM book_list
            ''')
            records = c.fetchall()
            conn.close()
            return records

        except Exception as e:
            print(e)

    def num_books_per_rating(self, ratings_list):
        rating_not_specified = 'Rating Not Specified'
        ratings_dict = { '1': 0, '2': 0, '3': 0, '4':0, '5':0, rating_not_specified: 0}
        for ratings_tuple in ratings_list:
                for rating in ratings_tuple:
                    if ratings_dict.get(rating) != None:
                        ratings_dict[rating] += 1
                    if rating == '-':
                        ratings_dict[rating_not_specified] += 1
        return ratings_dict

    def autolabel(self,rects, ax):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    
   
      
    def show_pages_table(self):
        page_list = self.query_all_page_count()
        data_list = self.books_per_pages1(page_list)
        columns = ( 'Pages', 'Books')

        light_shadow = 'gainsboro'
        col_header_colors = ('lightsteelblue', 'lightsteelblue')
        cell_colors = []
        light_color_row = ['white', 'white'] 
        shadow_color_row =  [light_shadow, light_shadow]


        for num_rows in range(0, int(len(data_list))):
            if num_rows%2 == 0:
                    cell_colors.append(light_color_row)
            else:
                    cell_colors.append(shadow_color_row)
                

        fig, ax = plt.subplots()
        table = plt.table(cellText=data_list,
                    cellLoc='center',
                    cellColours = cell_colors,
                colLabels=columns, colColours=col_header_colors,  loc='upper center')

        table.scale(1, 3)

        label_str = self.find_max_and_min(page_list)
        ax.legend( title=label_str , bbox_to_anchor=(0.7, 1.16), loc='upper left') # right next to title
        plt.title('Pages Per Book')
        plt.axis("off")
        plt.show()

    def query_all_page_count(self):
        try:
            conn = sqlite3.connect('book_list.db')
            c = conn.cursor()
            c.execute('''
                SELECT page_count 
                FROM book_list
            ''')
            records = c.fetchall()
            conn.close()
            return records

        except Exception as e:
            print(e)

    def books_per_pages1(self,pages_list):
        pages_not_specified = 'Pages Not Specified'

        range1 = '< 200'
        range2 = '201 - 300'
        range3 = '301 - 400'
        range4 = '401 - 500'
        range5 = '501 - 600'
        range6 = '> 600'
        
        pages_array =   [[range1, 0], [range2, 0], [range3, 0], [range4, 0], [range5, 0], [range6, 0], [pages_not_specified, 0]]

        for pages_tuple in pages_list:
                for page_count in pages_tuple:
                    if page_count == '-':
                            pages_array[6][1] += 1
                            continue
                    
                    page_count = int(page_count)
                    if page_count <= 200:
                            pages_array[0][1] += 1
                    if 201 <= page_count <= 300:
                            pages_array[1][1] += 1
                    if 301 <= page_count <= 400:
                            pages_array[2][1] += 1
                    if 401 <= page_count <= 500:
                            pages_array[3][1] += 1
                    if 501 <= page_count <= 600:
                            pages_array[4][1] += 1
                    if page_count >= 600:
                            pages_array[5][1] += 1
                                            
        return pages_array
    
    def find_max_and_min(self, pages_list):
        max_page_count = 0
        min_page_count = sys.maxsize
        total_pages = 0
        for pages_tuple in pages_list:
            for page_count in pages_tuple:
                    if page_count != '-':
                        max_page_count = max(max_page_count, page_count)
                        min_page_count = min(min_page_count, page_count )
                        total_pages += page_count
        label_str = "Max Pages: " + str(max_page_count) + "\nMin Pages: " + str(min_page_count) +"\nTotal Pages: " + str(total_pages) 
        return label_str
