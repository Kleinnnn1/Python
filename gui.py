# modules to be used
import tkinter as tk
import mysql.connector

# CREATE PROCESS - insert data into the database
def create_data_process():
    global first_name, last_name, email_address, mydb, id
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email_address = email_address_entry.get()

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbactivity4"
        )
        cursor = mydb.cursor()
        print("Successfully Connected to Mysql")

        sqlite_insert_query = """INSERT INTO tblusers
                             (first_name, last_name, email_address) 
                              VALUES 
                             (%s, %s, %s)"""
        data_tuple = (first_name, last_name, email_address)

        cursor.execute(sqlite_insert_query, data_tuple)
        mydb.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if mydb:
            mydb.close()
            print("The SQLite connection is closed")

    # clear the entry fields after submission
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    email_address_entry.delete(0, tk.END)

# UPDATE PROCESS - update the data from the database
def update_data_process():
    new_first_name = first_name_entry.get()
    new_last_name = last_name_entry.get()
    new_email_address = email_address_entry.get()
    id = id_entry.get()

    # Connect to the MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dbactivity4"
    )

    # Prepare the SQL statement to search for the record
    sql = "SELECT * FROM tblusers WHERE id = %s"
    m = (id,)

    # Execute the SQL statement
    mycursor = mydb.cursor()
    mycursor.execute(sql, m)
    result = mycursor.fetchone()

    # If the record is found, allow the user to update it
    if result:
        old_first_name = result[1]
        old_last_name = result[2]
        old_email_address = result[3]

        # Check if a new value is entered for each field
        if new_first_name == "":
            new_first_name = old_first_name
        if new_last_name == "":
            new_last_name = old_last_name
        if new_email_address == "":
            new_email_address = old_email_address

        # Prepare the SQL statement to update the record
        sql = "UPDATE tblusers SET first_name = %s, last_name = %s, email_address = %s WHERE id = %s"
        val = (new_first_name, new_last_name, new_email_address, id)

        # Execute the SQL statement
        mycursor.execute(sql, val)
        mydb.commit()

        print(mycursor.rowcount, "record(s) affected")
    else:
        print("Record not found")

    # Close the database connection
    mydb.close()

# DELETE PROCESS - delete a specific data from the database
def delete_data_process():
    id = id_entry.get()

    # Connect to the MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dbactivity4"
    )

    # Prepare the SQL statement to search for the record
    sql = "SELECT * FROM tblusers WHERE id = %s"
    m = (id,)

    # Execute the SQL statement
    mycursor = mydb.cursor()
    mycursor.execute(sql, m)
    result = mycursor.fetchone()

    # If the record is found, delete selected fields
    if result:
        if first_name_var.get() == 1:
            sql = "UPDATE tblusers SET first_name = NULL WHERE id = %s"
            mycursor.execute(sql, m)
            mydb.commit()

        if last_name_var.get() == 1:
            sql = "UPDATE tblusers SET last_name = NULL WHERE id = %s"
            mycursor.execute(sql, m)
            mydb.commit()

        if email_address_var.get() == 1:
            sql = "UPDATE tblusers SET email_address = NULL WHERE id = %s"
            mycursor.execute(sql, m)
            mydb.commit()

        print(mycursor.rowcount, "field(s) deleted")
    else:
        print("Record not found")

    # Close the database connection

# CREATE GUI
def create_data_gui():
    global first_name_entry, last_name_entry, email_address_entry
    creategui = tk.Tk()
    creategui.title("Insert Data")
    creategui.geometry("300x200")

    # Create the first name entry field

    activity_label = tk.Label(creategui, text="USER REGISTRATION", bg="#8BC34A", fg="white", font=("TkDefaultFont", 10, "bold"))
    activity_label.grid(row=1, column=1, padx=0, pady=5)

    first_name_label = tk.Label(creategui, text="First Name:")
    first_name_label.grid(row=2, column=0, padx=5, pady=5)
    first_name_entry = tk.Entry(creategui)
    first_name_entry.grid(row=2, column=1, padx=5, pady=5)

    # Create the last name entry field
    last_name_label = tk.Label(creategui, text="Last Name:")
    last_name_label.grid(row=3, column=0, padx=5, pady=5)
    last_name_entry = tk.Entry(creategui)
    last_name_entry.grid(row=3, column=1, padx=5, pady=5)

    # Create the email address entry field
    email_address_label = tk.Label(creategui, text="Email Address:")
    email_address_label.grid(row=4, column=0, padx=5, pady=5)
    email_address_entry = tk.Entry(creategui)
    email_address_entry.grid(row=4, column=1, padx=5, pady=5)

    # Create the submit button
    submit_button = tk.Button(creategui, text="Submit", command=create_data_process, bg="green", fg="white", font=("TkDefaultFont", 10, "bold"))
    submit_button.grid(row=6, column=1, pady=5)

    creategui.mainloop()

