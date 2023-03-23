# import tkinter
# root = tkinter.Tk()
# root.title("Act3")
# root.eval('tk::PlaceWindow . center')
# root.geometry("300x300")
#
# tkinter.Label(root, text="Employee ID").place(x=10, y=10)
# tkinter.Label(root, text="Employee First Name").place(x=10, y=40)
# tkinter.Label(root, text="Employee Last Name").place(x=10, y=70)
#
# e1 = tkinter.Entry(root)
# e1.place(x=140, y=10)
#
# e2 = tkinter.Entry(root)
# e2.place(x=140, y=40)
#
# e3 = tkinter.Entry(root)
# e3.place(x=140, y=70)
#
# e4 = tkinter.Entry(root)
# e4.place(x=140, y=100)
#
# tkinter.Button(root, text="Add", height=3, width=13).place(x=30, y=130)
# tkinter.Button(root, text="update", height=3, width=13).place(x=140, y=130)
# # Code to add widgets will go here...
# root.mainloop()
import tkinter as tk
import sqlite3


def createdb():
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('dbactivity3.db')
        sqlite_create_table_query = '''CREATE TABLE tblusers (
                                   employee_id TEXT PRIMARY KEY,
                                   employee_fname TEXT NOT NULL,
                                   employee_lname TEXT NOT NULL 
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


def submit_data():
    global employee_id, first_name, last_name, sqliteConnection
    employee_id = id_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()

    # Do something with the data, such as inserting it into a database
    try:
        sqliteConnection = sqlite3.connect('dbactivity3.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """INSERT INTO tblusers
                             (employee_id, employee_fname, employee_lname) 
                              VALUES 
                             (?, ?, ?)"""
        data_tuple = (employee_id, first_name, last_name)

        count = cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

    # Clear the entry fields after submission
    id_entry.delete(0, tk.END)
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)

def readSqliteTable():

   try:
       window = tk.Tk()
       window.title("SQLite Data")
       window.eval('tk::PlaceWindow . center')
       window.geometry("300x300")

       sqliteConnection = sqlite3.connect('dbactivity3.db')
       cursor = sqliteConnection.cursor()
       print("Connected to SQLite")

       sqlite_select_query = """SELECT * from tblusers"""
       cursor.execute(sqlite_select_query)
       records = cursor.fetchall()
       print("Total rows are:  ", len(records))
       print("Printing each row")
       a=1

       listbox = tk.Listbox(window, height=20, width=50)
       label = tk.Label(window, text="SQLite Data")
       label.pack()
       for row in records:
           listbox.insert(tk.END, f"Name: {row[0]}")
           listbox.insert(tk.END, f"Age: {row[1]}")
           listbox.insert(tk.END, f"City: {row[2]}")
           listbox.insert(tk.END, "")
       listbox.pack()
       cursor.close()

       window.mainloop()
   except sqlite3.Error as error:
       print("Failed to read data from sqlite table", error)
   finally:
       if sqliteConnection:
           sqliteConnection.close()
           print("The SQLite connection is closed")

root = tk.Tk()
root.title("Act3")
root.eval('tk::PlaceWindow . center')

# Create the ID entry field
id_label = tk.Label(root, text="Employee ID:")
id_label.grid(row=0, column=0, padx=5, pady=5)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1, padx=5, pady=5)

# Create the first name entry field
first_name_label = tk.Label(root, text="First Name:")
first_name_label.grid(row=1, column=0, padx=5, pady=5)
first_name_entry = tk.Entry(root)
first_name_entry.grid(row=1, column=1, padx=5, pady=5)

# Create the last name entry field
last_name_label = tk.Label(root, text="Last Name:")
last_name_label.grid(row=2, column=0, padx=5, pady=5)
last_name_entry = tk.Entry(root)
last_name_entry.grid(row=2, column=1, padx=5, pady=5)

# Create the submit button
submit_button = tk.Button(root, text="Submit", command=submit_data)
submit_button.grid(row=3, column=0, columnspan=2)

submit_button = tk.Button(root, text="Show", command=readSqliteTable)
submit_button.grid(row=4, column=0, columnspan=2)
root.mainloop()
