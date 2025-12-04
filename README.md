# Practica-2-automatas

# Analizador Léxico en Python

## 1. Objetivo del Proyecto

El objetivo de este proyecto es simular la primera fase de un compilador, conocida como **análisis léxico**, aplicada al idioma español. El programa implementa un Scanner (analizador léxico) capaz de:

- Separar un texto en unidades léxicas (tokens)
- Validar palabras contra un diccionario de las 1000 palabras más frecuentes en español
- Clasificar signos de puntuación
- Detectar números
- Marcar palabras no encontradas como errores ortográficos

## 2. ¿Cómo Funciona?

### 2.1 Flujo General del Programa

El programa ejecuta estos pasos en orden:

1. **Carga del diccionario** → Lee el archivo CSV con las 1000 palabras más frecuentes
2. **Lectura del texto** → Abre el archivo de entrada
3. **Tokenización** → Separa el texto en tokens individuales
4. **Clasificación** → Asigna un tipo a cada token
5. **Generación de salida** → Guarda los resultados en un archivo

### 2.2 Componentes Principales

#### A. Expresiones Regulares
```python
ER_PALABRA_BASICA = r'^[a-záéíóúüñ]+$'      # Solo letras españolas
ER_PUNTUACION = r'^[\.,;:\?\!¡¿]$'          # Signos de puntuación
ER_DIGITO = r'^\d+$'                         # Números
```

#### B. Función `cargar_diccionario()`
- Lee el archivo CSV `las-mil-palabras-mas-frecuentes.csv`
- Extrae todas las palabras válidas del diccionario español
- Ignora números y columnas irrelevantes
- Retorna un conjunto (`set`) con ~1000 palabras para búsquedas rápidas

#### C. Función `tokenizar()`
- Recibe el texto completo
- Usa la expresión regular para extraer:
  - Palabras (secuencias de letras españolas)
  - Signos de puntuación
  - Números
- Convierte todo a minúsculas
- Retorna una lista de tokens

#### D. Función `analizar_texto()`
Para cada token, aplica esta lógica de clasificación:

```
¿Es un número?
  → Clasificar como "DIGITO"
  
¿Está en el diccionario?
  → Clasificar como "PALABRA_VALIDA_ESPANOL"
  
¿Es un signo de puntuación?
  → Clasificar como "PUNTUACION"
  
Si no cumple ninguno:
  → Clasificar como "ERROR_ORTOGRAFICO"
```

#### E. Función `guardar_salida()`
- Escribe cada token con su clasificación
- Formato: `TIPO_TOKEN    lexema`

## 3. Ejemplo de Ejecución

### Entrada ([texto_entrada.txt](texto_entrada.txt)):
```
el gobierno dijo que la situación estaba bajo control.
```

### Proceso:
| Token | ¿Número? | ¿En diccionario? | ¿Puntuación? | Clasificación |
|-------|----------|-----------------|--------------|----------------|
| el | No | ✓ Sí | No | PALABRA_VALIDA_ESPANOL |
| gobierno | No | ✓ Sí | No | PALABRA_VALIDA_ESPANOL |
| dijo | No | ✓ Sí | No | PALABRA_VALIDA_ESPANOL |
| . | No | No | ✓ Sí | PUNTUACION |

### Salida ([tokens_salida.txt](tokens_salida.txt)):
```
PALABRA_VALIDA_ESPANOL	el
PALABRA_VALIDA_ESPANOL	gobierno
PALABRA_VALIDA_ESPANOL	dijo
PUNTUACION	.
```

## 4. Archivos del Proyecto

| Archivo | Descripción |
|---------|-------------|
| [analizador_lexico.py](analizador_lexico.py) | Script principal con toda la lógica |
| [las-mil-palabras-mas-frecuentes.csv](las-mil-palabras-mas-frecuentes.csv) | Diccionario de referencia |
| [texto_entrada.txt](texto_entrada.txt) | Texto a analizar (entrada) |
| [tokens_salida.txt](tokens_salida.txt) | Resultado del análisis (salida) |

## 5. Funcionalidades

✅ **Analizador Léxico**: Separa texto en tokens  
✅ **Validación de Palabras**: Verifica contra diccionario  
✅ **Reconocedor de Puntuación**: Identifica signos ortográficos  
✅ **Detector de Números**: Clasifica dígitos  
✅ **Detección de Errores**: Marca palabras no encontradas  

## 6. Tecnologías Utilizadas

- **Lenguaje**: Python 3.6+
- **Librerías**: `re` (expresiones regulares), `csv` (lectura de archivos)
- **Archivos**: Texto plano (.txt) y CSV

## 7. Cómo Usar

1. Coloca tu texto en `texto_entrada.txt`
2. Ejecuta el script:
   ```bash
   python analizador_lexico.py
   ```
3. Los resultados aparecerán en `tokens_salida.txt`

## 8. Resultados Esperados

El programa genera un archivo con líneas en formato:
```
TIPO_TOKEN    lexema
```

Donde `TIPO_TOKEN` puede ser:
- `PALABRA_VALIDA_ESPANOL` → Palabra en el diccionario
- `PUNTUACION` → Signo de puntuación
- `DIGITO` → Número
- `ERROR_ORTOGRAFICO` → Palabra no reconocida

## 9. Complejidad y Características

- **Tiempo**: O(n) donde n = número de tokens
- **Espacio**: O(m) donde m = palabras en diccionario (~1000)
- **Búsqueda**: O(1) gracias al uso de `set()`
- **Soporte**: Acentos y caracteres españoles (á, é, í, ó, ú, ü, ñ)




