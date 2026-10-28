# Clon de factorial y fibonacci
def calcular_factorial(x):
    if x == 0: return 1
    return x * calcular_factorial(x-1)

def calcular_fib(numero):
    if numero <= 1: return numero
    return calcular_fib(numero-1) + calcular_fib(numero-2)
