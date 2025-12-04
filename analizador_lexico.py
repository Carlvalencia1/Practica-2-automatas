import re
import csv

# ============================
# EXPRESIONES REGULARES
# ============================

ER_PALABRA_BASICA = re.compile(r'^[a-záéíóúüñ]+$')
ER_PUNTUACION = re.compile(r'^[\.,;:\?\!¡¿]$')
ER_DIGITO = re.compile(r'^\d+$')


# ============================
# CARGA DEL DICCIONARIO
# ============================
# Esta función está optimizada para tu CSV específicamente.
# Lee TODAS las columnas, descarta números y extrae palabras reales.

def cargar_diccionario(ruta_csv):
    diccionario = set()

    with open(ruta_csv, encoding="utf-8") as f:
        lector = csv.reader(f)

        # Saltar fila de encabezados
        next(lector, None)

        for fila in lector:
            for celda in fila:
                if not celda:
                    continue

                palabra = celda.strip().lower()

                # Ignorar números (columna Número)
                if palabra.isdigit():
                    continue

                # Mantener solo palabras del alfabeto español
                if ER_PALABRA_BASICA.match(palabra):
                    diccionario.add(palabra)

    return diccionario


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

def guardar_salida(tokens, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        for tipo, lexema in tokens:
            f.write(f"{tipo}\t{lexema}\n")


# ============================
# PROGRAMA PRINCIPAL
# ============================

if __name__ == "__main__":

    # Rutas según tu estructura REAL
    diccionario_ruta = "las-mil-palabras-mas-frecuentes.csv"
    entrada_ruta = "texto_entrada.txt"
    salida_ruta = "tokens_salida.txt"

    # Cargar diccionario
    dic = cargar_diccionario(diccionario_ruta)

    # Leer texto de entrada
    with open(entrada_ruta, "r", encoding="utf-8") as f:
        texto = f.read()

    # Ejecutar análisis
    resultado = analizar_texto(texto, dic)

    # Guardar archivo de salida
    guardar_salida(resultado, salida_ruta)

    print("✔ Análisis completado correctamente.")
    print(f"✔ Archivo generado: {salida_ruta}")
