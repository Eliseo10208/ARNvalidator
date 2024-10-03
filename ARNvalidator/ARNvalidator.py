import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
from docx import Document
from bs4 import BeautifulSoup
import csv
import os

# Definición de los estados
states = [
    'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 
    'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17', 'q18', 'q19', 'q20', 
    'q21', 'q22', 'q23', 'q24', 'q25', 'q26', 'q27', 'q28', 'q29', 'q30', 
    'q31', 'q32', 'q33', 'q34', 'q35', 'q36', 'q37', 'q38', 'q39', 'q40', 
    'q41', 'q42', 'q43', 'q44', 'q45', 'q46', 'q47', 'q48', 'q49', 'q50', 
    'q51', 'q52', 'q53', 'q54', 'q55', 'q56', 'q57', 'q58', 'q59', 'q60', 
    'q61', 'q62', 'q63', 'q64', 'q65', 'q66', 'q67', 'q68', 'q69', 'q70', 
    'q71', 'q72', 'q73', 'q74', 'q75', 'q76', 'q77', 'q78', 'q79', 'q80', 
    'q81', 'q82', 'q83', 'q84', 'q85', 'q86', 'q87', 'q88', 'q89', 'q90', 
    'q91', 'q92', 'q93', 'q94', 'q95', 'q96', 'q97', 'q98', 'q99', 'q100', 
    'q101', 'q102', 'q103', 'q104', 'q105', 'q106', 'q107', 'q108', 'q109', 'q110', 
    'q111', 'q112', 'q113', 'q114', 'q115', 'q116', 'q117', 'q118', 'q119', 'q120', 
    'q121', 'q122', 'q123', 'q124', 'q125', 'q126', 'q127', 'q128', 'q129', 'q130', 
    'q131', 'q132', 'q133', 'q134', 'q135', 'q136', 'q137', 'q138', 'q139', 'q140', 
    'q141', 'q142', 'q143', 'q144', 'q145', 'q146', 'q147', 'q148', 'q149', 'q150', 
    'q151', 'q152', 'q153', 'q154', 'q155', 'q156', 'q157', 'q158', 'q159', 'q160', 
    'q161', 'q162', 'q163', 'q164', 'q165', 'q166', 'q167', 'q168', 'q169', 'q170', 
    'q171', 'q172', 'q173', 'q174', 'q175', 'q176', 'q177', 'q178', 'q179', 'q180', 
    'q181', 'q182', 'q183', 'q184', 'q185', 'q186', 'q187', 'q188', 'q189', 'q190', 
    'q191', 'q192', 'q193', 'q194', 'q195', 'q196', 'q197', 'q198', 'q199'
]

