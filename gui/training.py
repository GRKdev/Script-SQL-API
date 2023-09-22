import tkinter as tk
from tkinter import ttk, messagebox
import os
import openai
import subprocess
import json
from dotenv import load_dotenv, set_key


class TrainingTab:
    def __init__(self, master):
        load_dotenv(".env")
        self.api_key = os.getenv("OPENAI_API_KEY")

        self.frame = ttk.Frame(master)

        self.api_label = tk.Label(self.frame, text="Clave API:")
        self.api_label.grid(row=0, column=0, pady=10)

        self.api_entry = tk.Entry(self.frame, width=30)
        if self.api_key:
            self.api_entry.insert(0, self.api_key)
        self.api_entry.grid(row=0, column=1, pady=10)

        self.upload_button = tk.Button(
            self.frame, text="Subir Archivos", command=self.upload_and_get_ids
        )
        self.upload_button.grid(row=0, column=3, pady=20)
        self.upload_button.config(width=11, height=2)

        self.model_label = tk.Label(self.frame, text="Modelo:")
        self.model_label.grid(row=1, column=0, pady=10)

        self.model_combo = ttk.Combobox(
            self.frame, values=["ada", "babbage-002", "gpt-3.5-turbo"]
        )
        self.model_combo.grid(row=1, column=1, pady=10)
        self.model_combo.current(0)

        self.message_label = tk.Label(self.frame, text="Mensaje:")
        self.message_label.grid(row=3, column=0, pady=10)

        self.message_entry = tk.Entry(self.frame, width=30)
        self.message_entry.grid(row=3, column=1, pady=10)

        self.final_button = tk.Button(
            self.frame, text="Enviar", command=self.send_final_query
        )
        self.final_button.grid(row=3, column=2, pady=20)
        self.final_button.config(bg="#7FFF7F")
        self.final_button.config(width=10, height=2)

        self.status_button = tk.Button(
            self.frame, text="Estado", command=self.check_status
        )
        self.status_button.grid(row=3, column=3, pady=20)
        self.status_button.config(width=10, height=2)

        self.cancel_button = tk.Button(
            self.frame, text="Cancelar", command=self.cancel_ft
        )
        self.cancel_button.grid(row=3, column=4, pady=20)
        self.cancel_button.config(bg="#FF7F84")
        self.cancel_button.config(width=10, height=2)

        self.fine_tune_label = tk.Label(self.frame, text="Seleccionar ID:")
        self.fine_tune_label.grid(row=5, column=0, pady=10)

        self.fine_tune_combo = ttk.Combobox(self.frame, width=1)
        self.fine_tune_combo.grid(row=5, column=1, pady=5)
        self.update_fine_tune_ids()

        self.check_selected_button = tk.Button(
            self.frame, text="Verificar Estado", command=self.check_selected_status
        )
        self.check_selected_button.grid(row=5, column=3, pady=20)
        self.check_selected_button.config(width=11, height=2)

        self.tree = ttk.Treeview(
            self.frame, columns=("ID", "Estado", "Costo", "Modelo Fine-Tuned")
        )
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Estado")
        self.tree.heading("#3", text="Costo")
        self.tree.heading("#4", text="Modelo Fine-Tuned")
        self.tree.grid(row=6, columnspan=4, pady=20)
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.fine_tuned_entry = tk.Entry(self.frame)
        self.fine_tuned_entry.grid(row=7, column=1, pady=5)

    def set_api_key(self):
        openai.api_key = self.api_key
        self.api_key = self.api_entry.get().strip()
        os.environ["OPENAI_API_KEY"] = self.api_key
        set_key(".env", "OPENAI_API_KEY", self.api_key)
        openai.api_key = self.api_key

    def upload_and_get_ids(self):
        self.set_api_key()

        if not self.api_key:
            tk.messagebox.showerror(
                "Error", "Por favor, introduce la clave API de OpenAI."
            )
            return

        try:
            train_response = openai.File.create(
                file=open("Documents/dicc/results/train.jsonl", "rb"),
                purpose="fine-tune",
            )
            train_id = train_response["id"]

            valid_response = openai.File.create(
                file=open("Documents/dicc/results/valid.jsonl", "rb"),
                purpose="fine-tune",
            )
            valid_id = valid_response["id"]

            self.train_id = train_id
            self.valid_id = valid_id

            tk.messagebox.showinfo(
                "IDs obtenidos", f"Train ID: {train_id}\nValid ID: {valid_id}"
            )

        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def save_to_file(self, train_id, valid_id, fine_tune_id, message):
        data = {
            "train_id": train_id,
            "valid_id": valid_id,
            "fine_tune_id": fine_tune_id,
            "message": message,
        }
        with open("training_history.json", "a") as file:
            json.dump(data, file)
            file.write("\n")

    def update_fine_tune_ids(self):
        self.message_to_id_map = {}
        messages = []
        try:
            with open("training_history.json", "r") as file:
                for line in file:
                    data = json.loads(line)
                    message = data["message"]
                    fine_tune_id = data["fine_tune_id"]
                    self.message_to_id_map[message] = fine_tune_id

                    messages.append(message)
        except FileNotFoundError:
            pass

        self.fine_tune_combo["values"] = messages
        self.fine_tune_combo.config(width=25)

    def send_final_query(self):
        selected_model = self.model_combo.get()

        if selected_model == "ada":
            self.send_final_query_ada()
        elif selected_model in ["babbage-002", "gpt-3.5-turbo"]:
            self.send_final_query_babbage_gpt()

    def send_final_query_babbage_gpt(self):
        message = self.message_entry.get().strip()
        selected_model = self.model_combo.get()

        try:
            response = openai.FineTuningJob.create(
                training_file=self.train_id,
                validation_file=self.valid_id,
                model=selected_model,
                suffix=message,
            )

            fine_tune_id = response["id"]
            tk.messagebox.showinfo("ID de Fine-Tune", fine_tune_id)
            self.fine_tune_id = fine_tune_id

        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
            return

        self.save_to_file(self.train_id, self.valid_id, self.fine_tune_id, message)
        self.update_fine_tune_ids()

    def send_final_query_ada(self):
        message = self.message_entry.get().strip()
        response = subprocess.check_output(
            [
                "openai",
                "api",
                "fine_tunes.create",
                "-t",
                self.train_id,
                "-v",
                self.valid_id,
                "-m",
                "ada",
                "--suffix",
                message,
            ],
            text=True,
        )
        print(response)

        for line in response.splitlines():
            if line.startswith("Created fine-tune:"):
                fine_tune_id = line.split(":")[1].strip()
                tk.messagebox.showinfo("ID de Fine-Tune", fine_tune_id)
                self.fine_tune_id = fine_tune_id
                break
        else:
            tk.messagebox.showerror(
                "Error", "No se encontró la ID de Fine-Tune en la respuesta."
            )

        self.save_to_file(self.train_id, self.valid_id, self.fine_tune_id, message)

        self.update_fine_tune_ids()

    def cancel_ft(self):
        if not hasattr(self, "fine_tune_id"):
            messagebox.showerror(
                "Error", "No has iniciado ningún entrenamiento recientemente."
            )
            return

        response = openai.FineTune.cancel(id=self.fine_tune_id)

        data = json.loads(response)

        tk.messagebox.showinfo("Estado del Cancelamiento", data["status"])

    def check_status(self):
        if not hasattr(self, "fine_tune_id"):
            messagebox.showerror(
                "Error", "No has iniciado ningún entrenamiento recientemente."
            )
            return

        response = subprocess.check_output(
            ["openai", "api", "fine_tunes.get", "-i", self.fine_tune_id], text=True
        )

        data = json.loads(response)

        error_messages = []
        cost = None

        for event in data.get("events", []):
            if "Fine-tune costs" in event.get("message", ""):
                cost = event["message"].split("$")[-1]

        for file_type, files in [
            ("Archivo de Entrenamiento", data.get("training_files", [])),
            ("Archivo de Validación", data.get("validation_files", [])),
        ]:
            for file in files:
                if file.get("status") == "error":
                    error_detail = file.get("status_details", "Detalles desconocidos.")
                    error_messages.append(f"{file_type}: {error_detail}")

        if error_messages:
            error_text = "\n".join(error_messages)
            tk.messagebox.showerror("Errores en los archivos", error_text)
        else:
            status_message = f"Estado: {data['status']}"
            if cost:
                status_message += f"\nCosto: ${cost}"
            tk.messagebox.showinfo("Estado del Entrenamiento", status_message)

    def check_selected_status(self):
        selected_message = self.fine_tune_combo.get()
        if not selected_message:
            messagebox.showerror("Error", "Selecciona un modelo de entrenamiento.")
            return

        selected_id = self.message_to_id_map.get(selected_message)
        if not selected_id:
            messagebox.showerror(
                "Error", "No se encontró una ID para el mensaje seleccionado."
            )
            return

        response = subprocess.check_output(
            ["openai", "api", "fine_tunes.get", "-i", selected_id], text=True
        )

        data = json.loads(response)

        error_messages = []

        fine_tuned_model = data.get("fine_tuned_model", "N/A")
        self.fine_tuned_entry.delete(0, tk.END)
        self.fine_tuned_entry.insert(0, fine_tuned_model)

        cost = next(
            (
                event["message"].split("$")[-1]
                for event in data["events"]
                if "Fine-tune costs" in event["message"]
            ),
            "N/A",
        )

        for file_type, files in [
            ("Archivo de Entrenamiento", data.get("training_files", [])),
            ("Archivo de Validación", data.get("validation_files", [])),
        ]:
            for file in files:
                if file.get("status") == "error":
                    error_detail = file.get("status_details", "Detalles desconocidos.")
                    error_messages.append(f"{file_type}: {error_detail}")

        if error_messages:
            error_text = "\n".join(error_messages)
            messagebox.showerror("Errores en los archivos", error_text)
        else:
            self.tree.insert(
                "", "end", values=(selected_id, data["status"], cost, fine_tuned_model)
            )
