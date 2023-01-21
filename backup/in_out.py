import os
import sys


def clear_console() -> None:
    os.system('cls') if sys.platform.startswith('win32') else os.system(
        'clear'
    )


def title() -> None:
    print()
    print("****** Backup Manager  ******")
    print()


def get_dir_path(ask_path: str) -> str:
    return input(ask_path + " >> ").strip()


# def input_path(path: str) -> str | None:
#     """fonction provisoire qui retourne un chemin source ou cible"""
#     if path == 'path_source':
#         return r'D:\users\test backup manager\vanilla'
#     if path == 'path_target':
#         return r'E:\DEV 2022 novembre 06\DEV\apps_js\vanilla'
#     return None


def error_msg(msg: str) -> None:
    print('*' * len(msg))
    print(msg)
    print('*' * len(msg))


def info_msg(msg: str) -> None:
    print(msg)


def display_list_of_items(items: list[str]) -> None:
    print(','.join(items))


def continue_or_stop():
    while True:
        choice = input("Taper 'y' pour continuer et 'n' pour arrêter: ")
        if choice == 'y':
            return True
        if choice == 'n':
            return False
