import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import pandas as pd
from docx import Document
from bs4 import BeautifulSoup
import re
import string

class DFA:
    def __init__(self, states, alphabet, transition_function, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.final_states = final_states

    def accepts(self, input):
        current_state = self.start_state
        generated_string = ""

        for symbol in input:
            if symbol not in self.alphabet:
                return False, generated_string
            if current_state not in self.transition_function:
                return False, generated_string
            if symbol not in self.transition_function[current_state]:
                return False, generated_string
            current_state = self.transition_function[current_state][symbol]
            generated_string += symbol
        return current_state in self.final_states, generated_string.strip()

class ModernGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Archivos con AFD")
        
        self.setup_gui()
        self.setup_dfa()

    def setup_gui(self):
        self.label = tk.Label(self.root, text="Seleccione un archivo para analizar:")
        self.label.pack(pady=10)
        self.browse_button = tk.Button(self.root, text="Abrir archivo", command=self.browse_file)
        self.browse_button.pack(pady=5)
        self.tree = ttk.Treeview(self.root, columns=("Posición", "Texto", "Categoría", "Aceptada"), show="headings")
        self.tree.heading("Posición", text="Posición")
        self.tree.heading("Texto", text="Texto")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.heading("Aceptada", text="Aceptada")
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)
        self.status_label = tk.Label(self.root, text="", foreground="green")
        self.status_label.pack(pady=10)
        self.save_button = tk.Button(self.root, text="Guardar reporte CSV", command=self.save_csv, state=tk.DISABLED)
        self.save_button.pack(pady=10)
        self.ocurrencias = []

    def setup_dfa(self):
        # Configuración del AFD (usa la misma configuración que proporcionaste)
        states = [
            'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 
            'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17', 'q18', 'q19', 'q20', 
            'q21', 'q22', 'q23', 'q24', 'q25', 'q26', 'q27', 'q28', 'q29', 'q30', 
            'q31', 'q32', 'q33', 'q34', 'q35', 'q36', 'q37', 'q39', 'q40', 'q42', 
            'q43', 'q44', 'q45', 'q46', 'q47', 'q48', 'q49', 'q50', 'q51', 'q52', 
            'q53', 'q54', 'q55', 'q56', 'q57', 'q58', 'q59', 'q60', 'q61', 'q101'
        ]
        alphabet = set(string.ascii_lowercase + string.digits + 'GETDHP/.&=?OSUACL' + ' ')
        transition_function = {
    # Métodos HTTP
    'q0': {'G': 'q1', 'D': 'q17', 'P': 'q7', ' ': 'q0'},
    'q1': {'E': 'q2'}, 
    'q2': {'T': 'q3'},
    'q3': {' ': 'q4'}, 

    'q7': {'A': 'q8', 'U': 'q12', 'O': 'q14'},
    'q8': {'T': 'q9'},
    'q9': {'C': 'q10'},
    'q10': {'H': 'q11'},
    'q11': {' ': 'q4'},
    
    'q12': {'T': 'q13'},
    'q13': {' ': 'q4'},
    'q14': {'S': 'q15'},
    'q15': {'T': 'q16'},
    'q16': {' ': 'q4'},
    
    'q17': {'E': 'q18'},
    'q18': {'L': 'q19'},
    'q19': {'E': 'q20'},
    'q20': {'T': 'q21'},
    'q21': {'E': 'q22'},
    'q22':  {' ':  'q4'},
    
    # Path de la petición
    'q4': {' ': 'q4', '/': 'q61'},
    'q61': {**{char: 'q5' for char in string.ascii_lowercase + string.digits}},
    'q5': {**{char: 'q5' for char in string.ascii_lowercase + string.digits}, '/': 'q6', ' ': 'q23', '?': 'q56', '.': 'q34'},
    'q6': {**{char: 'q5' for char in string.ascii_lowercase + string.digits}},
    
    # Rutas estáticas y dinámicas
    'q34': {'j': 'q50', 'a': 'q47', 'p': 'q44', 'h': 'q35', 'c': 'q53'},
    'q50': {'s': 'q51', 'p': 'q42'},
    'q51': {'p': 'q52'},
    'q52': {'?': 'q56', ' ': 'q23'},
    'q47': {'s': 'q48'},
    'q48': {'p': 'q49'},
    'q49': {'?':  'q56', ' ':   'q23'},
    'q44': {'n': 'q45', 'h': 'q39'},
    'q45': {'g': 'q46'},
    'q46': {' ': 'q23'},
    'q42': {'g': 'q43'},
    'q43': {' ':'q23'},
    'q39': {'p': 'q40'},
    'q40': {'?': 'q56',' ': 'q23'},
    'q35': {'t': 'q36'},
    'q36': {'m': 'q37'},
    'q37': {'l': 'q101'},
    'q101': {' ':'q23'},
    'q53': {'s': 'q54'},
    'q54': {'s': 'q55'},
    
    # Query Parameters
    'q56': {**{char: 'q57' for char in string.ascii_lowercase + string.digits}},
    'q57': {**{char: 'q57' for char in string.ascii_lowercase + string.digits}, '=': 'q58'},
    'q58': {**{char: 'q59' for char in string.ascii_lowercase + string.digits}},
    'q59': {**{char: 'q59' for char in string.ascii_lowercase + string.digits}, '&': 'q60', ' ': 'q23'},
    'q60': {**{char: 'q57' for char in string.ascii_lowercase + string.digits}},
    
    # Version de http y estados finales
    'q23': {' ': 'q23', 'H': 'q24'},
    'q24': {'T': 'q25'},
    'q25': {'T': 'q26'},
    'q26': {'P': 'q27'},
    'q27': {'/': 'q28'},
    'q28': {'2': 'q33', '1': 'q29'},
    'q29': {'.': 'q30'},
    'q30': {'0': 'q31', '1': 'q32'},
    
}
        start_state = 'q0'
        final_states = ['q31', 'q32', 'q33']
        self.dfa = DFA(states, alphabet, transition_function, start_state, final_states)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt *.csv *.xlsx *.docx *.html")])
        if file_path:
            self.analyze_file(file_path)

    def analyze_file(self, file_path):
        self.ocurrencias = []
        extension = file_path.split('.')[-1].lower()
        if extension == "txt":
            self.leer_txt(file_path)
        elif extension == "csv":
            self.leer_csv(file_path)
        elif extension == "xlsx":
            self.leer_xlsx(file_path)
        elif extension == "docx":
            self.leer_docx(file_path)
        elif extension == "html":
            self.leer_html(file_path)
        else:
            messagebox.showerror("Error", "Formato de archivo no soportado.")
            return
        
        self.mostrar_resultados()
        self.save_button.config(state=tk.NORMAL)

    def leer_txt(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                self.procesar_linea(line.strip(), i+1)

    def leer_csv(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for i, row in enumerate(reader, start=1):
                if len(row) >= 3:  # Ensure the row has at least 3 elements
                    http_request = f"{row[1]} {row[0]} {row[2]}"
                    self.procesar_linea(http_request.strip(), i)

    def leer_xlsx(self, file_path):
        try:
            df = pd.read_excel(file_path, header=None)  # Read without assuming header
            for i, row in df.iterrows():
                if len(row) >= 3:  # Ensure we have at least URL, Method, and Version
                    url = str(row[0]).strip()
                    method = str(row[1]).strip()
                    version = str(row[2]).strip()
                    http_request = f"{method} {url} {version}"
                    self.procesar_linea(http_request, i+1)
        except ImportError:
            messagebox.showerror("Error", "The openpyxl module is not installed. Please install it using 'pip install openpyxl'.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the Excel file: {str(e)}")

    def leer_docx(self, file_path):
        doc = Document(file_path)
        for i, para in enumerate(doc.paragraphs):
            self.procesar_linea(para.text.strip(), i+1)

    def leer_html(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            for i, tag in enumerate(soup.find_all()):
                self.procesar_linea(tag.get_text().strip(), i+1)

    def procesar_linea(self, texto, posicion):
        is_accepted, generated_string = self.dfa.accepts(texto)
        if is_accepted: 
            categoria = self.determinar_categoria(texto)
            self.ocurrencias.append({
                'Posición': posicion,
                'Texto': generated_string,
                'Categoría': categoria,
                'Aceptada': 'Sí' if is_accepted else 'No'
            })

    def determinar_categoria(self, url):
        if url.startswith("/api"):
            return "API"
        elif "?" in url:
            return "Recurso Dinámico"
        elif re.search(r'\.\w{2,4}($|\?)', url):
            return "Recurso Estático"
        else:
            return "Otro"

    def mostrar_resultados(self):
        self.tree.delete(*self.tree.get_children())
        for ocurrencia in self.ocurrencias:
            self.tree.insert("", "end", values=(ocurrencia['Posición'], ocurrencia['Texto'], ocurrencia['Categoría'], ocurrencia['Aceptada']))

    def save_csv(self):
        self.guardar_reporte_csv(self.ocurrencias)

    def guardar_reporte_csv(self, ocurrencias):
        try:
            with open('reporte.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['Posición', 'Texto', 'Categoría', 'Aceptada'])
                writer.writeheader()
                writer.writerows(ocurrencias)
            self.status_label.config(text="Reporte guardado exitosamente como 'reporte.csv'.", foreground="green")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el reporte CSV: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernGUI(root)
    root.mainloop()