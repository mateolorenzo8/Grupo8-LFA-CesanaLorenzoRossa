import ast
import pytest
from src.normalizador import normalizar_funcion_ast
from src.serializador import serializar_ast_preorder
from src.similitud import similitud_jaccard_ngramas, similitud_levenshtein_normalizada

UMBRAL_SIMILITUD = 0.70


def _obtener_tokens_desde_codigo(codigo_fuente: str) -> list[str]:
    """Función auxiliar para parsear, normalizar y serializar código Python."""
    tree = ast.parse(codigo_fuente)
    func_node = tree.body[0]
    assert isinstance(func_node, ast.FunctionDef)
    ast_normalizado = normalizar_funcion_ast(func_node)
    return serializar_ast_preorder(ast_normalizado)


# CASOS POSITIVOS (Funciones estructuralmente clones)

def test_caso_positivo_renombrado_de_variables_y_parametros():
    """
    Caso Positivo 1: Dos funciones con la misma lógica subyacente donde
    solo cambian los nombres de parámetros, variables locales y literales.
    Debe retornar una similitud perfecta o casi perfecta (>= 0.70).
    """
    codigo_original = """
def calcular_promedio(numeros):
    total = 0
    cantidad = len(numeros)
    for n in numeros:
        total += n
    if cantidad > 0:
        return total / cantidad
    return 0
"""

    codigo_clonado = """
def obtener_media(lista_valores):
    acumulador = 0
    longitud = len(lista_valores)
    for x in lista_valores:
        acumulador += x
    if longitud > 0:
        return acumulador / longitud
    return 0
"""

    tokens_1 = _obtener_tokens_desde_codigo(codigo_original)
    tokens_2 = _obtener_tokens_desde_codigo(codigo_clonado)

    score_jaccard = similitud_jaccard_ngramas(tokens_1, tokens_2, n=3)
    score_levenshtein = similitud_levenshtein_normalizada(tokens_1, tokens_2)

    # La normalización convierte variables a VAR1, VAR2... por lo que el AST normalizado es idéntico
    assert score_jaccard >= UMBRAL_SIMILITUD, f"Esperado >= {UMBRAL_SIMILITUD}, obtenido Jaccard: {score_jaccard}"
    assert score_levenshtein >= UMBRAL_SIMILITUD, f"Esperado >= {UMBRAL_SIMILITUD}, obtenido Levenshtein: {score_levenshtein}"


def test_caso_positivo_reordenamiento_de_instrucciones_independientes():
    """
    Caso Positivo 2: Funciones con las mismas instrucciones pero con líneas
    independientes reordenadas. Jaccard sobre n-gramas debe detectar alta similitud.
    """
    codigo_base = """
def procesar_usuario(nombre, edad, email):
    nombre_limpio = nombre.strip().lower()
    edad_valida = edad >= 18
    email_normalizado = email.lower()
    return {"nombre": nombre_limpio, "es_mayor": edad_valida, "email": email_normalizado}
"""

    codigo_reordenado = """
def registrar_usuario(nom, ed, correo):
    correo_norm = correo.lower()
    nom_norm = nom.strip().lower()
    es_adulto = ed >= 18
    return {"nombre": nom_norm, "es_mayor": es_adulto, "email": correo_norm}
"""

    tokens_1 = _obtener_tokens_desde_codigo(codigo_base)
    tokens_2 = _obtener_tokens_desde_codigo(codigo_reordenado)

    score_jaccard = similitud_jaccard_ngramas(tokens_1, tokens_2, n=3)

    assert score_jaccard >= UMBRAL_SIMILITUD, f"Esperado >= {UMBRAL_SIMILITUD}, obtenido Jaccard: {score_jaccard}"


# CASOS NEGATIVOS (Funciones claramente distintas)

def test_caso_negativo_estructuras_de_control_diferentes():
    """
    Caso Negativo 1: Algoritmos con propósitos y estructuras sintácticas completamente distintas
    (bucle acumulador vs. acceso directo a diccionario/condicionales).
    """
    codigo_bucle = """
def sumar_elementos(lista):
    suma = 0
    for elemento in lista:
        suma += elemento
    return suma
"""

    codigo_condicional = """
def obtener_descuento(cliente):
    if cliente.tipo == "VIP":
        return 0.20
    elif cliente.tipo == "FRECUENTE":
        return 0.10
    else:
        return 0.0
"""

    tokens_1 = _obtener_tokens_desde_codigo(codigo_bucle)
    tokens_2 = _obtener_tokens_desde_codigo(codigo_condicional)

    score_jaccard = similitud_jaccard_ngramas(tokens_1, tokens_2, n=3)
    score_levenshtein = similitud_levenshtein_normalizada(tokens_1, tokens_2)

    assert score_jaccard < UMBRAL_SIMILITUD, f"Esperado < {UMBRAL_SIMILITUD}, obtenido Jaccard: {score_jaccard}"
    assert score_levenshtein < UMBRAL_SIMILITUD, f"Esperado < {UMBRAL_SIMILITUD}, obtenido Levenshtein: {score_levenshtein}"


