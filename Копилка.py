import os
import json


def safe_input(text):
    value = input(text)
    if value.lower() == "выход":
        print("Программа завершена.")
        exit()
    return value


def actions():
    while True:
        choice_action = safe_input(
            "\n1. Завершить программу\n"
            "2. Зарегистрироваться\n"
            "3. Войти\n"
            "Выберите действие | "
        )

        while choice_action not in ("1", "2", "3"):
            print("Я вас не понимаю!")
            choice_action = safe_input("Напишите 1, 2 или 3 | ")

        if choice_action == "1":
            print("Программа завершена.")
            break

        elif choice_action == "2":
            while True:
                new_user_nick = safe_input("Придумайте ник (0 — Назад, выход — Выход) | ")

                if new_user_nick == "0":
                    break

                if os.path.exists(new_user_nick):
                    print("Этот ник уже занят.")
                    continue

                new_user_password = safe_input("Придумайте пароль (0 — Назад, выход — Выход) | ")

                if new_user_password == "0":
                    continue

                user_bank = {
                    "password": new_user_password,
                    "many": 0
                }

                with open(new_user_nick, "w", encoding="utf-8") as f:
                    json.dump(user_bank, f, ensure_ascii=False, indent=4)

                print("Регистрация успешна!")
                break

        elif choice_action == "3":
            while True:
                user_nick = safe_input("Введите ник (0 — Назад, выход — Выход) | ")

                if user_nick == "0":
                    break

                if not os.path.exists(user_nick):
                    print("Такого пользователя не найдено.")
                    continue

                with open(user_nick, "r", encoding="utf-8") as f:
                    data = json.load(f)

                attempts = 3

                while attempts > 0:
                    user_password = safe_input("Введите пароль (0 — Назад, выход — Выход) | ")

                    if user_password == "0":
                        break

                    if user_password == data["password"]:
                        print("Добро пожаловать,", user_nick)
                        break
                    else:
                        attempts -= 1
                        print("Пароль неправильный! Осталось попыток:", attempts)

                if user_password == "0":
                    break

                if attempts == 0:
                    os.remove(user_nick)
                    print("Системное уведомление: Вы превысили количество попыток ввода пароля и ваш аккаунт был УНИЧТОЖЕН.\nС уважением: система")
                    break

                while True:
                    print("\nВаш баланс:", data["many"], "рублей")

                    choice_many = safe_input(
                        "1. Закинуть деньги\n"
                        "2. Снять деньги\n"
                        "0. Назад\n"
                        "Что хотите сделать? | "
                    )

                    if choice_many == "0":
                        break

                    if choice_many not in ("1", "2"):
                        print("Напишите 1, 2 или 0.")
                        continue

                    if choice_many == "1":
                        while True:
                            deposit = safe_input("Сколько вложить? (0 — Назад, выход — Выход) | ")

                            if deposit == "0":
                                break

                            try:
                                num = int(deposit)
                                if num <= 0:
                                    print("Введите положительное число.")
                                    continue
                                data["many"] += num
                                print("Вы закинули:", num)
                                break
                            except ValueError:
                                print("Можно вводить только цифры.")

                    elif choice_many == "2":
                        while True:
                            withdraw = safe_input("Сколько снять? (0 — Назад, выход — Выход) | ")

                            if withdraw == "0":
                                break

                            try:
                                num = int(withdraw)
                                if num <= 0:
                                    print("Введите положительное число.")
                                    continue
                                if num > data["many"]:
                                    print("Недостаточно средств!")
                                    continue
                                data["many"] -= num
                                print("Вы сняли:", num)
                                break
                            except ValueError:
                                print("Можно вводить только цифры.")

                    with open(user_nick, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)

                break

actions()