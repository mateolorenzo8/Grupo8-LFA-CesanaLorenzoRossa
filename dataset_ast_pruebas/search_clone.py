def busqueda_binaria(arreglo, objetivo):
    inicio = 0
    fin = len(arreglo) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if arreglo[medio] == objetivo:
            return medio
        elif arreglo[medio] < objetivo:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1
