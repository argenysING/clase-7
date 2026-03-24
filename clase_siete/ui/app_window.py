import tkinter as tk
from tkinter import ttk, messagebox
from service.task_service import TaskService

class AppWindow(tk.Tk):
 
    def __init__(self, task_service: TaskService) -> None:
        super().__init__()
        self._task_service = task_service
 
        self.title("Gestor de Tareas")
        self.geometry("600x500")
        self.resizable(False, False)
        self.configure(bg="#e8f0fd")
        self.create_widgets()
 
    def create_widgets(self) -> None:
        # ── Título principal ──────────────────────────────────────
        tk.Label(self, text="Gestor de Tareas",bg="lightblue", font=("Arial", 16, "bold")).pack(pady=10)
 
        # ── Formulario ────────────────────────────────────────────
        form_frame = tk.Frame(self)
        form_frame.pack(pady=5)
 
        tk.Label(form_frame, text="Título:", bg="gray").grid(row=0, column=0, sticky="e", padx=5, pady=4)
        self.input_title = tk.Entry(form_frame, width=35)
        self.input_title.grid(row=0, column=1, padx=5, pady=4)
 
        tk.Label(form_frame, text="Descripción:", bg="gray").grid(row=1, column=0, sticky="e", padx=5, pady=4)
        self.input_description = tk.Entry(form_frame, width=35, bg="#f6f3ea")
        self.input_description.grid(row=1, column=1, padx=5, pady=4)
 
        tk.Button(self, text="Registrar tarea",bg="green", command=self.register_task).pack(pady=8)
 
        # ── Treeview ──────────────────────────────────────────────
        columns = ("col_uuid", "col_title", "col_desc")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
 
        self.tree.heading("col_uuid",  text="UUID")
        self.tree.heading("col_title", text="Título")
        self.tree.heading("col_desc",  text="Descripción")
 
        self.tree.column("col_uuid",  width=220, anchor="center")
        self.tree.column("col_title", width=150, anchor="center")
        self.tree.column("col_desc",  width=200, anchor="w")
 
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
 
        # Carga inicial de datos
        self.refresh_table()
 
    def register_task(self) -> None:
        title       = self.input_title.get().strip()
        description = self.input_description.get().strip()
 
        if not title or not description:
            messagebox.showwarning("Campos vacíos", "Por favor completa el título y la descripción.")
            return
 
        self._task_service.create_one_task(title, description)  
        self.refresh_table()
        self.clear_inputs()
 
    def refresh_table(self) -> None:
        # Limpiar filas existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
 
        # Insertar todas las tareas desde el servicio (acceso por atributo, no por clave)
        for task in self._task_service.get_all_tasks():
            self.tree.insert("", "end", values=(task.uuid, task.title, task.description))
 
    def clear_inputs(self) -> None:
        self.input_title.delete(0, "end")
        self.input_description.delete(0, "end")