# Definición del diccionario de transiciones
diccionario = {
    # arn:aws
    'q0': {'a': 'q1'},
    'q1': {'r': 'q2'},
    'q2': {'n': 'q3'},
    'q3': {':': 'q4'},
    'q4': {'a': 'q5'},
    'q5': {'w': 'q6'},
    'q6': {'s': 'q7'},
    'q7': {':': 'q8'},
    # ec2
    'q8': {'e': 'q20', 's': 'q9', 'l': 'q14'},
    'q20': {'c': 'q21'},
    'q21': {'2': 'q19'},
    'q19': {':': 'q22'},
    # s3
    'q9': {'3': 'q10'},
    'q10': {':': 'q11'},
    'q11': {':': 'q12'},
    'q12': {':': 'q13'},
    'q13': {
        'a': 'q13', 'b': 'q13', 'c': 'q13', 'd': 'q13', 'e': 'q13', 'f': 'q13', 'g': 'q13',
        'h': 'q13', 'i': 'q13', 'j': 'q13', 'k': 'q13', 'l': 'q13', 'm': 'q13', 'n': 'q13',
        'o': 'q13', 'p': 'q13', 'q': 'q13', 'r': 'q13', 's': 'q13', 't': 'q13', 'u': 'q13',
        'v': 'q13', 'w': 'q13', 'x': 'q13', 'y': 'q13', 'z': 'q13', '0': 'q13', '1': 'q13',
        '2': 'q13', '3': 'q13', '4': 'q13', '5': 'q13', '6': 'q13', '7': 'q13', '8': 'q13',
        '9': 'q13', '/': 'q13', '-': 'q13', '_': 'q13', '.': 'q13'
    },
    # lambda
    'q14': {'a': 'q15'},
    'q15': {'m': 'q16'},
    'q16': {'b': 'q17'},
    'q17': {'d': 'q18'},
    'q18': {'a': 'q19'},
    # regiones us-east-1
    'q22': {'u': 'q23', 'e': 'q37'},
    'q23': {'s': 'q24'},
    'q24': {'-': 'q25'},
    'q25': {'e': 'q26', 'w': 'q32'},
    'q26': {'a': 'q27'},
    'q27': {'s': 'q28'},
    'q28': {'t': 'q29'},
    'q29': {'-': 'q30'},
    'q30': {'1': 'q31'},
    # regiones us-west-2
    'q32': {'e': 'q33'},
    'q33': {'s': 'q34'},
    'q34': {'t': 'q35'},
    'q35': {'-': 'q36'},
    'q36': {'2': 'q31'},
    # regiones eu-west-2
    'q37': {'u': 'q38'},
    'q38': {'-': 'q39'},
    'q39': {'w': 'q40'},
    'q40': {'e': 'q41'},
    'q41': {'s': 'q42'},
    'q42': {'t': 'q43'},
    'q43': {'-': 'q44'},
    'q44': {'1': 'q31'},
    # idCuenta
    'q31': {':': 'q45'},
    'q45': {str(i): 'q46' for i in range(10)},  # '0'-'9'
    'q46': {str(i): 'q47' for i in range(10)},
    'q47': {str(i): 'q48' for i in range(10)},
    'q48': {str(i): 'q49' for i in range(10)},
    'q49': {str(i): 'q50' for i in range(10)},
    'q50': {str(i): 'q51' for i in range(10)},
    'q51': {str(i): 'q52' for i in range(10)},
    'q52': {str(i): 'q53' for i in range(10)},
    'q53': {str(i): 'q54' for i in range(10)},
    'q54': {str(i): 'q55' for i in range(10)},
    'q55': {str(i): 'q56' for i in range(10)},
    'q56': {str(i): 'q57' for i in range(10)},
    'q57': {':': 'q58'},
     'q58': {'f': 'q59','s': 'q66','i': 'q105','n': 'q144','k':'q121','v':'q130','e':'q164'},
    'q59': {'u': 'q60'},
    'q60': {'n': 'q61'},
    'q61': {'c': 'q62'},
    'q62': {'t': 'q63'},
    'q63': {'i': 'q64'},
    'q64': {'o': 'q65'},
    'q65': {'n': 'q12'},
    'q12': {':': 'q13'},
    #subnet
    'q66': {'u': 'q67','e': 'q79','n': 'q94'},
    'q67': {'b': 'q68'},
    'q68': {'n': 'q69'},
    'q69': {'e': 'q70'},
    'q70': {'t': 'q71'},
    'q71': {'/': 'q72'},
    'q72': {'s': 'q73'},
    'q73': {'u': 'q74'},
    'q74': {'b': 'q75'},
    'q75': {'n': 'q76'},
    'q76': {'e': 'q77'},
    'q77': {'t': 'q78'},
    'q78': {'-': 'q182'},
   
    'q79': {'c': 'q80'},
    'q80': {'u': 'q81'},
    'q81': {'r': 'q82'},
    'q82': {'i': 'q83'},
    'q83': {'t': 'q84'},
    'q84': {'y': 'q85'},
    'q85': {'-': 'q86'},
    'q86': {'g': 'q87'},
    'q87': {'r': 'q88'},
    'q88': {'o': 'q89'},
    'q89': {'u': 'q90'},
    'q90': {'p': 'q91'},
    'q91': {'/': 'q92'},
    'q92': {'s': 'q93'},
    'q93': {'g': 'q78'},
    # Bifurcación snapshot/snap-
    
    'q94': {'a': 'q95'},
    'q95': {'p': 'q96'},
    'q96': {'s': 'q97'},
    'q97': {'h': 'q98'},
    'q98': {'o': 'q99'},
    'q99': {'t': 'q100'},
    'q100': {'/': 'q101'},
    'q101': {'s': 'q102'},
    'q102': {'n': 'q103'},
    'q103': {'a': 'q104'},
    'q104': {'p': 'q78'},
       # Bifurcación para image/ami
    'q105': {'m': 'q106','n': 'q113'},
    'q106': {'a': 'q107'},
    'q107': {'g': 'q108'},
    'q108': {'e': 'q109'},
    'q109': {'/': 'q110'},
    'q110': {'a': 'q111'},
    'q111': {'m': 'q112'},
    'q112': {'i': 'q78'},
     # Bifurcación para instance/i
   
    'q113': {'s': 'q114'},
    'q114': {'t': 'q115'},
    'q115': {'a': 'q116'},
    'q116': {'n': 'q117'},
    'q117': {'c': 'q118'},
    'q118': {'e': 'q119'},
    'q119': {'/': 'q120'},
    'q120': {'i': 'q78'},
    
    
    # Bifurcación para key-pair/
     'q121': {'e': 'q122'},
    'q122': {'y': 'q123'},
    'q123': {'-': 'q124'},
    'q124': {'p': 'q125'},
    'q125': {'a': 'q126'},
    'q126': {'i': 'q127'},
    'q127': {'r': 'q128'},
    'q128': {'/': 'q129'},
      'q129': {
        'a': 'q129', 'b': 'q129', 'c': 'q129', 'd': 'q129', 'e': 'q129', 'f': 'q129', 'g': 'q129', 'h': 'q129',
        'i': 'q129', 'j': 'q129', 'k': 'q129', 'l': 'q129', 'm': 'q129', 'n': 'q129', 'o': 'q129', 'p': 'q129',
        'q': 'q129', 'r': 'q129', 's': 'q129', 't': 'q129', 'u': 'q129', 'v': 'q129', 'w': 'q129', 'x': 'q129',
        'y': 'q129', 'z': 'q129', '0': 'q129', '1': 'q129', '2': 'q129', '3': 'q129', '4': 'q129', '5': 'q129',
        '6': 'q129', '7': 'q129', '8': 'q129', '9': 'q129', '/': 'q129', '-': 'q129', '_': 'q129', '.': 'q129',
    },
    'q130': {'p': 'q131','o': 'q136'},
    'q131': {'c': 'q132'},
    'q132': {'/': 'q133'},
    'q133': {'v': 'q134'},
    'q134': {'p': 'q135'},
    'q135': {'c': 'q78'},
    # Bifurcación para vpc/vpc-
    'q136': {'l': 'q137'},
    'q137': {'u': 'q138'},
    'q138': {'m': 'q139'},
    'q139': {'e': 'q140'},
    'q140': {'/': 'q141'},
    'q141': {'v': 'q142'},
    'q142': {'o': 'q143'},
    'q143': {'l': 'q78'},
    # Bifurcación network-interface/eni
    'q144': {'e': 'q145'},
    'q145': {'t': 'q146'},
    'q146': {'w': 'q147'},
    'q147': {'o': 'q148'},
    'q148': {'r': 'q149'},
    'q149': {'k': 'q150'},
    'q150': {'-': 'q151'},
    'q151': {'i': 'q152'},
    'q152': {'n': 'q153'},
    'q153': {'t': 'q154'},
    'q154': {'e': 'q155'},
    'q155': {'r': 'q156'},
    'q156': {'f': 'q157'},
    'q157': {'a': 'q158'},
    'q158': {'c': 'q159'},
    'q159': {'e': 'q160'},
    'q160': {'/': 'q161'},
    'q161': {'e': 'q162'},
    'q162': {'n': 'q163'},
    'q163': {'i': 'q78'},
   # Bifurcacion elastic-ip/eipalloc
    'q164': {'l': 'q165'},
    'q165': {'a': 'q166'},
    'q166': {'s': 'q167'},
    'q167': {'t': 'q168'},
    'q168': {'i': 'q169'},
    'q169': {'c': 'q170'},
    'q170': {'-': 'q171'},
    'q171': {'i': 'q172'},
    'q172': {'p': 'q173'},
    'q173': {'/': 'q174'},
    'q174': {'e': 'q175'},
    'q175': {'i': 'q176'},
    'q176': {'p': 'q177'},
    'q177': {'a': 'q178'},
    'q178': {'l': 'q179'},
    'q179': {'l': 'q180'},
    'q180': {'o': 'q181'},
    'q181': {'c': 'q78'},
    
# Ultimos id de ec2 para finalizar
    'q182': {c: 'q183' for c in 'abcdef0123456789'},
    'q183': {c: 'q184' for c in 'abcdef0123456789'},
    'q184': {c: 'q185' for c in 'abcdef0123456789'},
    'q185': {c: 'q186' for c in 'abcdef0123456789'},
    'q186': {c: 'q187' for c in 'abcdef0123456789'},
    'q187': {c: 'q188' for c in 'abcdef0123456789'},
    'q188': {c: 'q189' for c in 'abcdef0123456789'},
    'q189': {c: 'q190' for c in 'abcdef0123456789'},
    'q190': {c: 'q191' for c in 'abcdef0123456789'},
    'q191': {c: 'q192' for c in 'abcdef0123456789'},
    'q192': {c: 'q193' for c in 'abcdef0123456789'},
    'q193': {c: 'q194' for c in 'abcdef0123456789'},
    'q194': {c: 'q195' for c in 'abcdef0123456789'},
    'q195': {c: 'q196' for c in 'abcdef0123456789'},
    'q196': {c: 'q197' for c in 'abcdef0123456789'},
    'q197': {c: 'q198' for c in 'abcdef0123456789'},
    'q198': {c: 'q199' for c in 'abcdef0123456789'},
    'q199': {}
    
}



