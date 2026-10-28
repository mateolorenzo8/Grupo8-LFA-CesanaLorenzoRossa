def promedio(valores):
    if not valores:
        return 0
    return sum(valores) / len(valores)

def maximo(valores):
    if not valores: return None
    valor_maximo = valores[0]
    for valor in valores[1:]:
        if valor > valor_maximo:
            valor_maximo = valor
    return valor_maximo
