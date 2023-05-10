import tkinter as tk
from tkinter import messagebox

class User:
    def __init__(self,username, creationdate) -> None:
        self.username = username
        self.creationdate = creationdate

    def __repr__(self):
        return f"{self.username} - {self.creationdate}"
    
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

    def btn_turn_on_click(self):
        self.bouton_desactiver.configure(state="normal")
        self.bouton_activer.configure(state="disabled")

    def btn_turn_off_click(self):
        self.bouton_desactiver.configure(state="disabled")
        self.bouton_activer.configure(state="normal")

    def load_users_from_file(self):
        print("test")

    def btn_register_click(self):
        username = "test"
    
if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()