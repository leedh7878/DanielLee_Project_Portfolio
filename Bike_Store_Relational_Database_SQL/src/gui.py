import customtkinter as ctk
from CTkTable import *
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os 
#global variable

loc_data = "../data"
load_dotenv()
password = os.getenv("password")
db_name = "bike_store_db"


def button_event():
    print("button pressed")


def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

def login(info):

    print('working')

def creating_app():

    
    app = ctk.CTk()
    app.title("Bike_Store Summary")    
    app.geometry("1000x600")
    ctk.set_default_color_theme("green") 

    # button = ctk.CTkButton(app, text="CTkButton", command=button_event)
    # button.pack(pady=10,padx=12)

    # combobox_var = ctk.StringVar(value="option 2")
    # combobox = ctk.CTkComboBox(app, values=["option 1", "option 2"],command=combobox_callback, variable=combobox_var)
    # combobox_var.set("option 2")
    # combobox.pack(pady =12, padx = 10)

    tabview = ctk.CTkTabview(master=app)
    tabview.pack(padx=10, pady=10)

    tabview.add("Log_In")  # add tab at the end
    tabview.add("Employee")  # add tab at the end

    tabview.set("Log_In")  # set currently visible tab

    entry_id = ctk.CTkEntry(master = tabview.tab("Log_In"),placeholder_text = "user id")
    entry_id.pack(padx=10, pady=10)

    entry_zip = ctk.CTkEntry(master = tabview.tab("Log_In"),placeholder_text = "zip code")
    entry_zip.pack(padx=10, pady=10)

    button = ctk.CTkButton(master = tabview.tab("Log_In"), text="Continue", command= login("ss"))

    button.pack(pady=10,padx=10)


    value = [[1,2,3,4,5],
            [1,2,3,4,5],
            [1,2,3,4,5],
            [1,2,3,4,5],
            [1,2,3,4,5]]

    def testa(choice):
        print("hi",choice)

    a = update_table()
    table = CTkTable(master=app, row=5, column=5, values=a,command=testa)
    table.pack(expand=False, fill=None, padx=20, pady=20)


    app.mainloop()

def update_table() -> list:

    try:
        conn = psycopg2.connect(f"dbname= '{db_name}' user='postgres' host = 'localhost' password= '{password}'")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()

        try:
            cur.execute(f"SELECT * from Stores")

            tables =  cur.fetchall() # A list() of tables.

            conn.commit()
            # Close the cursor and connection
            cur.close()
            conn.close()   
            
            column_names = tuple(col[0] for col in cur.description)
                        # Print the list of column names
            return [column_names] + tables
    
        except psycopg2.Error as e:
            raise e
            
    except psycopg2.Error as e:
        raise e

if __name__== '__main__':
    database_name = "bike_store_db"

    creating_app()