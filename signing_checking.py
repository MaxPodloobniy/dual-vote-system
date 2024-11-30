import hashlib
import random


def generate_prime(min_val, max_val):
    """Генерація простого числа в діапазоні."""

    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    primes = [p for p in range(min_val, max_val) if is_prime(p)]
    return primes[0] if primes else None


def generate_dsa_keys():
    """Генерація ключів DSA."""
    # Фіксовані параметри для навчальних цілей
    p = 23  # Просте число
    q = 11  # Інше просте число
    g = 4  # Генератор

    # Закритий ключ
    x = random.randint(1, q - 1)

    # Відкритий ключ
    y = pow(g, x, p)

    return {
        'public_key': (p, q, g, y),
        'private_key': x
    }


def sign_message(message, private_key, public_key):
    """Підпис повідомлення."""
    p, q, g, y = public_key
    x = private_key

    # Хешування повідомлення
    h = int(hashlib.sha1(message.encode()).hexdigest(), 16)

    # Генерація k
    k = random.randint(1, q - 1)

    # Обчислення r
    r = pow(g, k, p) % q

    # Обчислення s
    s = (pow(k, -1, q) * (h + x * r)) % q

    return (r, s)


def verify_signature(message, signature, public_key):
    """Перевірка підпису."""
    p, q, g, y = public_key
    r, s = signature

    # Хешування повідомлення
    h = int(hashlib.sha1(message.encode()).hexdigest(), 16)

    # Перевірка підпису
    w = pow(s, -1, q)
    u1 = (h * w) % q
    u2 = (r * w) % q
    v = (pow(g, u1, p) * pow(y, u2, p)) % p % q

    return v == r


def test_dsa():
    """Тестування алгоритму DSA."""
    # Генерація ключів
    keys = generate_dsa_keys()
    public_key = keys['public_key']
    private_key = keys['private_key']

    # Тестове повідомлення
    message = "Привіт, світ!"

    # Підпис повідомлення
    signature = sign_message(message, private_key, public_key)
    print(f"Підпис: {signature}")

    # Перевірка підпису
    is_valid = verify_signature(message, signature, public_key)
    print(f"Підпис валідний: {is_valid}")

    # Перевірка з модифікованим повідомленням
    modified_message = message + " (змінено)"
    is_valid_modified = verify_signature(modified_message, signature, public_key)
    print(f"Підпис для зміненого повідомлення: {is_valid_modified}")

    # Перевірка тесту
    assert is_valid, "Помилка перевірки підпису"
    assert not is_valid_modified, "Помилка: підпис прийнято для зміненого повідомлення"

    print("Тест пройшов успішно!")


'''# Запуск тесту
if __name__ == "__main__":
    test_dsa()'''