# READ GUI AND PROCESS
def read_data_gui():
    global mydb, listbox

    # clear the frame and set the window size
    clear_frame()
    root.geometry("330x405")

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbactivity4"
        )
        cursor = mydb.cursor()
        print("Successfully Connected to Mysql")

        mysql_select_query = """SELECT *, NOW() from tblusers"""
        cursor.execute(mysql_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")

        # create a label and listbox to display the records
        activity_label = tk.Label(root, text="RECORDS IN DATABASE", bg="#2196F3", fg="white", font=("TkDefaultFont", 10, "bold"))
        activity_label.grid(row=0, column=0, padx=0, pady=2)

        listbox = tk.Listbox(root, height=17, width=50)
        for row in records:
            listbox.insert(tk.END, f"ID: {row[0]}")
            listbox.insert(tk.END, f"First Name: {row[1]}")
            listbox.insert(tk.END, f"Last Name: {row[2]}")
            listbox.insert(tk.END, f"Email Address: {row[3]}")
            listbox.insert(tk.END, f"Record Created: {row[4]}")
            listbox.insert(tk.END, "")
        listbox.grid(row=1, column=0, padx=10, pady=10)

        update_button = tk.Button(root, text="Update", command=update_data_gui, bg="#FF9800", fg="white", width=15, font=("TkDefaultFont", 10, "bold"))
        update_button.grid(row=2, column=0, padx=10, pady=2)

        delete_button = tk.Button(root, text="Delete", command=delete_data_gui, bg="#F44336", fg="white", width=15, font=("TkDefaultFont", 10, "bold"))
        delete_button.grid(row=3, column=0, padx=10, pady=10)

        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to read data from MySQL table", error)
    finally:
        if mydb:
            mydb.close()
            print("The MySQL connection is closed")

# UPDATE GUI
def update_data_gui():
    global first_name_entry, last_name_entry, email_address_entry, id_entry

    updategui = tk.Tk()
    updategui.title("Update Data")
    updategui.geometry("300x200")

    # Create the first name entry field

    activity_label = tk.Label(updategui, text="UPDATE DATA", bg="#FF9800", fg="white", font=("TkDefaultFont", 10, "bold"))
    activity_label.grid(row=2, column=4, padx=0, pady=5)

    id_label = tk.Label(updategui, text="Id to be updated:")
    id_label.grid(row=3, column=3, padx=5, pady=5)
    id_entry = tk.Entry(updategui)
    id_entry.grid(row=3, column=4, padx=5, pady=5)

    first_name_label = tk.Label(updategui, text="First Name:")
    first_name_label.grid(row=4, column=3, padx=5, pady=5)
    first_name_entry = tk.Entry(updategui)
    first_name_entry.grid(row=4, column=4, padx=5, pady=5)

    # Create the last name entry field
    last_name_label = tk.Label(updategui, text="Last Name:")
    last_name_label.grid(row=5, column=3, padx=5, pady=5)
    last_name_entry = tk.Entry(updategui)
    last_name_entry.grid(row=5, column=4, padx=5, pady=5)

    # Create the email address entry field
    email_address_label = tk.Label(updategui, text="Email Address:")
    email_address_label.grid(row=6, column=3, padx=5, pady=5)
    email_address_entry = tk.Entry(updategui)
    email_address_entry.grid(row=6, column=4, padx=5, pady=5)

    # Create the submit button
    submit_button = tk.Button(updategui, text="Submit", command=update_data_process, bg="green", fg="white", font=("TkDefaultFont", 10, "bold"))
    submit_button.grid(row=7, column=4, pady=5)

    updategui.mainloop()

# DELETE GUI
def delete_data_gui():
    global id_entry, first_name_var, last_name_var, email_address_var
    clear_frame()
    root.geometry("300x220")

    # Create the id entry field
    activity_label = tk.Label(root, text="USER DATA DELETION", bg="#F44336", fg="white", font=("TkDefaultFont", 10, "bold"))
    activity_label.grid(row=1, column=1, padx=0, pady=5)

    id_label = tk.Label(root, text="Id to be deleted:")
    id_label.grid(row=7, column=0, padx=5, pady=5)
    id_entry = tk.Entry(root)
    id_entry.grid(row=7, column=1, padx=5, pady=5)

    # Create the checkboxes for selecting fields to delete
    first_name_var = tk.IntVar()
    first_name_checkbox = tk.Checkbutton(root, text="Delete first name", variable=first_name_var)
    first_name_checkbox.grid(row=8, column=1, padx=5, pady=5)
    last_name_var = tk.IntVar()
    last_name_checkbox = tk.Checkbutton(root, text="Delete last name", variable=last_name_var)
    last_name_checkbox.grid(row=9, column=1, padx=5, pady=5)
    email_address_var = tk.IntVar()
    email_address_checkbox = tk.Checkbutton(root, text="Delete email address", variable=email_address_var)
    email_address_checkbox.grid(row=10, column=1, padx=5, pady=5)

    # Create the submit button
    submit_button = tk.Button(root, text="Submit", command=delete_data_process, bg="green", fg="white", font=("TkDefaultFont", 10, "bold"))
    submit_button.grid(row=11, column=1, pady=5)

# clear the previous widgets when showing the inserted records
def clear_frame():
    for widgets in root.winfo_children():
        widgets.destroy()

# ROOT/MAIN GRAPHICAL USER INTERFACE
global root
root = tk.Tk()
root.title("Act4 Dagatan & Dacoroon")
root.eval('tk::PlaceWindow . center')
root.geometry("350x150")

activity_label = tk.Label(root, text="CRUD OPERATION", fg="black", font=("TkDefaultFont", 10, "bold"))
activity_label.grid(row=0, column=0, padx=0, pady=5)

create_button = tk.Button(root, text="Insert Data (Create)", command=create_data_gui, bg="#8BC34A", fg="white", width=40, font=("TkDefaultFont", 10, "bold"))
create_button.grid(row=1, column=0, padx=10, pady=10)

read_button = tk.Button(root, text="Manipulate Data (Read, Update, Delete)", command=read_data_gui, bg="#2196F3", fg="white", width=40, font=("TkDefaultFont", 10, "bold"))
read_button.grid(row=2, column=0, padx=10, pady=10)

root.mainloop()
