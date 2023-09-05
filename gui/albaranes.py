import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from utils.functions_albarans import generate_albaran_queries, generate_pedidos_queries, generate_facturas_queries, generate_random_prompts

def load_predefined_values():
    file_path = os.path.join("utils", "dicc_pre.json")
    with open(file_path, 'r') as f:
        return json.load(f)

predefined_values = load_predefined_values()
clientes_predefined = predefined_values['albaranes']


class AlbaranesTab:
    def __init__(self, master):
        self.frame = ttk.Frame(master)
        
        self.label_table = tk.Label(self.frame, text="Nom de la taula:")
        self.label_table.grid(row=0, column=0)
        self.entry_table = tk.Entry(self.frame)
        self.entry_table.grid(row=0, column=1)
        self.entry_table.insert(0, "alb")

        self.label_global_train_count = tk.Label(self.frame, text="Cantidad Train Global:")
        self.label_global_train_count.grid(row=0, column=2)
        self.entry_global_train_count = tk.Entry(self.frame)
        self.entry_global_train_count.grid(row=0, column=3)
        self.entry_global_train_count.insert(0, "10")
        self.entry_global_train_count.bind('<KeyRelease>', self.update_all_train_counts)
        tk.Label(self.frame, text="Cantidad Train").grid(row=1, column=2)

        self.button_toggle_all = tk.Button(self.frame, text="Toggle All", command=self.toggle_all)
        self.button_toggle_all.grid(row=1, column=3)        

        self.query_types = ["todo_alb", "DetalleCliente"]
        self.query_entries = {}
        self.query_train_counts = {}
        self.query_checkbutton_vars = {}
        self.query_checkbuttons = {}         

        for idx, q_type in enumerate(self.query_types):
            tk.Label(self.frame, text=f"{q_type} : ").grid(row=idx + 2, column=0)
            self.query_entries[q_type] = tk.Entry(self.frame)
            self.query_entries[q_type].grid(row=idx + 2, column=1)

            if q_type in clientes_predefined:
                self.query_entries[q_type].insert(0, clientes_predefined[q_type])

            self.query_train_counts[q_type] = tk.Entry(self.frame)
            self.query_train_counts[q_type].grid(row=idx + 2, column=2)
            self.query_train_counts[q_type].insert(0, "10")

            self.query_checkbutton_vars[q_type] = tk.BooleanVar()
            self.query_checkbuttons[q_type] = tk.Checkbutton(self.frame, variable=self.query_checkbutton_vars[q_type])
            self.query_checkbuttons[q_type].grid(row=idx + 2, column=3)
                
        self.button_generate = tk.Button(self.frame, text="Genera el Arxiu", command=self.generate_jsonl)
        self.button_generate.grid(row=len(self.query_types) + 2, column=0, columnspan=4)

    def toggle_all(self):
        new_state = not any(var.get() for var in self.query_checkbutton_vars.values())
        for var in self.query_checkbutton_vars.values():
            var.set(new_state)

    def update_all_train_counts(self, event):
        global_value = self.entry_global_train_count.get()
        for entry in self.query_train_counts.values():
            entry.delete(0, tk.END)
            entry.insert(0, global_value)


    def generate_jsonl(self):
        train_count = int(self.entry_train_count.get())
        valid_count = int(train_count * 0.20)
        
        self.train_prompts_list, self.valid_prompts_list = generate_random_prompts(train_count, valid_count)
        
        train_filepath = "Documents/dicc/results/train.jsonl"
        valid_filepath = "Documents/dicc/results/valid.jsonl"

        documento_tipo = self.generate_file(train_filepath, self.train_prompts_list)
        self.generate_file(valid_filepath, self.valid_prompts_list)

        messagebox.showinfo("Correcte", f"Arxius JsonL de {documento_tipo} creats amb exit!")

    def generate_file(self, filepath, prompts_list):
        table_name = self.entry_table.get().strip()
        function_name = self.entry_function_name.get().strip()

        generated_lines = []

        if self.query_type.get() == "Albaran":
            documento_tipo = "Albaran"            
            generate_albaran_queries(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "Pedido":
            documento_tipo = "Pedido"            
            generate_pedidos_queries(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "Factura":
            documento_tipo = "Factura"            
            generate_facturas_queries(generated_lines, table_name, function_name, prompts_list)


        with open(filepath, 'a', encoding='utf-8') as file:
            for line in generated_lines:
                file.write(line + '\n')
        return documento_tipo
