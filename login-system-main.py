from tkinter import *
from tkinter import messagebox
import tkinter.font as tf
from sqlite3 import *

# create a window
root = Tk()
root.title("Login system")
root.geometry("1920x1080+0+0")

# connect or create a database file
conn = connect("userdata.db")

c = conn.cursor()

# refer "create-a-table.py file
'''
c.execute("""CREATE TABLE shubham (
             'f_name' text,
             'l_name' text,
             'username' text,
             'password' text)""")
'''


# create a function to delete data frm database
def delete():
    conn = connect("userdata.db")

    c = conn.cursor()

    # delete data using following command
    c.execute("DELETE FROM shubham WHERE oid=" + str(del_ID.get()))
    del_ID.delete(0, END)

    conn.commit()

    conn.close()


# create function to nodify the data
def update():
    conn = connect("userdata.db")

    c = conn.cursor()

    c.execute("""UPDATE shubham SET
                f_name=:first,
                l_name=:last,
                username=:username,
                password=:password
                WHERE oid=:oid   """,
              {'first': first_name_editor.get(),
               'last': last_name_editor.get(),
               'username': username_editor.get(),
               'password': password_editor.get(),
               'oid': str(i + 1)}
              )
    # confirmation message
    lbl = Label(frm_main_editor, text="Saved!")
    lbl.grid(row=6, column=0, columnspan=2, pady=10)

    conn.commit()

    conn.close()


# function to insert data in editor entries to edit the data
def edit():
    global frm_main_editor
    root_4 = Tk()
    root_4.title("Edit profile")
    root_4.geometry("1920x1080+0+0")

    conn = connect("userdata.db")

    c = conn.cursor()
    # select data from database
    c.execute("SELECT * FROM shubham WHERE oid=" + str(i + 1))
    record = c.fetchall()

    global first_name_editor
    global last_name_editor
    global password_editor
    global username_editor

    # create buttons and entries for editor window
    frm_main_editor = LabelFrame(root_4, bg="white", pady=20, padx=20)
    frm_main_editor.grid(padx=550, pady=100)

    first_name_editor = Entry(frm_main_editor, borderwidth=5, width=50)
    first_name_editor.grid(row=0, column=1)
    last_name_editor = Entry(frm_main_editor, borderwidth=5, width=50)
    last_name_editor.grid(row=1, column=1)
    username_editor = Entry(frm_main_editor, borderwidth=5, width=50)
    username_editor.grid(row=2, column=1)
    password_editor = Entry(frm_main_editor, borderwidth=5, width=50)
    password_editor.grid(row=3, column=1)

    first_name_lbl = Label(frm_main_editor, text="First name", bg="white")
    first_name_lbl.grid(row=0, column=0, pady=10)
    last_name_lbl = Label(frm_main_editor, text="Last name", bg="white")
    last_name_lbl.grid(row=1, column=0, pady=10)
    username_lbl = Label(frm_main_editor, text="Username", bg="white")
    username_lbl.grid(row=2, column=0, pady=10)
    password_lbl = Label(frm_main_editor, text="Password", bg="white")
    password_lbl.grid(row=3, column=0, pady=10)
    # create a button to save the changes
    save_btn = Button(frm_main_editor, text="Save changes", command=update)
    save_btn.grid(row=4, column=0, columnspan=2, pady=10)
    # buton to exit editor window
    exit_btn = Button(frm_main_editor, text="Exit", command=root_4.destroy)
    exit_btn.grid(row=5, column=0, columnspan=2, ipadx=25)
    # insert data from database in entries
    for rec in record:
        first_name_editor.insert(0, rec[0])
        last_name_editor.insert(0, rec[1])
        username_editor.insert(0, rec[2])
        password_editor.insert(0, rec[3])

    conn.commit()

    conn.close()


# create home oage of user
def home_page():
    root_3 = Tk()
    root_3.title("Home window")
    root_3.geometry("1920x1080+0+0")

    conn = connect("userdata.db")

    c = conn.cursor()
    # select data frm database with given oid
    c.execute("SELECT * FROM shubham WHERE oid=" + str(i + 1))
    user_record_list = c.fetchall()
    user_record = user_record_list[0]
    # create header text for homepage
    fontsize_1 = tf.Font(family='Symbol 8', size=20)
    fontsize_2 = tf.Font(family='Symbol 8', size=15)
    lbl = Label(root_3, text=f"Welcome {user_record[0]} 😃", font=fontsize_1)
    lbl.grid(row=0, column=0, sticky=NW, padx=20, pady=20)

    lbl = Label(root_3, text="Type here", font=fontsize_2)
    lbl.grid(row=1, column=0, sticky=W)

    text = Text(root_3)
    text.grid(row=2, column=0, ipadx=80)
    # create logout button
    logout_btn = Button(root_3, text="Logout", command=root_3.destroy)
    logout_btn.grid(row=0, column=1, sticky=NE, padx=300, pady=20)

    # create 'edit profile' button
    edit_btn = Button(root_3, text="Edit profile", command=edit)
    edit_btn.grid(row=0, column=1, sticky=NE, padx=220, pady=20)

    conn.commit()

    conn.close()


# create function to verify the user
def login():
    global record
    conn = connect("userdata.db")

    c = conn.cursor()
    c.execute("SELECT *,oid FROM shubham")
    record = c.fetchall()
    # get username and password that user entered
    entered_password = password_2.get()
    entered_username = username_2.get()
    global i
    i = 0
    while i in range(len(record)):
        # logic to verify the user
        if entered_password in record[i] and entered_username in record[i]:
            confirm = messagebox.showinfo("Login", "Logged in successfully")
            root_2.destroy()
            break
        i += 1

    else:
        error = messagebox.showerror("Error", "Invalid username or password")
    # show pop up and enter the homepage when user click ok
    if confirm == "ok":
        home_page()

    conn.commit()

    conn.close()


