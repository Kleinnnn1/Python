# modules to be used
import tkinter as tk
import sqlite3

# clear the previous widgets when showing the inserted records
def clear_frame():
    for widgets in root.winfo_children():
        widgets.destroy()

# create database
def create_db():
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('dbactivity3.db')
        sqlite_create_table_query = '''CREATE TABLE tblusers(
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   first_name TEXT NOT NULL,
                                   last_name TEXT NOT NULL,
                                   email_address TEXT NOT NULL
                                   );'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")


# insert data into the database
def insert_data():
    global first_name, last_name, email_address, sqliteConnection
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email_address = last_name_entry.get()

    try:
        sqliteConnection = sqlite3.connect('dbactivity3.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """INSERT INTO tblusers
                             (first_name, last_name, email_address) 
                              VALUES 
                             (?, ?, ?)"""
        data_tuple = (first_name, last_name, email_address)

        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

    # clear the entry fields after submission
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    email_address_entry.delete(0, tk.END)


# retrieve data from the database
def read_data():
    global sqliteConnection
    try:
        clear_frame()
        root.geometry("300x300")
        sqliteConnection = sqlite3.connect('dbactivity3.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT *, DATE('now','localtime') from tblusers"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")

        activity_label = tk.Label(root, text="RECORDS IN DATABASE")
        activity_label.grid(row=0, column=0, padx=0, pady=2)

        listbox = tk.Listbox(root, height=17, width=50)
        for row in records:
            listbox.insert(tk.END, f"ID: {row[0]}")
            listbox.insert(tk.END, f"First Name: {row[1]}")
            listbox.insert(tk.END, f"Last Name: {row[2]}")
            listbox.insert(tk.END, f"Email Address: {row[3]}")
            listbox.insert(tk.END, f"Record Created: {row[4]}")
            listbox.insert(tk.END, "")
        listbox.grid()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


# root Graphical User Interface
global root
root = tk.Tk()
root.title("Act3")
root.eval('tk::PlaceWindow . center')
root.geometry("300x200")

activity_label = tk.Label(root, text="USER REGISTRATION")
activity_label.grid(row=1, column=1, padx=0, pady=5)

# Create the first name entry field
first_name_label = tk.Label(root, text="First Name:")
first_name_label.grid(row=2, column=0, padx=5, pady=5)
first_name_entry = tk.Entry(root)
first_name_entry.grid(row=2, column=1, padx=5, pady=5)

# Create the last name entry field
last_name_label = tk.Label(root, text="Last Name:")
last_name_label.grid(row=3, column=0, padx=5, pady=5)
last_name_entry = tk.Entry(root)
last_name_entry.grid(row=3, column=1, padx=5, pady=5)

# Create the ID entry field
email_address_label = tk.Label(root, text="Email Address:")
email_address_label.grid(row=4, column=0, padx=5, pady=5)
email_address_entry = tk.Entry(root)
email_address_entry.grid(row=4, column=1, padx=5, pady=5)

# Create the submit button
submit_button = tk.Button(root, text="Submit", command=insert_data, bg="green", fg="white")
submit_button.grid(row=6, column=1, pady=5)

# Create the show records button
show_button = tk.Button(root, text="Show Records", command=read_data, bg="blue", fg="white")
show_button.grid(row=8, column=1)
root.mainloop()
