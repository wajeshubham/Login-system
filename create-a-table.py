"""create a table in your database to store
the data that user enters"""




from tkinter import *
from sqlite3 import *

#create a window
root = Tk()
root.title("Login system")
root.geometry("1920x1080+0+0")

#connect or create a database file
conn = connect("userdata.db")

c = conn.cursor()


#create a table using following command

c.execute("""CREATE TABLE shubham (
             'f_name' text,
             'l_name' text,
             'username' text,
             'password' text)""")


conn.commit()

conn.close()

root.mainloop()
