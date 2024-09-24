import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import pandas as pd
import docx
from bs4 import BeautifulSoup

class ModernGUI:
    def __init__(self, master):
        self.master = master
        master.title("HTTP-ReqAnalyzer")
        master.geometry("800x600")
        master.configure(bg="#f0f0f0")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", padding=10, relief="flat", background="#4CAF50", foreground="white")
        self.style.map("TButton", background=[("active", "#45a049")])
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        self.style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))

        self.create_widgets()

    def create_widgets(self):
        # Header
        header = ttk.Label(self.master, text="HTTP-ReqAnalyzer", style="Header.TLabel")
        header.pack(pady=20)

        # Frame para el botón de carga y la etiqueta del archivo
        load_frame = ttk.Frame(self.master, padding="10")
        load_frame.pack(fill="x", padx=20)

        self.btn_cargar = ttk.Button(load_frame, text="Cargar archivo", command=self.cargar_archivo)
        self.btn_cargar.pack(side="left", padx=(0, 10))

        self.label_archivo = ttk.Label(load_frame, text="No se ha cargado ningún archivo")
        self.label_archivo.pack(side="left")

        # Frame para los resultados
        result_frame = ttk.Frame(self.master, padding="10")
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview para mostrar los resultados
        self.tree = ttk.Treeview(result_frame, columns=("Posición", "Categoría", "Aceptada", "Texto"), show="headings")
        self.tree.heading("Posición", text="Posición")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.heading("Aceptada", text="Aceptada")
        self.tree.heading("Texto", text="Texto")
        self.tree.column("Posición", width=70)
        self.tree.column("Categoría", width=100)
        self.tree.column("Aceptada", width=70)
        self.tree.column("Texto", width=400)
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Etiqueta de estado
        self.status_label = ttk.Label(self.master, text="", foreground="green")
        self.status_label.pack(pady=10)

    def cargar_archivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos permitidos", "*.xlsx *.csv *.docx *.html")])
        if file_path:
            self.label_archivo.config(text=f"Archivo cargado: {file_path}")
            self.procesar_archivo(file_path)
        else:
            messagebox.showerror("Error", "No se ha seleccionado ningún archivo.")

    def procesar_archivo(self, file_path):
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.docx'):
                df = self.leer_docx(file_path)
            elif file_path.endswith('.html'):
                df = self.leer_html(file_path)
            else:
                messagebox.showerror("Error", "Formato de archivo no compatible.")
                return

            self.analizar_contenido(df)
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el archivo: {str(e)}")

    def leer_docx(self, file_path):
        try:
            doc = docx.Document(file_path)
            full_text = [para.text for para in doc.paragraphs]
            return pd.DataFrame(full_text, columns=["Contenido"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo DOCX: {e}")
            return pd.DataFrame(columns=["Contenido"])

    def leer_html(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text().splitlines()
            return pd.DataFrame(text, columns=["Contenido"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo HTML: {e}")
            return pd.DataFrame(columns=["Contenido"])

    def analizar_contenido(self, dataframe):
        ocurrencias = []
        for index, row in dataframe.iterrows():
            cadena = row.iloc[0]
            resultado, categoria = self.afd(cadena)
            ocurrencias.append({
                'Posición': index + 1,
                'Texto': cadena,
                'Categoría': categoria if resultado else "No aceptada",
                'Aceptada': "Sí" if resultado else "No"
            })

        # Limpiar Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Insertar nuevos datos
        for ocurrencia in ocurrencias:
            self.tree.insert("", "end", values=(ocurrencia['Posición'], ocurrencia['Categoría'], 
                                                ocurrencia['Aceptada'], ocurrencia['Texto']))

        # Guardar el reporte en CSV
        self.guardar_reporte_csv(ocurrencias)

    def afd(self, cadena):
        metodos = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
        versiones = ["HTTP/1.0", "HTTP/1.1", "HTTP/2"]

        partes = cadena.split(" ")
        if len(partes) != 3:
            return False, ""

        metodo, url, version = partes

        if metodo not in metodos:
            return False, ""

        if not url.startswith("/") or " " in url:
            return False, ""

        if version not in versiones:
            return False, ""

        if url.startswith("/api/"):
            categoria = "API"
        elif any(url.endswith(ext) for ext in [".html", ".css", ".jpg", ".png", ".js"]):
            categoria = "Recurso Estático"
        elif any(url.endswith(ext) for ext in [".php", ".asp", ".jsp"]):
            categoria = "Recurso Dinámico"
        else:
            categoria = "Otro"

        return True, categoria

    def guardar_reporte_csv(self, ocurrencias):
        try:
            with open('reporte_ocurrencias.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Posición', 'Texto', 'Categoría', 'Aceptada']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for ocurrencia in ocurrencias:
                    writer.writerow(ocurrencia)
            self.status_label.config(text="Reporte guardado en 'reporte_ocurrencias.csv'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el reporte: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernGUI(root)
    root.mainloop()