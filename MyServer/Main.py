import tkinter as tk
from src.Interface import InterfaceGraphique

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGraphique(root)
    root.mainloop()