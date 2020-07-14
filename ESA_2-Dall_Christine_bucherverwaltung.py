#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tk_grid1.py

from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter.messagebox import *


# Class Manages the book database
class DbBooks:

    # Method Creates the database
    def db_create_table_books(self):

        sql_command = '''
            CREATE TABLE IF NOT EXISTS books(
            nr INTEGER PRIMARY KEY,
            titel VARCHAR(50), 
            autor VARCHAR(30),
            serie VARCHAR(30),
            bemerkung text
            );
        '''
        c = self.cursor()
        c.execute(sql_command)
        self.commit()

    # Method Adds a new record
    def db_insert_book(titel, autor, serie, bemerkung):
        DB_NAME = 'db_books.sqlite'
        db = sqlite3.connect(DB_NAME)

        c = db.cursor()
        sql_command = '''
        INSERT INTO books(titel, autor, serie, bemerkung) VALUES (?, ?, ?, ?);
        '''
        c.execute(sql_command, (titel, autor, serie, bemerkung[:40]))

        db.commit()

    # Method Changes a record
    def db_update_book(nr, titel, autor, serie, bemerkung):
        DB_NAME = 'db_books.sqlite'
        db = sqlite3.connect(DB_NAME)
        c = db.cursor()

        if titel != '':
            c.execute("UPDATE books SET titel=? WHERE nr=?", (titel, nr))
        if autor != '':
            c.execute("UPDATE books SET autor=? WHERE nr=?", (autor, nr))
        if serie != '':
            c.execute("UPDATE books SET serie=? WHERE nr=?", (serie, nr))
        if bemerkung != '':
            c.execute("UPDATE books SET bemerkung=? WHERE nr=?", (bemerkung, nr))

        db.commit()

    # Method deletes a record
    def db_delete_book(nr):
        DB_NAME = 'db_books.sqlite'
        db = sqlite3.connect(DB_NAME)

        c = db.cursor()
        c.execute("DELETE FROM books WHERE nr=?", (nr,))

        db.commit()

    # Method return all entrys
    def db_return_all_entrys_book(self):
        DB_NAME = 'db_books.sqlite'
        db = sqlite3.connect(DB_NAME)

        sql_command = 'SELECT * FROM books'
        c = db.cursor()
        c.execute(sql_command)
        return c.fetchall()

        db.commit()

    # Method checks id valid
    def db_check_id_valid(self):
        DB_NAME = 'db_books.sqlite'
        db = sqlite3.connect(DB_NAME)

        try:
            c = db.cursor()
            c.execute("SELECT * FROM books WHERE nr =?", (self))
            # print(c.fetchone())
            db.commit()
        except Exception as e:
            showerror("Warnung", "Eingabefehler, die eingebende Nummer ist nicht vorhanden.")


    # Method outputs all entries
    @staticmethod
    def db_print_table_books():

        DB_NAME = 'db_books.sqlite'
        db = sqlite3.connect(DB_NAME)

        sql_command = 'SELECT * FROM books'
        c = db.cursor()
        c.execute(sql_command)
        data = c.fetchall()

        for row in data:
            nr, titel, autor, serie, bemerkung = row
            print(f' {nr} {titel} {autor} {serie} {bemerkung} ')


# Class internalized windows
class BookApp(Tk):

    # Method internalizes start Frame
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    # Method internalizes frame
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


