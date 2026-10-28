import argparse
from src.extractor import extraer_funciones_de_dir, extraer_funciones_de_archivo
from src.normalizer import normalizar_ast_funcion
from src.serializer import serializar_ast_preorden
from src.similarity import similitud_jaccard_ngramas, similitud_levenshtein_normalizada

UMBRAL_SIMILITUD = 0.70  # Umbral documentado (70%)

def main():
    parser = argparse.ArgumentParser(description="Motor de búsqueda de funciones similares vía AST")
    parser.add_argument("--dir", required=True, help="Directorio objetivo para indexar")
    parser.add_argument("--funcion", required=True, help="Formato archivo.py:nombre_funcion")
    parser.add_argument("--top", type=int, default=5, help="Top-K resultados")
    parser.add_argument("--metrica", choices=["jaccard", "levenshtein"], default="jaccard")

    argumentos = parser.parse_args()

    # 1. Cargar corpus
    todas_las_funciones = extraer_funciones_de_dir(argumentos.dir)
    if not todas_las_funciones:
        print("No se encontraron funciones en el directorio especificado.")
        return

    # 2. Obtener función objetivo
    archivo_objetivo, nombre_objetivo = argumentos.funcion.split(":")
    funciones_objetivo = extraer_funciones_de_archivo(archivo_objetivo)
    meta_objetivo = next((f for f in funciones_objetivo if f.name == nombre_objetivo), None)

    if not meta_objetivo:
        print(f"No se encontró la función '{nombre_objetivo}' en '{archivo_objetivo}'.")
        return

    # 3. Serializar función objetivo
    objetivo_normalizado = normalizar_ast_funcion(meta_objetivo.ast_node)
    tokens_objetivo = serializar_ast_preorden(objetivo_normalizado)

    resultados = []
    for meta in todas_las_funciones:
        # Opcional: ignorar exactamente el mismo puntero/ubicación si no se quiere auto-comparar
        if meta.file_path == meta_objetivo.file_path and meta.name == meta_objetivo.name and meta.line_number == meta_objetivo.line_number:
            continue

        meta_normalizada = normalizar_ast_funcion(meta.ast_node)
        tokens = serializar_ast_preorden(meta_normalizada)

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
        print(f"Puntaje: {puntaje:.4f}{es_candidata} -> {meta.file_path}:{meta.name} (Línea {meta.line_number})")

if __name__ == "__main__":
    main()