# create login page
def login_page():
    global root_2
    root_2 = Tk()
    root_2.title("Login window")
    root_2.geometry("1920x1080+0+0")

    conn = connect("userdata.db")

    c = conn.cursor()

    global frm_main_2
    global password_2
    global username_2
    # create login page  and login button
    frm_main_2 = LabelFrame(root_2, bg="white", pady=20, padx=20)
    frm_main_2.grid(padx=550, pady=100)

    username_2 = Entry(frm_main_2, borderwidth=5, width=50)
    username_2.grid(row=0, column=1, padx=5)
    password_2 = Entry(frm_main_2, borderwidth=5, width=50)
    password_2.grid(row=1, column=1)

    username_lbl = Label(frm_main_2, text="Username", bg="white")
    username_lbl.grid(row=0, column=0, pady=10)
    password_lbl = Label(frm_main_2, text="Password", bg="white")
    password_lbl.grid(row=1, column=0, pady=10)

    login_btn = Button(frm_main_2, text="Login", command=login)
    login_btn.grid(row=2, column=0, columnspan=2)

    conn.commit()

    conn.close()


def show():
    info_wd = Tk()
    info_wd.title("User Information")

    conn = connect("userdata.db")
    c = conn.cursor()
    c.execute("SELECT *,oid FROM shubham")
    # get data from database
    records = c.fetchall()
    info = " "

    # logic to display username and name of user on screen
    for rec in records:
        print(rec)
        info += rec[0] + " " + rec[1] + "\t" + str(rec[4]) + "\n" + f"Username: {rec[2]}" + "\n" + "\n"
        print(info)
    lbl = Label(info_wd, text=info, bg='white')
    lbl.grid(row=8, column=0, columnspan=1, pady=30, padx=30)

    conn.commit()
    conn.close()


# function to make sign in button active
def activate():
    if r.get() == 1:
        submit_btn = Button(frm_main, text="Sign Up", width=50, state=ACTIVE, command=save)
        submit_btn.grid(row=5, column=0, columnspan=2, pady=10, ipadx=15)
    if r.get() == 0:
        submit_btn = Button(frm_main, text="Sign Up", width=50, state=DISABLED)
        submit_btn.grid(row=5, column=0, columnspan=2, pady=10, ipadx=15)


# function to add entered information in database
def save():
    conn = connect("userdata.db")

    c = conn.cursor()

    c.execute("INSERT INTO shubham VALUES(:f_name,:l_name,:username,:password)",
              {'f_name': first_name.get(),
               'l_name': last_name.get(),
               'username': username.get(),
               'password': password.get()
               })

    first_name.delete(0, END)
    last_name.delete(0, END)
    username.delete(0, END)
    password.delete(0, END)

    conn.commit()

    conn.close()


# create button ,labels and entries for main page
frm_main = LabelFrame(root, bg="white", pady=20, padx=20)
frm_main.grid(padx=550, pady=100)

first_name = Entry(frm_main, borderwidth=5, width=50)
first_name.grid(row=0, column=1)
last_name = Entry(frm_main, borderwidth=5, width=50)
last_name.grid(row=1, column=1)
username = Entry(frm_main, borderwidth=5, width=50)
username.grid(row=2, column=1)
password = Entry(frm_main, borderwidth=5, width=50)
password.grid(row=3, column=1)

first_name_lbl = Label(frm_main, text="First name", bg="white")
first_name_lbl.grid(row=0, column=0, pady=10)
last_name_lbl = Label(frm_main, text="Last name", bg="white")
last_name_lbl.grid(row=1, column=0, pady=10)
username_lbl = Label(frm_main, text="Username", bg="white")
username_lbl.grid(row=2, column=0, pady=10)
password_lbl = Label(frm_main, text="Password", bg="white")
password_lbl.grid(row=3, column=0, pady=10)

submit_btn = Button(frm_main, text="Sign Up", width=50, state=DISABLED)
submit_btn.grid(row=5, column=0, columnspan=2, pady=10, ipadx=15)
# variable for chechbutton
r = IntVar()
r.set(1)
accept_btn = Checkbutton(frm_main, text="I accept all thems & conditions", variable=r, onvalue=r.get(),
                         offvalue=r.set(0), bg="white", command=activate)
accept_btn.grid(row=4, column=0, columnspan=3, ipadx=20)

btn = Button(frm_main, text="showinfo", command=show)
btn.grid(row=6, column=0, columnspan=2)

login_lbl = Label(frm_main, text='Already have an account?', bg='white', fg='blue')
login_lbl.grid(row=9, column=0, columnspan=2, pady=10)

login_btn = Button(frm_main, text="Login", command=login_page)
login_btn.grid(row=10, column=0, columnspan=2)

fontsize = tf.Font(family='Symbol 8', size=15)
lbl = Label(root, text=f"Welcome to LOGIN SYSTEM 😃", font=fontsize)
lbl.grid(row=0, column=0, sticky=NW, padx=20, pady=20)

# entry to take ID as an input from admin
del_ID = Entry(root, borderwidth=5, width=40)
del_ID.grid(row=0, column=0, sticky=NE, padx=80, pady=20)

del_ID_lbl = Label(root, text="Enter ID")
del_ID_lbl.grid(row=0, column=0, sticky=NE, padx=335, pady=22)

# button to delete the data from database
del_ID_btn = Button(root, text="Delete", command=delete)
del_ID_btn.grid(row=0, column=0, sticky=NE, padx=80, pady=55, ipadx=30)

warn_lbl = Label(frm_main, text="*All fields are required", bg='white', fg='red')
warn_lbl.grid(row=11, column=0)

conn.commit()

conn.close()

root.mainloop()