# Clase AFD para procesar cadenas
class AFD:
    def __init__(self, estados, transiciones, estado_inicial, estados_aceptacion):
        self.estados = estados
        self.transiciones = transiciones
        self.estado_actual = estado_inicial
        self.estados_aceptacion = estados_aceptacion
    
    def procesar_cadena(self, cadena, fila):
        ocurrencias = []
        for i in range(len(cadena)):
            self.reiniciar()  # Reiniciar el autómata para cada nueva posición
            for simbolo in cadena[i:]:  # Procesar desde la posición actual
                if simbolo in self.transiciones[self.estado_actual]:
                    self.estado_actual = self.transiciones[self.estado_actual][simbolo]
                else:
                    break  # Salir del bucle si no hay transición válida

            # Verificar si al finalizar la cadena, estamos en un estado de aceptación
            if self.estado_actual in self.estados_aceptacion:
                ocurrencias.append((fila, i, cadena[i:]))  # Fila, columna/posición y texto de la ocurrencia

        return ocurrencias

    def reiniciar(self):
        self.estado_actual = 'q0'  # Reiniciar al estado inicial


# Función para leer diferentes tipos de archivos
def leer_archivo(archivo):
    if archivo.endswith('.csv'):
        # Leer archivo CSV
        df = pd.read_csv(archivo)
        return df.to_string(index=False).splitlines()  # Convertir DataFrame a lista de líneas de texto
    
    elif archivo.endswith('.xlsx'):
        # Leer archivo Excel
        df = pd.read_excel(archivo)
        return df.to_string(index=False).splitlines()  # Convertir DataFrame a lista de líneas de texto
    
    elif archivo.endswith('.docx'):
        # Leer archivo DOCX
        doc = Document(archivo)
        return [p.text for p in doc.paragraphs if p.text.strip()]  # Extraer solo líneas con texto
    
    elif archivo.endswith('.html'):
        # Leer archivo HTML
        with open(archivo, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            return soup.get_text(separator='\n\n').splitlines()

        
    elif archivo.endswith('.txt'):
        # Leer archivo TXT
        with open(archivo, 'r', encoding='utf-8') as file:
            return file.readlines()  # Leer todas las líneas del archivo .txt 

    else:
        raise ValueError("Formato de archivo no soportado.")


# Función principal para buscar ocurrencias
def buscar_ocurrencias(archivo):
    # Leer el archivo con los patrones de texto
    cadenas = leer_archivo(archivo)
    
    ocurrencias = []

    # Procesar cada cadena con el autómata
    for fila, cadena in enumerate(cadenas):
        cadena = cadena.strip()  # Eliminar espacios en blanco y saltos de línea
        resultados = afd.procesar_cadena(cadena, fila)
        ocurrencias.extend(resultados)

    return ocurrencias


# Función para exportar resultados a CSV
def exportar_ocurrencias_a_csv(ocurrencias, archivo_salida):
    with open(archivo_salida, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Fila', 'Posición', 'Texto'])

        for ocurrencia in ocurrencias:
            writer.writerow(ocurrencia)


# Definir los estados de aceptación
estados_aceptacion = ['q13', 'q199', 'q129']  # Ajustar según corresponda

# Crear una instancia del autómata (recuerda definir el diccionario de transiciones `diccionario`)
afd = AFD(
    estados=states, 
    transiciones=diccionario, 
    estado_inicial='q0', 
    estados_aceptacion=estados_aceptacion
)


# Funciones de la interfaz GUI
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        filetypes=[
            ("Todos los archivos soportados", "*.csv *.xlsx *.docx *.html *.txt"),
            ("CSV Files", "*.csv"),
            ("Excel Files", "*.xlsx"),
            ("Word Files", "*.docx"),
            ("HTML Files", "*.html"),
            ("Text Files", "*.txt")
        ]
    )
    if archivo:
        entrada_archivo.set(archivo)

def procesar_archivo():
    archivo_entrada = entrada_archivo.get()
    if not archivo_entrada or not os.path.isfile(archivo_entrada):
        messagebox.showerror("Error", "Selecciona un archivo válido.")
        return

    try:
        ocurrencias = buscar_ocurrencias(archivo_entrada)
        mostrar_ocurrencias(ocurrencias)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def mostrar_ocurrencias(ocurrencias):
    # Limpiar el cuadro de texto
    text_area.delete(1.0, tk.END)
    
    # Mostrar cada ocurrencia encontrada
    if ocurrencias:
        for ocurrencia in ocurrencias:
            text_area.insert(tk.END, f"Fila: {ocurrencia[0]}, Posición: {ocurrencia[1]}, Texto: {ocurrencia[2]}\n")
    else:
        text_area.insert(tk.END, "No se encontraron coincidencias.")

def guardar_reporte():
    archivo_salida = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if archivo_salida:
        ocurrencias = text_area.get(1.0, tk.END).strip().splitlines()
        ocurrencias_procesadas = [tuple(line.split(", ")) for line in ocurrencias if line]
        try:
            exportar_ocurrencias_a_csv(ocurrencias_procesadas, archivo_salida)
            messagebox.showinfo("Éxito", f"Ocurrencias exportadas a '{archivo_salida}'")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")

# Crear ventana principal
root = tk.Tk()
root.title("Validador de ARN")

# Variables para la GUI
entrada_archivo = tk.StringVar()

# Elementos de la GUI
label_instruccion = tk.Label(root, text="Selecciona el archivo a procesar:")
label_instruccion.grid(row=0, column=0, padx=10, pady=10)

entry_archivo = tk.Entry(root, textvariable=entrada_archivo, width=50)
entry_archivo.grid(row=0, column=1, padx=10, pady=10)

boton_seleccionar = tk.Button(root, text="Seleccionar", command=seleccionar_archivo)
boton_seleccionar.grid(row=0, column=2, padx=10, pady=10)

boton_procesar = tk.Button(root, text="Procesar Archivo", command=procesar_archivo)
boton_procesar.grid(row=1, column=1, padx=10, pady=10)

# Cuadro de texto para mostrar las ocurrencias
text_area = scrolledtext.ScrolledText(root, width=80, height=20)
text_area.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Botón para guardar el reporte opcionalmente
boton_guardar = tk.Button(root, text="Guardar Reporte", command=guardar_reporte)
boton_guardar.grid(row=3, column=1, padx=10, pady=20)

# Iniciar la GUI
root.mainloop()