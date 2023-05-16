import tkinter as tk
from tkinter import messagebox
from serial import Serial
from time import sleep
import _thread
import sys
import sqlite3


try:
    connexion = sqlite3.connect("database.sqlite")
    curs = connexion.cursor
    
    table = """CREATE TABLE USER(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nfcId INTEGER,
            username TEXT NOT NULL,
            creationDate TEXT NOT NULL,
            description TEXT NOT NULL );"""     

    query = """INSERT INTO USER (nfcId,username,creationDate,description) VALUES (1234,"HUGO","test","test");"""
    connexion.execute(query)
    connexion.commit()
    connexion.close
    print("Skill issue")
    
    print("creation table")
except sqlite3.Error as error:
    print(error)
finally:
    if connexion:
        connexion.close
        

s = Serial("COM7",9600, timeout=0.05)
terminateThread = False

try:
    connextion = sqlite3.connect("database.db")
    curs = connextion.cursor
except sqlite3.Error as error:
            print(error)

class User:
    def __init__(self,nfcid, username, creationdate, description) -> None:
        self.nfcid = nfcid
        self.username = username
        self.nfcId = nfcId
        self.creationdate = creationdate
        self.description = description

    def __repr__(self):
        return f"{self.username} - {self.nfcId} - {self.creationdate}"
    
    def listUserDiplay(self):
        return f"{self.username}"


class UserInterface(tk.Tk):
    def __init__(self, root):
        
        self.root = root
        self.root.title("User System")
        self.root.geometry("500x500")

        self.bouton_activer = tk.Button(self.root, text="Turn on system")
        self.bouton_activer["command"] = self.btn_turn_on_click
        self.bouton_activer.pack(pady=10)

        self.bouton_desactiver = tk.Button(self.root, text="Turn off system", state="disabled")
        self.bouton_desactiver["command"] = self.btn_turn_off_click
        self.bouton_desactiver.pack(pady=10)

        self.label_users = tk.Label(self.root, text="Users:")
        self.label_users.pack(pady=5)
        self.liste_users = tk.Listbox(self.root, height=10,width=60 )
        self.liste_users.pack(pady=5)

        self.bouton_register = tk.Button(self.root, text="Register")
        self.bouton_register["command"] = self.btn_register_click
        self.bouton_register.pack(pady=10)

        self.load_users_from_file()

    def create_user(self):
        try:
            connextion = sqlite3.connect("database.db")
            curs = connextion.cursor
        except sqlite3.Error as error:
            print(error)
    
    
    def contains_open(self,s):
        return 'OPEN' in s.upper()
    def remove_open(self,s):
        return s.replace('OPEN', '').replace('open', '')
    
    def open_lock(self):
        global terminateThread
        while True:
            if terminateThread:
                print("test")
                break
            #lecture de commande de l'hôte
            data_in = s.readline()
            msg = str(data_in)[2:-5]
            if(msg != "" and 'OPEN' in msg):
                print(msg)
                code = msg.replace('OPEN','')
                print(code)
                s.write(b"VALIDE\n")
                sleep(1)
                s.write(b"START\n")
        
    def btn_turn_on_click(self):
        global terminateThread
        self.bouton_desactiver.configure(state="normal")
        self.bouton_activer.configure(state="disabled")
        terminateThread = False
        s.write(b"START\n")
        _thread.start_new_thread(self.open_lock, ())
            
    def btn_turn_off_click(self):
        self.bouton_desactiver.configure(state="disabled")
        self.bouton_activer.configure(state="normal")
        global terminateThread 
        terminateThread = True
        
        

    def load_users_from_file(self):
        print("test")

    def btn_register_click(self):
        s.write(b"REGISTER\n")
        while True:
            data_in = s.readline()
            msg = str(data_in)[2:-5]
            if(msg != "" and 'REGISTER' in msg):
                code = msg.replace('REGISTER','')
                print(code)
                break
    
if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()