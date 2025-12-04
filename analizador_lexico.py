import re
import csv
from tkinter import Tk, Frame, Label, Button
from tkinter import ttk

# ============================
# EXPRESIONES REGULARES
# ============================

ER_PALABRA_BASICA = re.compile(r'^[a-záéíóúüñ]+$')
ER_PUNTUACION = re.compile(r'^[\.,;:\?\!¡¿]$')
ER_DIGITO = re.compile(r'^\d+$')


# ============================
# CARGA DEL DICCIONARIO
# ============================

def cargar_diccionario(ruta_csv):
    diccionario = set()

    with open(ruta_csv, encoding="utf-8") as f:
        lector = csv.reader(f)
        next(lector, None)

        for fila in lector:
            for celda in fila:
                if not celda:
                    continue

                palabra = celda.strip().lower()

                if palabra.isdigit():
                    continue

                if ER_PALABRA_BASICA.match(palabra):
                    diccionario.add(palabra)

    return diccionario


# ============================
# CARGAR TEXTO DE ENTRADA
# ============================

def cargar_texto(ruta_txt):
    """Lee el archivo de texto de entrada"""
    with open(ruta_txt, encoding="utf-8") as f:
        return f.read()


# ============================
# TOKENIZACIÓN
# ============================

def tokenizar(texto):
    return re.findall(r"[a-záéíóúüñ]+|[\.,;:\?\!¡¿]|\d+", texto.lower())


# ============================
# ANALIZADOR LÉXICO
# ============================

def analizar_texto(texto, diccionario):
    tokens = tokenizar(texto)
    salida = []

    for lexema in tokens:

        # 1. Detectar número
        if ER_DIGITO.match(lexema):
            salida.append(("DIGITO", lexema))
            continue

        # 2. Verificar diccionario
        if lexema in diccionario:
            salida.append(("PALABRA_VALIDA_ESPANOL", lexema))
            continue

        # 3. Detectar puntuación
        if ER_PUNTUACION.match(lexema):
            salida.append(("PUNTUACION", lexema))
            continue

        # 4. Todo lo demás → Error ortográfico
        salida.append(("ERROR_ORTOGRAFICO", lexema))

    return salida


# ============================
# GUARDAR RESULTADOS
# ============================

def guardar_salida(tokens, ruta="tokens_salida.txt"):
    with open(ruta, "w", encoding="utf-8") as f:
        for tipo, lexema in tokens:
            f.write(f"{tipo}\t{lexema}\n")


# ============================
# INTERFAZ GRÁFICA MEJORADA
# ============================

def mostrar_interfaz_gui(tokens_clasificados):
    """Muestra los tokens en una ventana gráfica con tabla estilo salida esperada"""
    ventana = Tk()
    ventana.title("Salida Esperada (Formato: [Tipo de Token, Lexema])")
    ventana.geometry("750x700")
    ventana.resizable(True, True)
    ventana.configure(bg="white")
    
    # ====== TÍTULO ======
    frame_titulo = Frame(ventana, bg="white", pady=15)
    frame_titulo.pack(fill="x")
    
    titulo = Label(frame_titulo, 
                   text="Salida Esperada (Formato: [Tipo de Token, Lexema])", 
                   font=("Arial", 13, "bold"), 
                   bg="white",
                   fg="#333333")
    titulo.pack()
    
    # ====== TABLA ======
    frame_tabla = Frame(ventana, bg="white")
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Crear Treeview con estilo
    columnas = ("Token", "Lexema")
    tabla = ttk.Treeview(frame_tabla, 
                         columns=columnas, 
                         height=28, 
                         show="headings",
                         style="Custom.Treeview")
    
    # Definir ancho de columnas
    tabla.column("Token", width=350, anchor="w")
    tabla.column("Lexema", width=350, anchor="w")
    
    # Encabezados
    tabla.heading("Token", text="Token")
    tabla.heading("Lexema", text="Lexema")
    
    # Agregar datos a la tabla
    for idx, (tipo_token, lexema) in enumerate(tokens_clasificados):
        # Alternar colores de filas para mejor visualización
        tag = "oddrow" if idx % 2 == 0 else "evenrow"
        tabla.insert("", "end", values=(tipo_token, lexema), tags=(tag,))
    
    # ====== ESTILOS PERSONALIZADOS ======
    estilo = ttk.Style()
    estilo.theme_use('clam')
    
    # Encabezados
    estilo.configure("Custom.Treeview.Heading", 
                    font=("Arial", 11, "bold"), 
                    background="#cccccc",
                    foreground="#000000",
                    padding=10,
                    borderwidth=1,
                    relief="solid")
    
    # Filas
    estilo.configure("Custom.Treeview", 
                    font=("Arial", 10),
                    rowheight=28,
                    fieldbackground="white",
                    borderwidth=1)
    
    # Colores alternados
    estilo.configure("Custom.Treeview", 
                    background="white",
                    foreground="#000000")
    
    tabla.tag_configure("oddrow", background="#ffffff")
    tabla.tag_configure("evenrow", background="#f5f5f5")
    
    # Bordes
    tabla.pack(side="left", fill="both", expand=True, pady=5)
    
    # ====== SCROLLBAR ======
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y", padx=(5, 0))
    
    # ====== INFORMACIÓN ======
    frame_info = Frame(ventana, bg="#f0f0f0", pady=8)
    frame_info.pack(fill="x", padx=20)
    
    info_text = Label(frame_info, 
                     text=f"Total de tokens procesados: {len(tokens_clasificados)}", 
                     font=("Arial", 9),
                     bg="#f0f0f0",
                     fg="#666666")
    info_text.pack()
    
    # ====== BOTONES ======
    frame_botones = Frame(ventana, bg="white", pady=15)
    frame_botones.pack(fill="x")
    
    def guardar_tabla():
        """Guarda la tabla en el archivo de salida"""
        guardar_salida(tokens_clasificados)
        # Cambiar texto del botón temporalmente
        boton_guardar.config(state="disabled")
        boton_guardar.config(text="✓ Guardado")
        ventana.after(2000, lambda: boton_guardar.config(state="normal", text="Guardar Salida"))
    
    boton_guardar = Button(frame_botones, 
                          text="Guardar Salida", 
                          command=guardar_tabla, 
                          bg="#4CAF50", 
                          fg="white", 
                          padx=25, 
                          pady=10, 
                          font=("Arial", 10, "bold"),
                          relief="flat",
                          cursor="hand2",
                          activebackground="#45a049",
                          activeforeground="white")
    boton_guardar.pack(side="left", padx=10)
    
    boton_cerrar = Button(frame_botones, 
                         text="Cerrar", 
                         command=ventana.quit, 
                         bg="#f44336", 
                         fg="white", 
                         padx=25, 
                         pady=10, 
                         font=("Arial", 10, "bold"),
                         relief="flat",
                         cursor="hand2",
                         activebackground="#da190b",
                         activeforeground="white")
    boton_cerrar.pack(side="left", padx=10)
    
    ventana.mainloop()


# ============================
# PROGRAMA PRINCIPAL
# ============================

if __name__ == "__main__":
    diccionario = cargar_diccionario("las-mil-palabras-mas-frecuentes.csv")
    texto = cargar_texto("texto_entrada.txt")
    tokens_clasificados = analizar_texto(texto, diccionario)
    
    # Mostrar interfaz gráfica con los resultados
    mostrar_interfaz_gui(tokens_clasificados)
