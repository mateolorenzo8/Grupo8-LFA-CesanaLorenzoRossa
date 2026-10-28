def ordenar_burbuja(lista):
    tamanio = len(lista)
    for idx1 in range(tamanio):
        for idx2 in range(0, tamanio - idx1 - 1):
            if lista[idx2] > lista[idx2+1]:
                lista[idx2], lista[idx2+1] = lista[idx2+1], lista[idx2]
    return lista
