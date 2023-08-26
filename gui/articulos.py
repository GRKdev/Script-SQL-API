import tkinter as tk
from tkinter import ttk, messagebox
from utils.functions_articulos import generate_custom_queries, generate_proveedores_queries, load_prompts_from_json, generate_random_numbers, generate_precioart_queries, generate_random_bars, generate_codebar_queries,generate_toda_la_info

class ArticulosTab:
    def __init__(self, master):
        self.frame = ttk.Frame(master)

        self.train_prompts_list = load_prompts_from_json
        self.valid_prompts_list = load_prompts_from_json

        self.query_type_label = tk.Label(self.frame, text="Tipo de consulta:")
        self.query_type_label.grid(row=1, column=0, pady=(10, 10))
        self.query_type = ttk.Combobox(self.frame, values=["Articulos", "Proveidor","CodigoArticulo","PrecioArticulo", "CodeBar","todo","todo_codigo"], state="readonly")
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
        
        if self.query_type.get() == "CodigoArticulo":
            self.train_prompts_list, self.valid_prompts_list = generate_random_numbers(train_count, valid_count)
        elif self.query_type.get() == "todo_codigo":
            self.train_prompts_list, self.valid_prompts_list = generate_random_numbers(train_count, valid_count)
        elif self.query_type.get() == "CodeBar":
            self.train_prompts_list, self.valid_prompts_list = generate_random_bars(train_count, valid_count)
        else:
            original_train_prompts = load_prompts_from_json()
            original_valid_prompts = load_prompts_from_json()

            self.train_prompts_list = [original_train_prompts[i % len(original_train_prompts)] for i in range(train_count)]
            self.valid_prompts_list = [original_valid_prompts[i % len(original_valid_prompts)] for i in range(valid_count)]
        
        train_filepath = "Documents/dicc/results/train.jsonl"
        valid_filepath = "Documents/dicc/results/valid.jsonl"

        documento_tipo = self.generate_file(train_filepath, self.train_prompts_list)
        self.generate_file(valid_filepath, self.valid_prompts_list)

        messagebox.showinfo("Correcte", f"Arxius JsonL de {documento_tipo} creats amb exit!")

    def generate_file(self, filepath, prompts_list):
        table_name = self.entry_table.get().strip()
        function_name = self.entry_function_name.get().strip()

        generated_lines = []

        if self.query_type.get() == "Proveidor":
            documento_tipo = "Proveidor"            
            generate_proveedores_queries(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "Articulos":
            documento_tipo = "Articulos"            
            generate_custom_queries(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "CodigoArticulo":
            documento_tipo = "CodigoArticulo"            
            generate_custom_queries(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "PrecioArticulo":
            documento_tipo = "PrecioArticulo"            
            generate_precioart_queries(generated_lines, table_name, function_name, prompts_list)         
        elif self.query_type.get() == "CodeBar":
            documento_tipo = "CodeBar"
            generate_codebar_queries(generated_lines, table_name, function_name, prompts_list)
        elif self.query_type.get() == "todo":
            documento_tipo = "todo"            
            generate_toda_la_info(generated_lines, table_name, function_name, prompts_list)            
        elif self.query_type.get() == "todo_codigo":
            documento_tipo = "todo_codigo"            
            generate_toda_la_info(generated_lines, table_name, function_name, prompts_list)   

        with open(filepath, 'a', encoding='utf-8') as file:
            for line in generated_lines:
                file.write(line + '\n')
        return documento_tipo
