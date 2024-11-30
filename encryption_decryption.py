import random
import math


def is_prime(n):
    """Перевірка числа на простоту."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def generate_prime(max_val=10000):
    """Генерація випадкового простого числа."""
    while True:
        p = random.randint(2, max_val)
        if is_prime(p):
            return p


def generate_keys():
    """Генерація ключів для системи Аль-Гамаля."""
    p = generate_prime()

    while True:
        g = random.randint(2, p - 1)
        if g < p:
            break

    x = random.randint(2, p - 2)
    y = pow(g, x, p)

    return {
        'public_key': (p, g, y),
        'private_key': x
    }


def string_to_blocks(message, p):
    """Перетворення рядка на блоки числами."""
    blocks = []
    for char in message:
        # Перетворюємо символ на число
        block = ord(char)

        # Перевірка, що блок менше p
        if block >= p:
            raise ValueError(f"Символ {char} перевищує допустиме значення для p={p}")

        blocks.append(block)
    return blocks


def blocks_to_string(blocks):
    """Перетворення блоків назад у рядок."""
    return ''.join(chr(block) for block in blocks)


def encrypt_string(message, public_key):
    """Шифрування рядка."""
    p, g, y = public_key

    # Перетворення рядка на блоки
    blocks = string_to_blocks(message, p)

    # Шифрування кожного блоку
    encrypted_blocks = [encrypt(block, public_key) for block in blocks]

    return encrypted_blocks


def decrypt_string(encrypted_blocks, private_key, p):
    """Розшифрування рядка."""
    # Розшифрування кожного блоку
    decrypted_blocks = [decrypt(block, private_key, p) for block in encrypted_blocks]

    # Перетворення блоків назад у рядок
    return blocks_to_string(decrypted_blocks)


def encrypt(message, public_key):
    """Шифрування повідомлення."""
    p, g, y = public_key

    if message >= p:
        raise ValueError("Повідомлення повинно бути менше за p")

    k = random.randint(2, p - 2)
    a = pow(g, k, p)
    b = (pow(y, k, p) * message) % p

    return (a, b)


def decrypt(crypto_text, private_key, p):
    """Розшифрування повідомлення."""
    a, b = crypto_text
    x = private_key

    def mod_inverse(a, m):
        def egcd(a, b):
            if a == 0:
                return (b, 0, 1)
            else:
                g, y, x = egcd(b % a, a)
                return (g, x - (b // a) * y, y)

        g, x, _ = egcd(a, m)
        if g != 1:
            raise Exception('Модульне обернене не існує')
        else:
            return x % m

    ax_mod_p = pow(a, x, p)
    ax_inverse = mod_inverse(ax_mod_p, p)
    decrypted_message = (b * ax_inverse) % p

    return decrypted_message


def test_al_gamal_string_encryption():
    """Тестування системи шифрування рядків."""
    # Генеруємо ключі
    keys = generate_keys()
    public_key = keys['public_key']
    private_key = keys['private_key']
    p = public_key[0]

    # Оригінальне повідомлення
    original_message = "Hello, світ!"
    print(f"Оригінальне повідомлення: {original_message}")

    # Шифрування
    encrypted_blocks = encrypt_string(original_message, public_key)
    print(f"Зашифровані блоки: {encrypted_blocks}")

    # Розшифрування
    decrypted_message = decrypt_string(encrypted_blocks, private_key, p)
    print(f"Розшифроване повідомлення: {decrypted_message}")

    # Перевірка
    assert original_message == decrypted_message, "Помилка шифрування/розшифрування"
    print("Шифрування та розшифрування рядка пройшло успішно!")


# Запуск тесту
'''if __name__ == "__main__":
    test_al_gamal_string_encryption()'''