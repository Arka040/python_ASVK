#!/usr/bin/env python3

import random
import urllib.request
import sys
import argparse


def bullscows(guess: str, secret: str) -> tuple[int, int]:
    if len(guess) != len(secret):
        raise ValueError("Длина догадки должна совпадать с длиной загадки")

    bulls = 0
    cows = 0

    for i in range(len(guess)):
        if guess[i] == secret[i]:
            bulls += 1

    guess_chars = {}
    secret_chars = {}

    for char in guess:
        guess_chars[char] = guess_chars.get(char, 0) + 1

    for char in secret:
        secret_chars[char] = secret_chars.get(char, 0) + 1

    for char in guess_chars:
        if char in secret_chars:
            cows += min(guess_chars[char], secret_chars[char])

    cows -= bulls

    return (bulls, cows)


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    if not words:
        raise ValueError("Список слов пуст")

    secret = random.choice(words)
    attempts = 0

    while True:
        guess = ask("Введите слово: ", words)
        attempts += 1

        bulls, cows = bullscows(guess, secret)

        inform("Быки: {}, Коровы: {}", bulls, cows)

        if bulls == len(secret):
            return attempts


def load_dictionary(source: str, word_length: int = 5) -> list[str]:
    if source.startswith(('http://', 'https://')):
        with urllib.request.urlopen(source) as response:
            content = response.read().decode('utf-8')
            words = content.splitlines()
    else:
        try:
            with open(source, 'r', encoding='utf-8') as file:
                words = file.read().splitlines()
        except UnicodeDecodeError:
            with open(source, 'r', encoding='latin-1') as file:
                words = file.read().splitlines()

    filtered_words = [word.strip().lower() for word in words if
                      len(word.strip()) == word_length]

    if not filtered_words:
        print(f"Предупреждение: в словаре нет слов длины {word_length}")
        filtered_words = [word.strip().lower() for word in words if
                          word.strip()]

    return filtered_words


def main():
    parser = argparse.ArgumentParser(description='Игра "Быки и коровы"')
    parser.add_argument('dictionary', help='Путь к файлу словаря или URL')
    parser.add_argument('length', type=int, nargs='?', default=5,
                        help='Длина слов (по умолчанию 5)')

    args = parser.parse_args()

    words = load_dictionary(args.dictionary, args.length)

    if not words:
        print("Ошибка: словарь пуст или не содержит подходящих слов.")
        sys.exit(1)

    def ask(prompt, valid=None):
        while True:
            try:
                user_input = input(prompt).strip()
                if valid is None or user_input in valid:
                    return user_input
                print(
                    f"Пожалуйста, введите слово из списка допустимых слов (длина: {len(valid[0])})")
            except (EOFError, KeyboardInterrupt):
                print("\nВыход из игры.")
                sys.exit(0)
            except Exception as e:
                print(f"Произошла ошибка при вводе: {e}")
                print("Пожалуйста, попробуйте снова.")

    def inform(format_string, bulls, cows):
        print(format_string.format(bulls, cows))

    attempts = gameplay(ask, inform, words)

    print(f"Поздравляем! Вы угадали слово за {attempts} попыток.")


if __name__ == "__main__":
    main()