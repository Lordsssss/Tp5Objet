import tkinter as tk
from tkinter import messagebox
from serial import Serial
from time import sleep
import _thread
import gestionnaireDB as db
from datetime import datetime

s = Serial("COM7",9600, timeout=0.05)
terminateThread = False


class User:
    def __init__(self,nfcid, username, creationdate, description) -> None:
        self.nfcid = nfcid
        self.username = username
        self.creationdate = creationdate
        self.description = description

    
    def __repr__(self):
        return f"{self.username} - {self.nfcid} - {self.creationdate}"
    
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

        self.label_username = tk.Label(self.root, text="Le nom d'utilisateur")
        self.label_username.pack(pady=5)
        self.entree_username = tk.Entry(self.root, width=10)
        self.entree_username.pack(pady=5)
        
        self.bouton_register = tk.Button(self.root, text="Register")
        self.bouton_register["command"] = self.btn_register_click
        self.bouton_register.pack(pady=10)
    
    def update_user_list(self):
        user_data = db.selectionListeUser()
        print(user_data)
        for user in user_data:
            self.liste_users.insert(tk.END, str(user[0]))
    
    def contains_open(self,s):
        return 'OPEN' in s.upper()
    def remove_open(self,s):
        return s.replace('OPEN', '').replace('open', '')
    
    def open_lock(self):
        global terminateThread
        while True:
            if terminateThread:
                break
            #lecture de commande de l'hôte
            data_in = s.readline()
            msg = str(data_in)[2:-5]
            if(msg != "" and 'OPEN' in msg):
                print(msg)
                code = msg.replace('OPEN','')
                print(code)
                if db.verifierNfcId(code):
                    s.write(b"VALIDE\n")
                else:
                    s.write(b"INVALIDE\n")
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
        s.write(b"STOP\n")
    
    def register_card(self):
        while True:
                data_in = s.readline()
                msg = str(data_in)[2:-5]
                print("message",msg)
                if(msg != "" and 'REGISTER' in msg):
                    code = msg.replace('REGISTER','')
                    print(code)
                    user = User(code,self.entree_username.get(),datetime.now(),"Compte utilisateur")
                    db.ajouterUser(user.nfcid,user.username,user.creationdate,user.description)
                    messagebox.showinfo("Bravo !","Le compte a été créer !")
                    break
    
    def btn_register_click(self):
        s.write(b"REGISTER\n")
        if self.entree_username.get() == "":
            messagebox.showerror("Error","Vous n'avez pas entrer la description")
        else:
            self.bouton_desactiver.configure(state="disabled")
            self.bouton_activer.configure(state="normal")
            global terminateThread 
            terminateThread = True
            self.register_card()
            messagebox.showwarning("Restart","L'application va se fermer")
            root.destroy()
            
if __name__ == "__main__":
    db.creationTable()
    root = tk.Tk()
    app = UserInterface(root)
    app.update_user_list()
    root.mainloop()