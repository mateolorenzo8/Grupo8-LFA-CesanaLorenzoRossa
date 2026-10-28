import argparse
import os
from src.extractor import extraer_funciones_directorio, extraer_funciones_archivo
from src.normalizador import normalizar_funcion_ast
from src.serializador import serializar_ast_preorder
from src.similitud import similitud_jaccard_ngramas, similitud_levenshtein_normalizada

UMBRAL_SIMILITUD = 0.70  # Umbral documentado (70%)

def main():
    parser = argparse.ArgumentParser(description="Motor de búsqueda de funciones similares vía AST")
    parser.add_argument("--dir", required=True, help="Directorio objetivo para indexar")
    parser.add_argument("--funcion", required=True, help="Formato archivo.py:nombre_funcion")
    parser.add_argument("--top", type=int, default=5, help="Top-K resultados")
    parser.add_argument("--metrica", choices=["jaccard", "levenshtein"], default="jaccard")

    argumentos = parser.parse_args()

    # 1. Cargar corpus
    todas_las_funciones = extraer_funciones_directorio(argumentos.dir)
    if not todas_las_funciones:
        print("No se encontraron funciones en el directorio especificado.")
        return

    # 2. Obtener función objetivo
    archivo_objetivo, nombre_objetivo = argumentos.funcion.split(":")
    archivo_objetivo = os.path.normpath(archivo_objetivo)
    funciones_objetivo = extraer_funciones_archivo(archivo_objetivo)
    meta_objetivo = next((f for f in funciones_objetivo if f.nombre == nombre_objetivo), None)

    if not meta_objetivo:
        print(f"No se encontró la función '{nombre_objetivo}' en '{archivo_objetivo}'.")
        return

    # 3. Serializar función objetivo
    objetivo_normalizado = normalizar_funcion_ast(meta_objetivo.nodo_ast)
    tokens_objetivo = serializar_ast_preorder(objetivo_normalizado)

    resultados = []
    for meta in todas_las_funciones:
        # Ignorar la misma función objetivo en el mismo archivo y línea
        if (os.path.normpath(meta.ruta) == os.path.normpath(meta_objetivo.ruta)
                and meta.nombre == meta_objetivo.nombre
                and meta.linea == meta_objetivo.linea):
            continue

        meta_normalizada = normalizar_funcion_ast(meta.nodo_ast)
        tokens = serializar_ast_preorder(meta_normalizada)

        if argumentos.metrica == "jaccard":
            puntaje = similitud_jaccard_ngramas(tokens_objetivo, tokens, n=3)
        else:
            puntaje = similitud_levenshtein_normalizada(tokens_objetivo, tokens)

        resultados.append((puntaje, meta))

    # 4. Ordenar y filtrar
    resultados.sort(key=lambda x: x[0], reverse=True)

    print(f"\n--- Búsqueda de duplicados para '{nombre_objetivo}' ({argumentos.metrica.upper()}) ---")
    for puntaje, meta in resultados[:argumentos.top]:
        es_candidata = " [Candidata a duplicado]" if puntaje >= UMBRAL_SIMILITUD else ""
        print(f"Puntaje: {puntaje:.4f}{es_candidata} -> {meta.ruta}:{meta.nombre} (Línea {meta.linea})")

if __name__ == "__main__":
    main()
