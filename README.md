# Detector de Clones y Similitud de Código (AST)

Herramienta para la detección de similitud estructural y clonación de funciones en Python mediante el análisis del Árbol de Sintaxis Abstracta (AST), serialización en pre-orden y métricas de distancia (Jaccard sobre n-gramas y Levenshtein normalizado).

Proyecto desarrollado para la cátedra de **Lenguajes Formales y Autómatas** (Grupo 8 - Cesana, Lorenzo, Rossa).

---

## Estructura del Proyecto

```text
.
├── main.py               # Punto de entrada / Interfaz de línea de comandos (CLI)
├── src/
│   ├── extractor.py      # Extracción y parseo de funciones desde archivos y directorios
│   ├── normalizador.py   # Normalización del AST (anonimización de nombres y literales)
│   ├── serializador.py   # Recorrido en pre-orden y tokenización estructural del AST
│   └── similitud.py      # Métricas de cálculo de similitud (Jaccard y Levenshtein)
└── tests/
    └── test_detector.py  # Pruebas unitarias para casos positivos y negativos de clones
```

---

## Flujo de Trabajo

1. **Extracción:** Se recorre el directorio objetivo y se aíslan los nodos de funciones (`ast.FunctionDef`).
2. **Normalización:** Se abstraen nombres de variables locales, parámetros y literales (`VAR1`, `VAR2`, `LIT`, etc.) para enfocarse puramente en la lógica y estructura sintáctica.
3. **Serialización:** Se realiza un recorrido pre-orden del árbol normalizado, convirtiéndolo en una secuencia de tokens.
4. **Comparación:** Se contrastan las secuencias mediante coeficientes de similitud:
   - **Jaccard ($n$-gramas):** Robusto ante reordenamiento de sentencias independientes.
   - **Levenshtein Normalizado:** Sensible al orden secuencial estricto de las operaciones.

---

## Uso desde la Terminal

El script principal `main.py` permite buscar duplicados o funciones estructuralmente similares dentro de un directorio a partir de una función de referencia.

### Sintaxis

```bash
python main.py --dir <directorio> --funcion <archivo.py:nombre_funcion> [--metrica {jaccard,levenshtein}] [--top <k>]
```

### Parámetros

| Parámetro | Requerido | Por defecto | Descripción |
|---|:---:|:---:|---|
| `--dir` | **Sí** | - | Directorio base que contiene el código a indexar y analizar. |
| `--funcion` | **Sí** | - | Función objetivo en formato `ruta/al/archivo.py:nombre_funcion`. |
| `--metrica` | No | `jaccard` | Métrica de similitud a emplear (`jaccard` o `levenshtein`). |
| `--top` | No | `5` | Cantidad máxima de resultados a mostrar en el ranking. |

### Ejemplos de Invocación

**1. Búsqueda con métrica de Jaccard (por defecto):**
```bash
python main.py --dir ./src --funcion src/extractor.py:extraer_funciones_archivo
```

**2. Búsqueda con distancia de Levenshtein y top 3 resultados:**
```bash
python main.py --dir ./src --funcion src/extractor.py:extraer_funciones_archivo --metrica levenshtein --top 3
```

