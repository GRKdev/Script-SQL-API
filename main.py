import tkinter as tk
from tkinter import ttk
from gui.clients import ClientTab
from gui.albaranes import AlbaranesTab
from gui.training import TrainingTab
from gui.articulos import ArticulosTab
from gui.facturacio_stats import StatsTab

class JsonLGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Script Jsonl Training - OpenAI")

        style = ttk.Style()
        style.configure("TNotebook", background='#ccc')  # Cambiar el fondo del Notebook
        style.map("TNotebook.Tab", background=[("selected", "#ff0000")])  # Cambiar el fondo de la pestaña seleccionada a rojo

        self.notebook = ttk.Notebook(master)

        self.notebook = ttk.Notebook(master, style='TNotebook')
        
        self.tab_clients = ClientTab(self.notebook)
        self.notebook.add(self.tab_clients.frame, text="Clients")
        
        self.tab_articulos = ArticulosTab(self.notebook)
        self.notebook.add(self.tab_articulos.frame, text="Articulos")

        self.tab_albaranes = AlbaranesTab(self.notebook)
        self.notebook.add(self.tab_albaranes.frame, text="Albarans")
        
        self.tab_stats = StatsTab(self.notebook)
        self.notebook.add(self.tab_stats.frame, text="Facturacio Stats")

        self.tab_training = TrainingTab(self.notebook)
        self.notebook.add(self.tab_training.frame, text="Entrenar")

        self.notebook.pack(expand=1, fill="both")

root = tk.Tk()
app = JsonLGenerator(root)
root.mainloop()
