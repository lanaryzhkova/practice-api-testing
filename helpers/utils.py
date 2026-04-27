import random, string


def randomString():
    """Генерирует случайную строку с длиной 10 символов"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))

def randomIntList():
    """Генерирует массив случайных чисел"""
    return [random.randint(1, 100) for _ in range(5)]

def randomInt():
    """Генерирует случайное число"""
    return random.randint(1, 100)