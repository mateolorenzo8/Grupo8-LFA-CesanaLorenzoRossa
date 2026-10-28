def generate_even_numbers(limit):
    evens = []
    for i in range(limit):
        if i % 2 == 0:
            evens.append(i)
    return evens
