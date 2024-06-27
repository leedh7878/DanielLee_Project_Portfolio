import customtkinter as ctk
from CTkTable import *
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os 
from PIL import Image
import traceback
import sqlite3

from tkinter import ttk

'''global variable'''
loc_data = "../data"
load_dotenv()
password = os.getenv("password")
db_name = "bike_store_db"
''''''''''''''''''''''''''''''

class connect_database():

    def __init__ (self, name):
        self.db_name = name

        
        self.conn = psycopg2.connect(f"dbname= '{self.db_name}' user='postgres' host = 'localhost' password= '{password}'")

        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        self.cur = self.conn.cursor()

    def input_query(self, statement) -> tuple:
        try:
            self.cur.execute(statement)

            tables =  self.cur.fetchall() # A list() of tables.

            self.conn.commit()
            
            column_names = tuple(col[0] for col in self.cur.description)
                        # Print the list of column names

            return [column_names] + tables

        except psycopg2.Error as e:
            raise e

    def close(self) -> None:
        try:
            self.conn.close()
            self.cur.close()

        except psycopg2.Erorr as e:
            raise e

db_connection = connect_database(db_name)

class LoginPage(ctk.CTk):

    def __init__(self): #master -> parent
        super().__init__()
        self.geometry('300x500')
        self.resizable(False, False)
        self.wm_title('Bike Store Service Log In Page')
        self.toplevel_window = None
        self.message_window = None
        self.filter_user = ""

        self.segemented_button = ctk.CTkSegmentedButton(self,values=["Customers", "Staffs"], width = 200, dynamic_resizing= True, command = self.segmented_button_callback)
        self.segemented_button.set("Customers")
        self.segemented_button.place(relx = 0.5, rely = 0.4, anchor = 'center')
        self.user = "Customers"

        self.last_name = ctk.CTkEntry(self, placeholder_text="Last Name")
        self.last_name.place(relx = 0.5, rely = 0.5, anchor = 'center')

        self.user_id = ctk.CTkEntry(self, placeholder_text="User Id")
        self.user_id.place(relx = 0.5, rely = 0.6, anchor = 'center')

        self.button = ctk.CTkButton(self, text="Log In", command=self.login)
        self.button.place(relx = 0.5, rely = 0.8, anchor = 'center')
        
        self.login_info = (self.last_name.get(), self.user_id.get())

        ''' Image Insertion'''
        dir = os.path.dirname(__file__)
        os.chdir(dir)
        
        my_image = ctk.CTkImage(dark_image=Image.open("../image/dataset-cover.jpg"),size=(150, 80))

        self.myimage = ctk.CTkLabel(self, image=my_image, text="")  
        self.myimage.place(relx = 0.5, rely = 0.2, anchor = 'center')

        self.table = []

    def sql2str(self,file_path) -> list:
    # Read SQL file contents
        try:
            with open(file_path, 'r') as sql_file: # 'r' for read mode
                sql_script = sql_file.read()

            # Split SQL script into individual queries
            queries = sql_script.split(';')

            return queries[:-1]
            
        except Exception as e:
            print("error:", e)
            print(traceback.format_exc())

    def open_toplevel(self) -> None:
        try:
            self.withdraw()
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():

                if self.user == "Customers":
                    self.toplevel_window = CustomerWindow(self.filter_user)  
                else:
                    self.toplevel_window = StaffWindow(self.filter_user)  


                self.toplevel_window.display_table()
                self.wait_window(self.toplevel_window)
                self.deiconify()
            else:
                self.toplevel_window.focus()  # if window exists focus it
            

        except Exception as e:
            print('error: ', e)
            print(traceback.format_exc())

    def open_message(self) -> None:
        try:
            if self.message_window is None or not self.message_window.winfo_exists():
                self.message_window = Message()  # create window if its None or destroyed
                self.message_window.grab_set()
                self.wait_window(self.message_window)
            else:
                self.message_window.focus()  # if window exists focus it
        except Exception as e:
            print('error: ', e)
            print(traceback.format_exc())

    def login(self) -> None:
        try:
            self.login_info = (self.last_name.get().capitalize(), self.user_id.get())

            temp_lastname , temp_id = self.login_info
            

            unique_id = ""
            if self.user == "Customers":
                unique_id = "customer_id"
            else: 
                unique_id = "staff_id"

            self.filter_user = f"SELECT {unique_id}, first_name FROM {self.user} WHERE last_name = '{temp_lastname}' AND {unique_id} = '{temp_id}';" 
            
            output_table = []
            
            try:
                db_connection = connect_database(db_name)
                output_table = db_connection.input_query(self.filter_user)
            
            except Exception as e:

                print('error: ', e)
                # print(traceback.format_exc())
                self.open_message()
                self.wait_window(self.message_window)

            else:
                if len(output_table) >1:
                    print("we have users")

                    w,e,r = self.sql2str("./aggregate.sql")
                    
                    self.open_toplevel()

                else:
                    self.open_message()

        except Exception as e:
  
            print('error: ', e)
            print(traceback.format_exc())

    def segmented_button_callback(self,value):
        print("segmented button clicked:", value)
        self.user = value

class Message(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()
        self.geometry('300x100')
        self.wm_title('Message')
        self.attributes('-topmost', 'true')
        self.label = ctk.CTkLabel(self, text="Input is not valid, Please retry")
        self.label.pack(padx=10, pady=20)
                
class ToplevelWindow(ctk.CTkToplevel):

    def __init__(self, f_u):
        super().__init__()
        self.geometry('600x600')
        self.wm_title('Info Page')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.filtered_user =  db_connection.input_query(f_u)
        
        self.label = ctk.CTkLabel(self, font=("Arial", 24, "bold"), text = f"Welcome {self.filtered_user[1][1]} !!")
        self.label.place(x = 10, y =10)


    def display_table(self) -> None:

        table =ttk.Treeview(self, columns = self.filtered_user[0], show ='headings')
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="white")

        for x in self.filtered_user[0]:
            table.heading(x, text = x.replace("_", " "))
        
        count = 0
        for y in self.filtered_user[1:]:
            table.insert(parent = '', index = count, values = y)
            count +=1
        table.place(relx=0.01, rely=0.1, width=500, height=500)


    def on_closing(self) -> None:
        try:
            self.destroy()

        except Exception as e:
            print('error: ', e)
            print(traceback.format_exc())

class CustomerWindow(ToplevelWindow):

    def __init__(self, f_u):
        super().__init__(f_u)
    
        self.label1 = ctk.CTkLabel(self, text = "This is customer window")
        self.label1.place(relx = 0.4, rely = 0.3)


class StaffWindow(ToplevelWindow):

    def __init__(self, f_u):
        super().__init__(f_u)
    
        self.label1 = ctk.CTkLabel(self, text = "This is Staff window")
        self.label1.place(relx = 0.4, rely = 0.3)

class button_window(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()
        


if __name__== '__main__':

    app = LoginPage()
    app.mainloop()

    # 1 14127