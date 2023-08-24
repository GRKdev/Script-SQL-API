import tkinter as tk
from tkinter import ttk
from gui.clients import ClientTab
from gui.albaranes import AlbaranesTab
from gui.training import TrainingTab
from gui.articulos import ArticulosTab

class JsonLGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Script Jsonl Training - OpenAI")

        self.notebook = ttk.Notebook(master)
        
        self.tab_clients = ClientTab(self.notebook)
        self.notebook.add(self.tab_clients.frame, text="Clients")
        
        self.tab_albaranes = ArticulosTab(self.notebook)
        self.notebook.add(self.tab_albaranes.frame, text="Articulos")

        self.tab_albaranes = AlbaranesTab(self.notebook)
        self.notebook.add(self.tab_albaranes.frame, text="Albarans")
        
        self.notebook.pack(expand=1, fill="both")

        self.tab_training = TrainingTab(self.notebook)
        self.notebook.add(self.tab_training.frame, text="Entrenar")

root = tk.Tk()
app = JsonLGenerator(root)
root.mainloop()
