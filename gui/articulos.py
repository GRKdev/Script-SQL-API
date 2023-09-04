import tkinter as tk
from tkinter import ttk
import os
import json
from utils.functions_articulos import (
    generate_custom_queries, load_prompts_from_json, generate_random_numbers,
    generate_precioart_queries, generate_random_bars, generate_codebar_queries,
    generate_toda_la_info
)


def load_predefined_values():
    file_path = os.path.join("utils", "dicc_pre.json")
    with open(file_path, 'r') as f:
        return json.load(f)
    
predefined_values = load_predefined_values()
articulos_predefined = predefined_values["articulos"]

class ArticulosTab:
    def __init__(self, master):
        self.frame = ttk.Frame(master)
        
        self.label_table = tk.Label(self.frame, text="Nom de la taula:")
        self.label_table.grid(row=0, column=0)
        self.entry_table = tk.Entry(self.frame)
        self.entry_table.grid(row=0, column=1)
        self.entry_table.insert(0, "art")

        self.label_global_train_count = tk.Label(self.frame, text="Cantidad Train Global:")
        self.label_global_train_count.grid(row=0, column=2)
        self.entry_global_train_count = tk.Entry(self.frame)
        self.entry_global_train_count.grid(row=0, column=3)
        self.entry_global_train_count.insert(0, "10")
        self.entry_global_train_count.bind('<KeyRelease>', self.update_all_train_counts)
        tk.Label(self.frame, text="Cantidad Train").grid(row=1, column=2)

        self.button_toggle_all = tk.Button(self.frame, text="Toggle All", command=self.toggle_all)
        self.button_toggle_all.grid(row=1, column=3)

        self.query_types = ["Articulos","CodigoArticulo","PrecioArticulo", "PrecioCode", "CodeBar","todo","todo_codigo"]
        self.query_entries = {}
        self.query_train_counts = {}
        self.query_checkbutton_vars = {}
        self.query_checkbuttons = {}

        for idx, q_type in enumerate(self.query_types):
            tk.Label(self.frame, text=f"{q_type} : ").grid(row=idx + 2, column=0)
            self.query_entries[q_type] = tk.Entry(self.frame)
            self.query_entries[q_type].grid(row=idx + 2, column=1)
            
            if q_type in articulos_predefined:
                self.query_entries[q_type].insert(0, articulos_predefined[q_type])

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
        function_names = {q_type: entry.get().strip() for q_type, entry in self.query_entries.items() if self.query_checkbutton_vars[q_type].get()}
        default_train_count = int(self.entry_train_count.get()) if hasattr(self, 'entry_train_count') else 100

        for query_type, function_name in function_names.items():
            train_count = int(self.query_train_counts.get(query_type, default_train_count).get())
            valid_count = int(train_count * 0.20)

            if query_type == "CodigoArticulo":
                train_data, valid_data = generate_random_numbers(train_count, valid_count)
            elif query_type == "todo_codigo":
                train_data, valid_data = generate_random_numbers(train_count, valid_count)
            elif query_type == "CodeBar":
                train_data, valid_data = generate_random_bars(train_count, valid_count)
            elif query_type == "PrecioCode":
                train_data, valid_data = generate_random_numbers(train_count, valid_count)            
            else:
                original_train_prompts = load_prompts_from_json()
                original_valid_prompts = load_prompts_from_json()
                train_data = [original_train_prompts[i % len(original_train_prompts)] for i in range(train_count)]
                valid_data = [original_valid_prompts[i % len(original_valid_prompts)] for i in range(valid_count)]

            train_filepath = "Documents/dicc/results/train.jsonl"
            valid_filepath = "Documents/dicc/results/valid.jsonl"

            self.generate_file(train_filepath, train_data, query_type, function_name)
            self.generate_file(valid_filepath, valid_data, query_type, function_name)

    def generate_file(self, filepath, prompts_list, query_type, function_name): 
        table_name = self.entry_table.get().strip()
        generated_lines = []

        if query_type == "PrecioCode":
            documento_tipo = "PrecioCode"            
            generate_precioart_queries(generated_lines, table_name, function_name, prompts_list)
        elif query_type == "Articulos":
            documento_tipo = "Articulos"            
            generate_custom_queries(generated_lines, table_name, function_name, prompts_list)
        elif query_type == "CodigoArticulo":
            documento_tipo = "CodigoArticulo"            
            generate_custom_queries(generated_lines, table_name, function_name, prompts_list)
        elif query_type == "PrecioArticulo":
            documento_tipo = "PrecioArticulo"            
            generate_precioart_queries(generated_lines, table_name, function_name, prompts_list)         
        elif query_type == "CodeBar":
            documento_tipo = "CodeBar"
            generate_codebar_queries(generated_lines, table_name, function_name, prompts_list)
        elif query_type == "todo":
            documento_tipo = "todo"            
            generate_toda_la_info(generated_lines, table_name, function_name, prompts_list)            
        elif query_type == "todo_codigo":
            documento_tipo = "todo_codigo"            
            generate_toda_la_info(generated_lines, table_name, function_name, prompts_list)   


        with open(filepath, 'a', encoding='utf-8') as file:
            for line in generated_lines:
                file.write(line + '\n')
        return documento_tipo