# Class StartPage
class StartPage(Frame):

    # method init
    def __init__(self, master):
        DB_NAME = 'db_books.sqlite'
        db = sqlite3.connect(DB_NAME)

        Frame.__init__(self, master)
        Frame.configure(self, bg='blue')

        Label(self, text="Büchervewaltung", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        Label(self, text="Menü", font=('Helvetica', 12, "bold")).pack(fill="x", pady=5)

        # Buttons "Buch hinzufügen", "Buch ändern" and "Buch löschen"
        Button(self, text="Buch hinzufügen", fg="blue",
               command=lambda: master.switch_frame(PageNewBook)).pack(fill=X)
        Button(self, text="Buch ändern", fg="blue",
               command=lambda: master.switch_frame(PageUpdateBook)).pack(fill=X)
        Button(self, text="Buch löschen", fg="blue",
               command=lambda: master.switch_frame(PageDeleteBook)).pack(fill=X)

        Label(self, text="Eingetragende Bücher", font=('Helvetica', 14, "bold")).pack(fill="x", pady=15)

        frame_overview_books = Frame(self)
        frame_overview_books.pack()

        list_books = ttk.Treeview(frame_overview_books, columns=(1, 2, 3, 4, 5), height=10, show="headings")
        list_books.pack(side='left')

        list_books.heading(1, text="Nr")
        list_books.heading(2, text="Titel")
        list_books.heading(3, text="Autor")
        list_books.heading(4, text="Serie")
        list_books.heading(5, text="Bemerkung")

        list_books.column(1, width=40)
        list_books.column(2, width=100)
        list_books.column(3, width=100)
        list_books.column(4, width=100)
        list_books.column(5, width=200)

        scroll = ttk.Scrollbar(frame_overview_books, orient="vertical", command=list_books.yview)
        scroll.pack(side='right', fill='y')

        list_books.configure(yscrollcommand=scroll.set)

        # all book entry
        data = DbBooks.db_return_all_entrys_book(db)

        for content in data:
            list_books.insert('', 'end', values=(content[0], content[1], content[2], content[3], content[4]))


# class add new book Frame
class PageNewBook(Frame):

    # Method init Frame
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self, bg='blue')

        # Method checks whether author and title are given and inserts the entry in the database
        def insert_book(*args):
            if titel.get() != '' and autor.get() != '':
                DbBooks.db_insert_book(titel.get(), autor.get(), serie.get(), bemerkung.get())
                if askyesno('Buch hinzufügen', 'Weiteres Buch hinzufügen'):
                    pass
                else:
                    master.switch_frame(StartPage)
            else:
                showerror("Warnung", "Eingabefehler, Buchitel oder/und Autor nicht eingeben.")

        Label(self, text="Neues Buch hinzufügen", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        frame_add_book = ttk.Frame(self, borderwidth=1, relief='sunken', \
                                   width=600, height=250, padding='80 20 80 20')
        frame_add_book.grid_propagate(0)
        frame_add_book.pack()

        titel = StringVar()
        autor = StringVar()
        serie = StringVar()
        bemerkung = StringVar()

        # Entry Titel
        label_titel = ttk.Label(frame_add_book, text='Buch Titel:* ')
        label_titel.grid(row=0, column=0, sticky=W, padx=5, pady=5)

        entry_titel = ttk.Entry(frame_add_book, textvariable=titel)
        entry_titel.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        entry_titel.focus()

        # Entry Autor
        label_autor = ttk.Label(frame_add_book, text='Autor:* ')
        label_autor.grid(row=0, column=2, sticky=W, padx=5, pady=5)

        entry_autor = ttk.Entry(frame_add_book, textvariable=autor)
        entry_autor.grid(row=0, column=3, sticky=W, padx=5, pady=5)
        entry_autor.focus()

        # Entry Serie
        label_serie = ttk.Label(frame_add_book, text='Buch Serie: ')
        label_serie.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        entry_serie = ttk.Entry(frame_add_book, textvariable=serie)
        entry_serie.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        entry_serie.focus()

        # Entry bemerkung
        label_bemerkung = ttk.Label(frame_add_book, text='Bemerkung: ')
        label_bemerkung.grid(row=1, column=2, sticky=W, padx=5, pady=5)

        entry_bemerkung = ttk.Entry(frame_add_book, textvariable=bemerkung, width=20)
        entry_bemerkung.grid(row=1, column=3, sticky=W, padx=5, pady=5)
        entry_bemerkung.focus()

        label_mandatory = ttk.Label(frame_add_book, text='* Pflichtfelder')
        label_mandatory.grid(row=3, column=0, sticky=W, padx=5, pady=5)

        # button
        button_1 = ttk.Button(frame_add_book, text='Buch hinzufügen', command=insert_book)
        button_1.grid(row=4, column=1, sticky=W, padx=5, pady=5)

        self.bind('<Return>', insert_book)

        Button(self, text="Zurück zur Übersicht",
               command=lambda: master.switch_frame(StartPage)).pack()


# class Frame update book
class PageUpdateBook(Frame):
    # method init frame
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self, bg='blue')
        Label(self, text="Eintrag ändern", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        # Method checks whether numbers are given and changes the entry to database
        def update_book(*args):
            if nr.get() != '':
                DbBooks.db_check_id_valid(nr.get())
                DbBooks.db_update_book(nr.get(), titel.get(), autor.get(), serie.get(), bemerkung.get())
                if askyesno('Buch ändern', 'Weiteres Buch ändern'):
                    pass
                else:
                    master.switch_frame(StartPage)
            else:
                showerror("Warnung", "Buch-Nr. nicht eingeben.")

        Label(self, text="Neues Buch hinzufügen", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        frame_add_book = ttk.Frame(self, borderwidth=1, relief='sunken', \
                                   width=600, height=250, padding='80 20 80 20')
        frame_add_book.grid_propagate(0)
        frame_add_book.pack()

        nr = StringVar()
        titel = StringVar()
        autor = StringVar()
        serie = StringVar()
        bemerkung = StringVar()

        Label(self, text="Es müssen nur die zu geänderten Daten und die Buch-Nr. eingeben werden.",
              font=('Helvetica', 10, "bold")).pack(side="top", fill="x", pady=5)

        # Entry Nr
        label_titel = ttk.Label(frame_add_book, text='Buch Nr. *: ')
        label_titel.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        entry_titel = ttk.Entry(frame_add_book, textvariable=nr)
        entry_titel.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        entry_titel.focus()

        # Entry Titel
        label_titel = ttk.Label(frame_add_book, text='Buch Titel: ')
        label_titel.grid(row=2, column=0, sticky=W, padx=5, pady=5)

        entry_titel = ttk.Entry(frame_add_book, textvariable=titel)
        entry_titel.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        entry_titel.focus()

        # Entry Autor
        label_autor = ttk.Label(frame_add_book, text='Autor: ')
        label_autor.grid(row=2, column=2, sticky=W, padx=5, pady=5)

        entry_autor = ttk.Entry(frame_add_book, textvariable=autor)
        entry_autor.grid(row=2, column=3, sticky=W, padx=5, pady=5)
        entry_autor.focus()

        # Entry Serie
        label_serie = ttk.Label(frame_add_book, text='Buch Serie: ')
        label_serie.grid(row=3, column=0, sticky=W, padx=5, pady=5)

        entry_serie = ttk.Entry(frame_add_book, textvariable=serie)
        entry_serie.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        entry_serie.focus()

        # Entry bemerkung
        label_bemerkung = ttk.Label(frame_add_book, text='Bemerkung: ')
        label_bemerkung.grid(row=3, column=2, sticky=W, padx=5, pady=5)

        entry_bemerkung = ttk.Entry(frame_add_book, textvariable=bemerkung, width=20)
        entry_bemerkung.grid(row=3, column=3, sticky=W, padx=5, pady=5)
        entry_bemerkung.focus()

        # label Pflichtfelder
        label_mandatory = ttk.Label(frame_add_book, text='* Pflichtfelder')
        label_mandatory.grid(row=4, column=0, sticky=W, padx=5, pady=5)

        # button
        button_1 = ttk.Button(frame_add_book, text='Buch ändern', command=update_book)
        button_1.grid(row=4, column=1, sticky=W, padx=5, pady=5)

        self.bind('<Return>', update_book)

        Button(self, text="Zurück zur Übersicht",
               command=lambda: master.switch_frame(StartPage)).pack()


# class Frame delete Book
class PageDeleteBook(Frame):
    # method init
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self, bg='blue')
        Label(self, text="Buch löschen", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        # method checks whether a number has been entered
        def delete_book(*args):
            if nr.get() != '':
                DbBooks.db_check_id_valid(nr.get())
                DbBooks.db_delete_book(nr.get())
                if askyesno('Buch löschen', 'Weiteres Buch löschen'):
                    pass
                else:
                    master.switch_frame(StartPage)
            else:
                showerror("Warnung", "Buch-Nr. nicht eingeben.")

        Label(self, text="Neues Buch hinzufügen", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        frame_delete_book = ttk.Frame(self, borderwidth=1, relief='sunken', \
                                      width=600, height=250, padding='80 20 80 20')
        frame_delete_book.grid_propagate(0)
        frame_delete_book.pack()

        nr = StringVar()

        # Entry Titel
        label_delet_nr = ttk.Label(frame_delete_book, text='Nr. des Buches : ')
        label_delet_nr.grid(row=0, column=0, sticky=W, padx=5, pady=5)

        entry_delet_nr = ttk.Entry(frame_delete_book, textvariable=nr)
        entry_delet_nr.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        entry_delet_nr.focus()

        # button
        button_1 = ttk.Button(frame_delete_book, text='Buch löschen', command=delete_book)
        button_1.grid(row=3, column=1, sticky=W, padx=5, pady=5)

        Button(self, text="Zurück zur Übersicht",
               command=lambda: master.switch_frame(StartPage)).pack()


if __name__ == "__main__":
    WINDOW_TITEL = 'Buchverwaltung'
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 400

    # new Database
    DB_NAME = 'db_books.sqlite'
    db = sqlite3.connect(DB_NAME)
    DbBooks.db_create_table_books(db)

    #DbBooks.db_insert_book('Die Wächter', 'John Grisham', '', '')
    #DbBooks.db_insert_book('Die Sonnenschwester', 'Lucinda Riley', 'Band 6', '')
    #DbBooks.db_insert_book('Der Insasse', 'Sebastian Fitzek', '', 'geschenkt bekommen')

    root = BookApp()
    root.title(WINDOW_TITEL)
    root.geometry("{}x{}".format(WINDOW_WIDTH, WINDOW_HEIGHT))

    root.mainloop()