def test_caso_negativo_iterativo_vs_recursivo():
    """
    Caso Negativo 2: Resolución del mismo problema semántico (Factorial) pero con
    estructuras de control totalmente distintas (bucle 'while' vs. recursión con 'if').
    """
    codigo_iterativo = """
def factorial_iterativo(n):
    resultado = 1
    mientras = n
    while mientras > 1:
        resultado *= mientras
        mientras -= 1
    return resultado
"""

    codigo_recursivo = """
def factorial_recursivo(n):
    if n <= 1:
        return 1
    return n * factorial_recursivo(n - 1)
"""

    tokens_1 = _obtener_tokens_desde_codigo(codigo_iterativo)
    tokens_2 = _obtener_tokens_desde_codigo(codigo_recursivo)

    score_jaccard = similitud_jaccard_ngramas(tokens_1, tokens_2, n=3)
    score_levenshtein = similitud_levenshtein_normalizada(tokens_1, tokens_2)

    # El AST difiere drásticamente (nodo While vs nodo If y llamadas recursivas)
    assert score_jaccard < UMBRAL_SIMILITUD, f"Esperado < {UMBRAL_SIMILITUD}, obtenido Jaccard: {score_jaccard}"
    assert score_levenshtein < UMBRAL_SIMILITUD, f"Esperado < {UMBRAL_SIMILITUD}, obtenido Levenshtein: {score_levenshtein}"



def test_caso_negativo_insercion_de_codigo_extenso():
    """
    Prueba de limitación (Caso Negativo / Falso Negativo):
    Una función a la que se le agrega un bloque de código extenso en el medio.
    Aunque la estructura general es similar, la abundancia de nuevos tokens
    hace caer el puntaje por debajo del umbral (< 0.70).
    """
    codigo_base = """
def procesar_datos(lista):
    resultado = []
    for x in lista:
        resultado.append(x * 2)
    return resultado
"""

    codigo_con_bloque_extra = """
def procesar_datos(lista):
    resultado = []

    # Bloque extenso insertado en el medio
    if len(lista) > 10:
        for i in range(len(lista)):
            if i % 2 == 0:
                print("Procesando elemento par:", i)
            else:
                print("Procesando elemento impar:", i)

    for x in lista:
        resultado.append(x * 2)
    return resultado
"""

    tokens_1 = _obtener_tokens_desde_codigo(codigo_base)
    tokens_2 = _obtener_tokens_desde_codigo(codigo_con_bloque_extra)

    score_jaccard = similitud_levenshtein_normalizada(tokens_1, tokens_2)

    assert score_jaccard < UMBRAL_SIMILITUD, f"Esperado < {UMBRAL_SIMILITUD}, obtenido Jaccard: {score_jaccard}"


def test_caso_negativo_reordenamiento_grande_de_bloques():
    """
    Prueba de limitación (Caso Negativo / Falso Negativo - Caso 3):
    Reordenamiento grande de bloques de código.
    Aunque la herramienta tolera pequeños cambios de orden entre líneas cercanas,
    si se cambia de lugar el orden de varios bloques completos (ej: mover estructuras
    de control completas de sitio), la secuencia y la asignación secuencial de
    variables en el AST cambian lo suficiente para que el puntaje de similitud caiga (< 0.70).
    """
    codigo_original = """
def procesar_lote_operaciones(datos, config):
    # Bloque 1: Bucle de filtrado y mapeo
    filtrados = []
    for item in datos:
        if item.activo:
            filtrados.append(item.valor * 2)

    # Bloque 2: Validacion condicional profunda
    if config.modo == 1:
        limite = 100
        factor = 1.5
    else:
        limite = 50
        factor = 1.0

    # Bloque 3: Reduccion / acumulacion con while
    total = 0
    i = 0
    while i < len(filtrados):
        total += filtrados[i] * factor
        i += 1

    return total > limite
"""

    codigo_reordenado = """
def ejecutar_lote_reordenado(entradas, opciones):
    # Bloque 2 movido al inicio
    if opciones.modo == 1:
        tope = 100
        multiplicador = 1.5
    else:
        tope = 50
        multiplicador = 1.0

    # Bloque 3 movido al medio
    acumulado = 0
    indice = 0
    while indice < len(entradas):
        acumulado += entradas[indice] * multiplicador
        indice += 1

    # Bloque 1 movido al final
    depurados = []
    for elem in entradas:
        if elem.activo:
            depurados.append(elem.valor * 2)

    return acumulado > tope
"""

    tokens_1 = _obtener_tokens_desde_codigo(codigo_original)
    tokens_2 = _obtener_tokens_desde_codigo(codigo_reordenado)

    score_jaccard = similitud_jaccard_ngramas(tokens_1, tokens_2, n=3)
    score_levenshtein = similitud_levenshtein_normalizada(tokens_1, tokens_2)

    assert score_jaccard < UMBRAL_SIMILITUD, f"Esperado < {UMBRAL_SIMILITUD}, obtenido Jaccard: {score_jaccard}"
    assert score_levenshtein < UMBRAL_SIMILITUD, f"Esperado < {UMBRAL_SIMILITUD}, obtenido Levenshtein: {score_levenshtein}"
