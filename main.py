import tkinter as tk
from tkinter import ttk
from gui.clients import ClientTab
from gui.albaranes import AlbaranesTab
from gui.training import TrainingTab
from gui.articulos import ArticulosTab
from gui.facturacio_stats import EstadisticasTab

class JsonLGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Script Jsonl Training - OpenAI")

        self.notebook = ttk.Notebook(master)

        self.notebook = ttk.Notebook(master, style='TNotebook')
        
        self.tab_clients = ClientTab(self.notebook)
        self.notebook.add(self.tab_clients.frame, text="Clients")
        
        self.tab_articulos = ArticulosTab(self.notebook)
        self.notebook.add(self.tab_articulos.frame, text="Articulos")

        self.tab_albaranes = AlbaranesTab(self.notebook)
        self.notebook.add(self.tab_albaranes.frame, text="Albarans")
        
        self.tab_stats = EstadisticasTab(self.notebook)
        self.notebook.add(self.tab_stats.frame, text="Facturacio Stats")

        self.tab_training = TrainingTab(self.notebook)
        self.notebook.add(self.tab_training.frame, text="Entrenar")

        self.notebook.pack(expand=1, fill="both")

root = tk.Tk()
app = JsonLGenerator(root)
root.mainloop()
