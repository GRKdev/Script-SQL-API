import tkinter as tk
from tkinter import ttk, messagebox
from utils.functions_albarans import generate_albaran_queries, generate_pedidos_queries, generate_facturas_queries, generate_random_prompts

class AlbaranesTab:
    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.train_prompts_list, self.valid_prompts_list = generate_random_prompts()
        self.create_gui()

    def create_gui(self):

        self.query_type_label = tk.Label(self.frame, text="Tipo de consulta:")
        self.query_type_label.grid(row=1, column=0, pady=(10, 10))
        self.query_type = ttk.Combobox(self.frame, values=["Albaran", "Factura", "Pedido"], state="readonly")
        self.query_type.grid(row=1, column=1, pady=(10, 10))
        self.query_type.set("Custom") 

        self.label_train_count = tk.Label(self.frame, text="Quantitat dades Train(20% Valid)")
        self.label_train_count.grid(row=2, column=0, pady=(10, 10))
        self.entry_train_count = tk.Entry(self.frame)
        self.entry_train_count.grid(row=2, column=1, pady=(10, 10))
        self.entry_train_count.insert(0, "100")  # Valor por defecto

        self.label_table = tk.Label(self.frame, text="Nom de la taula:")
        self.label_table.grid(row=3, column=0, pady=(10, 5))
        self.entry_table = tk.Entry(self.frame)
        self.entry_table.grid(row=3, column=1, pady=(10, 5))

        self.label_function_name = tk.Label(self.frame, text="Nom de la funció:")
        self.label_function_name.grid(row=4, column=0, pady=(10, 5))
        self.entry_function_name = tk.Entry(self.frame)
        self.entry_function_name.grid(row=4, column=1, pady=(10, 5))

        # Botón de generar archivo
        self.button_generate = tk.Button(self.frame, text="Genera el Arxiu", command=self.generate_jsonl)
        self.button_generate.grid(row=12, column=0, columnspan=2, pady=(20, 10))


    def generate_jsonl(self):
        train_count = int(self.entry_train_count.get())
        valid_count = int(train_count * 0.20)  # Calcula el 20%
        
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
