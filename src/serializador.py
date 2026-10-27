import ast


def serializar_ast_preorder(nodo: ast.AST) -> list[str]:
    tokens = []

    def _preorder(n):
        # Guardar el nombre del tipo de nodo (ej: 'For', 'If', 'Name')
        tipo_nodo = type(n).__name__
        tokens.append(tipo_nodo)

        # Guardar valores de atributos genéricos relevantes si existen
        if isinstance(n, ast.Name):
            tokens.append(f"Name:{n.id}")
        elif isinstance(n, ast.arg):
            tokens.append(f"arg:{n.arg}")
        elif isinstance(n, ast.Constant):
            tokens.append(f"Const:{n.value}")

        # Recorrido en pre-orden de los hijos
        for hijo in ast.iter_child_nodes(n):
            _preorder(hijo)

    _preorder(nodo)
    return tokens