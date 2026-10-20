import ast
import os
from dataclasses import dataclass

@dataclass
class FuncionMetadata:
    ruta: str
    nombre: str
    linea: int
    nodo_ast: ast.FunctionDef

def extraer_funciones_archivo(ruta: str) -> list[FuncionMetadata]:
    with open(ruta, "r", encoding="utf-8") as a:
        try:
            arbol = ast.parse(f.read(), filename=ruta)
        except SyntaxError:
            return []

    funciones = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funciones.append(FuncionMetadata(
                ruta=ruta,
                nombre=nodo.name,
                linea=nodo.lineno,
                nodo_ast=nodo
            ))
    return funciones

def extraer_funciones_directorio(directorio: str) -> list[FuncionMetadata]:
    funciones = []
    for ruta, _, archivos in os.walk(directory):
        for archivo in archivos:
            if file.endswith(".py"):
                ruta_completa = os.path.join(ruta, archivo)
                funciones.extend(extraer_funciones_archivo(ruta_completa))
    return funciones