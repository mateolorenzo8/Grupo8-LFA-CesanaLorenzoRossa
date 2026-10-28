def pares(limite_superior):
    lista_pares = []
    for num in range(limite_superior):
        if num % 2 == 0:
            lista_pares.append(num)
    return lista_pares
