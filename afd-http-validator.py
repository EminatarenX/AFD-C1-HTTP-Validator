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

    def process(self, text):
        current_state = self.start_state
        buffer = ""
        valid_strings = []
        
        for char in text:
            if char in self.alphabet:
                if current_state in self.transition_function and char in self.transition_function[current_state]:
                    current_state = self.transition_function[current_state][char]
                    buffer += char
                else:
                    if current_state in self.final_states:
                        valid_strings.append(buffer.strip())
                    current_state = self.start_state
                    buffer = ""
                    if char in self.transition_function[self.start_state]:
                        current_state = self.transition_function[self.start_state][char]
                        buffer = char
            else:
                if current_state in self.final_states:
                    valid_strings.append(buffer.strip())
                current_state = self.start_state
                buffer = ""
        
        if current_state in self.final_states:
            valid_strings.append(buffer.strip())
        
        return valid_strings

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
        self.tree = ttk.Treeview(self.root, columns=("Posición", "Texto", "Categoría"), show="headings")
        self.tree.heading("Posición", text="Posición")
        self.tree.heading("Texto", text="Texto")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)
        self.status_label = tk.Label(self.root, text="", foreground="green")
        self.status_label.pack(pady=10)
        self.save_button = tk.Button(self.root, text="Guardar reporte CSV", command=self.save_csv, state=tk.DISABLED)
        self.save_button.pack(pady=10)
        self.ocurrencias = []

    def setup_dfa(self):
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
        content = self.read_file_content(file_path, extension)
        valid_strings = self.dfa.process(content)
        
        for i, http_request in enumerate(valid_strings, start=1):
            categoria = self.determinar_categoria(http_request)
            self.ocurrencias.append({
                'Posición': i,
                'Texto': http_request,
                'Categoría': categoria,
            })
        
        self.mostrar_resultados()
        self.save_button.config(state=tk.NORMAL)

    def read_file_content(self, file_path, extension):
        if extension == "txt":
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        elif extension == "csv":
            with open(file_path, 'r', encoding='utf-8') as file:
                return ' '.join(file.read().split())
        elif extension == "xlsx":
            try:
                df = pd.read_excel(file_path, header=None)
                return ' '.join(df.astype(str).values.flatten())
            except ImportError:
                messagebox.showerror("Error", "The openpyxl module is not installed. Please install it using 'pip install openpyxl'.")
                return ""
        elif extension == "docx":
            doc = Document(file_path)
            return ' '.join([para.text for para in doc.paragraphs])
        elif extension == "html":
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                return soup.get_text()
        else:
            messagebox.showerror("Error", "Formato de archivo no soportado.")
            return ""

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
            self.tree.insert("", "end", values=(ocurrencia['Posición'], ocurrencia['Texto'], ocurrencia['Categoría']))

    def save_csv(self):
        self.guardar_reporte_csv(self.ocurrencias)

    def guardar_reporte_csv(self, ocurrencias):
        try:
            with open('reporte.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['Posición', 'Texto', 'Categoría'])
                writer.writeheader()
                writer.writerows(ocurrencias)
            self.status_label.config(text="Reporte guardado exitosamente como 'reporte.csv'.", foreground="green")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el reporte CSV: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernGUI(root)
    root.mainloop()