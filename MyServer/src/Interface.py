import tkinter as tk
from datetime import datetime
import threading
import subprocess
import platform
from src.Apache import Server
from tkinter import messagebox

class InterfaceGraphique:
    def __init__(self, root):
        self.server = Server()
        self.server_thread = None
        self.root = root
        self.root.title("MyServer")
        self.root.geometry("800x300")

        # Ajouter des widgets
        self.label_titre = tk.Label(
            root,
            text="Welcome to MyServer",
            font=("Arial", 16))
        self.label_titre.pack(pady=5)

        self.bouton_start = tk.Button(
            root,
            text="Start",
            command=self.start_serveur)
        self.bouton_start.pack(pady=5)

        self.bouton_stop = tk.Button(
            root,
            text="Stop",
            command=self.stop_serveur)
        self.bouton_stop.pack(pady=5)

        self.bouton_config = tk.Button(
            root,
            text="Config",
            command=self.change_conf)
        self.bouton_config.pack(pady=5)

        self.label_info = tk.Label(
            root,
            text=f"Date: {datetime.now()}",
            width=200,
            height=100,
            bd=1,  # Épaisseur de la bordure
            relief="ridge"  # Style de la bordure
        )
        self.label_info.pack(pady=20)

    def start_serveur(self):
        if not self.server.running:
            self.server =Server()
            self.server_thread = threading.Thread(target=self.server.start, daemon=True)
            self.server_thread.start()
            self.bouton_start.config(state="disabled")
            self.bouton_stop.config(state="normal")
        else:
            messagebox.showinfo("Serveur", "Le serveur est déjà en cours d'exécution.")

    def stop_serveur(self):
        if self.server.running:
            self.server.stop()
            self.server_thread.join()
            self.bouton_start.config(state="normal")
            self.bouton_stop.config(state="disabled")
        else:
            messagebox.showinfo("Serveur", "Le serveur est déjà arrêté.")
    
    def change_conf(self):
        file_path = "config.xml"
        try:
            system = platform.system()
            if system == "Windows":
                # Ouvre le fichier avec Notepad (Bloc-notes) sur Windows
                subprocess.run(["notepad", file_path], check=True)
            elif system == "Linux":
                # Ouvre le fichier avec gedit sur Ubuntu (ou autre éditeur de texte)
                subprocess.run(["gedit", file_path], check=True)
            else:
                print(f"Le système d'exploitation '{system}' n'est pas pris en charge.")
        except FileNotFoundError:
            print(f"Le fichier '{file_path}' est introuvable.")
        except subprocess.CalledProcessError:
            print(f"Impossible d'ouvrir le fichier '{file_path}'.")
        except Exception as e:
            print(f"Une erreur inattendue s'est produite : {e}")

