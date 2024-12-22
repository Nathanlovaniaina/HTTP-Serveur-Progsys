import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

class Installeur:
    def __init__(self, root):
        self.root = root
        self.root.title("MyServer-Installer")
        self.root.geometry("600x200")

        label = tk.Label(root, text="Sélectionnez le dossier de destination pour installer le projet", font=("Arial", 14))
        label.pack(pady=10)

        self.destination_button = tk.Button(root, text="Sélectionner le dossier de destination", command=self.select_destination)
        self.destination_button.pack(pady=10)

        self.destination_label = tk.Label(root, text="Aucun dossier sélectionné", font=("Arial", 10))
        self.destination_label.pack()

        self.install_button = tk.Button(root, text="Installer", command=self.install_project, state=tk.DISABLED)
        self.install_button.pack(pady=20)

        self.source_path = "./MyServer" 
        self.destination_path = None

    def select_destination(self):
        self.destination_path = filedialog.askdirectory(title="Sélectionner le dossier de destination")
        if self.destination_path:
            self.destination_label.config(text=f"Destination: {self.destination_path}")
            self.check_ready_to_install()

    def check_ready_to_install(self):
        if self.destination_path:
            self.install_button.config(state=tk.NORMAL)
        else:
            self.install_button.config(state=tk.DISABLED)

    def install_project(self):
        try:
            # Vérifier si le dossier source existe
            if not os.path.exists(self.source_path):
                messagebox.showerror("Erreur", f"Le dossier source '{self.source_path}' n'existe pas.")
                return

            # Vérifier si le dossier de destination existe
            if not os.path.exists(self.destination_path):
                messagebox.showerror("Erreur", f"Le dossier de destination '{self.destination_path}' n'existe pas.")
                return

            # Copie le dossier source dans le dossier de destination
            destination_folder = os.path.join(self.destination_path, os.path.basename(self.source_path))
            if os.path.exists(destination_folder):
                messagebox.showinfo("Info", f"Le projet est déjà installé dans {destination_folder}.")
                return

            shutil.copytree(self.source_path, destination_folder)
            messagebox.showinfo("Installation terminée", f"Le projet a été installé avec succès dans {destination_folder}.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'installation: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    installeur = Installeur(root)
    root.mainloop()
