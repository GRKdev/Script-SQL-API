import tkinter as tk
from tkinter import ttk
from utils.functions_clients import generate_custom_queries, generate_telefon_queries, generate_email_queries, generate_direccio_queries, load_names_from_json, generate_custom_queries_multi
from utils.functions_clients import generate_custom_queries_multi, generate_direc_multi, generate_email_multi,generate_telefon_multi, generate_from_telefon, generate_phone_numbers, generate_todo_clientes
from random import shuffle

class ClientTab:
    def __init__(self, master):
        self.frame = ttk.Frame(master)

        self.train_prompts_list = load_names_from_json
        self.valid_prompts_list = load_names_from_json

        self.query_type_label = tk.Label(self.frame, text="Tipo de consulta:")
        self.query_type_label.grid(row=1, column=0, pady=(10, 10))
        self.query_type = ttk.Combobox(self.frame, values=["todo_cliente","Custom", "Telefon", "Email", "Direccion", "Custom_Multi", "Telefon_Multi", "Email_Multi", "Direccion_Multi", "Telefono_cliente"], state="readonly")
        self.query_type.grid(row=1, column=1, pady=(10, 10))
        self.query_type.set("Custom") 

        self.label_train_count = tk.Label(self.frame, text="Quantitat dades Train(20% Valid)")
        self.label_train_count.grid(row=2, column=0, pady=(10, 10))
        self.entry_train_count = tk.Entry(self.frame)
        self.entry_train_count.grid(row=2, column=1, pady=(10, 10))
        self.entry_train_count.insert(0, "100")

        self.label_table = tk.Label(self.frame, text="Nom de la taula:")
        self.label_table.grid(row=3, column=0, pady=(10, 5))
        self.entry_table = tk.Entry(self.frame)
        self.entry_table.grid(row=3, column=1, pady=(10, 5))

        self.label_function_name = tk.Label(self.frame, text="Nom de la funció:")
        self.label_function_name.grid(row=4, column=0, pady=(10, 5))
        self.entry_function_name = tk.Entry(self.frame)
        self.entry_function_name.grid(row=4, column=1, pady=(10, 5))

        self.button_generate = tk.Button(self.frame, text="Genera el Arxiu", command=self.generate_jsonl)
        self.button_generate.grid(row=12, column=0, columnspan=2, pady=(20, 10))


    def generate_jsonl(self):
        train_count = int(self.entry_train_count.get())
        valid_count = int(train_count * 0.20)

        if self.query_type.get().endswith("_Multi"):
            train_count *= 2

        if self.query_type.get() == "Telefono_cliente":
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

        self.generate_file(train_filepath, self.train_prompts_list)
        self.generate_file(valid_filepath, self.valid_prompts_list)



    def generate_file(self, filepath, prompts_list):
        table_name = self.entry_table.get().strip()
        function_name = self.entry_function_name.get().strip()

        generated_lines = []

        if self.query_type.get() == "Telefon":
            documento_tipo = "Telefons"            
            generate_telefon_queries(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "Custom":
            documento_tipo = "Clients"            
            generate_custom_queries(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "Email":
            documento_tipo = "Emails"            
            generate_email_queries(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "Direccion":
            documento_tipo = "Adreces"            
            generate_direccio_queries(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "Custom_Multi":
            documento_tipo = "Custom_Multi"            
            generate_custom_queries_multi(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "Telefon_Multi":
            documento_tipo = "Telefon_Multi"            
            generate_telefon_multi(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "Email_Multi":
            documento_tipo = "Emails_Multi"            
            generate_email_multi(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "Direccion_Multi":
            documento_tipo = "Adreces_Multi"            
            generate_direc_multi(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "Telefono_cliente":
            documento_tipo = "Telefono_cliente"            
            generate_from_telefon(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "todo_cliente":
            documento_tipo = "todo_cliente"            
            generate_todo_clientes(generated_lines, table_name, function_name, prompts_list)

        with open(filepath, 'a', encoding='utf-8') as file:
            for line in generated_lines:
                file.write(line + '\n')
        return documento_tipo
