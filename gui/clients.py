import tkinter as tk
from tkinter import ttk
from random import shuffle
import random
import json
import os
from utils.functions_clients import (
    generate_custom_queries, generate_telefon_queries, generate_email_queries,
    generate_direccio_queries, load_names_from_json, generate_custom_queries_multi,
    generate_direc_multi, generate_email_multi, generate_telefon_multi,
    generate_from_telefon, generate_phone_numbers, generate_todo_clientes,
    controlled_shuffle
)

def load_predefined_values():
    file_path = os.path.join("utils", "dicc_pre.json")
    with open(file_path, 'r') as f:
        return json.load(f)
    
predefined_values = load_predefined_values()
clientes_predefined = predefined_values['clientes']

class ClientTab:
    def __init__(self, master):
        self.frame = ttk.Frame(master)
        
        self.label_table = tk.Label(self.frame, text="Nom de la taula:")
        self.label_table.grid(row=0, column=0)
        self.entry_table = tk.Entry(self.frame)
        self.entry_table.grid(row=0, column=1)
        self.entry_table.insert(0, "cli")

        self.label_global_train_count = tk.Label(self.frame, text="Cantidad Train Global:")
        self.label_global_train_count.grid(row=0, column=2)
        self.entry_global_train_count = tk.Entry(self.frame)
        self.entry_global_train_count.grid(row=0, column=3)
        self.entry_global_train_count.insert(0, "10")
        self.entry_global_train_count.bind('<KeyRelease>', self.update_all_train_counts)
        tk.Label(self.frame, text="Cantidad Train").grid(row=1, column=2)

        self.button_toggle_all = tk.Button(self.frame, text="Toggle All", command=self.toggle_all)
        self.button_toggle_all.grid(row=1, column=3)        

        self.query_types = [
            "todo_cliente", "Info_Basic", "Telefon", "Email", "Direccion", "Info_Multi",
            "Telefon_Multi", "Email_Multi", "Direccion_Multi", "Telefono_cliente"
            ]
        
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
        function_names = {q_type: entry.get().strip() for q_type, entry in self.query_entries.items() if self.query_checkbutton_vars[q_type].get()}
        default_train_count = int(self.entry_train_count.get()) if hasattr(self, 'entry_train_count') else 100

        for query_type, function_name in function_names.items():
            train_count = int(self.query_train_counts.get(query_type, default_train_count).get())
            valid_count = int(train_count * 0.20)

            if query_type.endswith("_Multi"):
                train_count *= 2
                valid_count *= 2            
            if query_type == "Telefono_cliente":
                self.train_prompts_list, self.valid_prompts_list = generate_phone_numbers(train_count, valid_count)
            else:
                original_train_prompts = load_names_from_json()
                original_valid_prompts = load_names_from_json()
                shuffle(original_train_prompts)
                shuffle(original_valid_prompts)
                self.train_prompts_list = [original_train_prompts[i % len(original_train_prompts)] for i in range(train_count)]
                self.valid_prompts_list = [original_valid_prompts[i % len(original_valid_prompts)] for i in range(valid_count)]

            train_filepath = "Documents/dicc/results/train.jsonl"
            valid_filepath = "Documents/dicc/results/valid.jsonl"
            self.generate_file(train_filepath, self.train_prompts_list, query_type, function_name)
            self.generate_file(valid_filepath, self.valid_prompts_list, query_type, function_name) 

    def generate_file(self, filepath, prompts_list, query_type, function_name):
        is_valid = 'valid' in filepath
        table_name = self.entry_table.get().strip()
        generated_lines = []

        query_types = {
            "Telefon": ("Telefons", generate_telefon_queries),
            "Info_Basic": ("Clients", generate_custom_queries),
            "Email": ("Emails", generate_email_queries),
            "Direccion": ("Adreces", generate_direccio_queries),
            "Info_Multi": ("Custom_Multi", generate_custom_queries_multi),
            "Telefon_Multi": ("Telefon_Multi", generate_telefon_multi),
            "Email_Multi": ("Emails_Multi", generate_email_multi),
            "Direccion_Multi": ("Adreces_Multi", generate_direc_multi),
            "Telefono_cliente": ("Telefono_cliente", generate_from_telefon),
            "todo_cliente": ("todo_cliente", generate_todo_clientes)
        }

        if query_type in query_types:
            documento_tipo, generate_func = query_types[query_type]
            generate_func(generated_lines, table_name, function_name, prompts_list, is_valid)

            with open(filepath, 'a', encoding='utf-8') as file:
                for line in generated_lines:
                    file.write(line + '\n')

            return documento_tipo
