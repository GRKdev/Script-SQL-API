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

        self.notebook = ttk.Notebook(master, style='TNotebook')
        
        tabs = [
            (ClientTab, "Clients"),
            (ArticulosTab, "Articulos"),
            (AlbaranesTab, "Albarans"),
            (EstadisticasTab, "Facturacio Stats"),
            (TrainingTab, "Entrenar")
        ]
        
        for tab_class, tab_name in tabs:
            tab = tab_class(self.notebook)
            self.notebook.add(tab.frame, text=tab_name)

        self.notebook.pack(expand=1, fill="both")

root = tk.Tk()
app = JsonLGenerator(root)
root.mainloop()