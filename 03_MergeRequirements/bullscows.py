#!/usr/bin/env python3

import random
import urllib.request
import sys
import argparse
import cowsay
import os


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

    cow_list = cowsay.list_cows()

    custom_cow = None
    kitten_path = 'kitten.cow'

    if os.path.isfile(kitten_path):
        try:
            with open(kitten_path) as f:
                custom_cow = cowsay.read_dot_cow(f)
            print(
                f"Используется пользовательская корова из файла {kitten_path}")
        except Exception as e:
            print(f"Ошибка при чтении файла коровы: {e}")
            custom_cow = None

    def ask(prompt, valid=None):
        try:
            if custom_cow:
                print(cowsay.cowsay(prompt, cowfile=custom_cow))
            else:
                random_cow = random.choice(cow_list)
                print(cowsay.cowsay(prompt, cow=random_cow))
        except Exception as e:
            print(f"Ошибка при использовании cowsay: {e}")
            print(prompt)

        while True:
            try:
                user_input = input(prompt).strip()
                if valid is None or user_input in valid:
                    return user_input

                error_msg = f"Пожалуйста, введите слово из списка допустимых слов (длина: {len(valid[0])})"
                try:
                    random_cow = random.choice(cow_list)
                    print(cowsay.cowsay(error_msg, cow=random_cow))
                except Exception:
                    print(error_msg)
            except (EOFError, KeyboardInterrupt):
                print("\nВыход из игры.")
                sys.exit(0)
            except Exception as e:
                print(f"Произошла ошибка при вводе: {e}")
                print("Пожалуйста, попробуйте снова.")

    def inform(format_string, bulls, cows):
        message = format_string.format(bulls, cows)
        try:
            random_cow = random.choice(cow_list)
            print(cowsay.cowsay(message, cow=random_cow))
        except Exception as e:
            print(f"Ошибка при использовании cowsay: {e}")
            print(message)

    attempts = gameplay(ask, inform, words)

    final_message = f"Поздравляем! Вы угадали слово за {attempts} попыток."
    try:
        if custom_cow:
            print(cowsay.cowsay(final_message, cowfile=custom_cow))
        else:
            random_cow = random.choice(cow_list)
            print(cowsay.cowsay(final_message, cow=random_cow))
    except Exception:
        print(final_message)


if __name__ == "__main__":
    main()