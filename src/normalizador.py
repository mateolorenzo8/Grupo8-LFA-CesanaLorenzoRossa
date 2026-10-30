import ast
import copy


class ASTNormalizer(ast.NodeTransformer):
    def __init__(self):
        self.var_mapa = {}
        self.var_contador = 1

    # Nombres definidos por la lib
    def _get_var_token(self, nombre: str) -> str:
        if nombre not in self.var_mapa:
            self.var_mapa[nombre] = f"VAR{self.var_contador}"
            self.var_contador += 1
        return self.var_mapa[nombre]

    def visit_Name(self, nodo: ast.Name):
        nuevo_id = self._get_var_token(nodo.id)
        return ast.copy_location(ast.Name(id=nuevo_id, ctx=nodo.ctx), nodo)

    def visit_arg(self, nodo: ast.arg):
        nuevo_arg = self._get_var_token(nodo.arg)
        return ast.copy_location(ast.arg(arg=nuevo_arg, annotation=None), nodo)

    def visit_Constant(self, nodo: ast.Constant):
        return ast.copy_location(ast.Constant(value="LIT"), nodo)


def normalizar_funcion_ast(nodo_func: ast.FunctionDef) -> ast.FunctionDef:
    # Clonar el nodo para no alterar el AST original
    copia_nodo = copy.deepcopy(nodo_func)

    # Ignorar el nombre de la función para que no influya en la comparación
    copia_nodo.name = "FUNC_ANONIMA"

    normalizador = ASTNormalizer()

    # Determina metodo a usar según el tipo
    # Hicimos como override a metodos de la lib arriba
    ast_normalizado = normalizador.visit(copia_nodo)

    return ast_normalizado