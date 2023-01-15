
def input_path(path: str) -> str | None:
    """fonction provisoire qui retourne un chemin source ou cible"""
    if path == 'path_source':
        return r'D:\users\test backup manager\vanilla'
    if path == 'path_target':
        return r'E:\DEV 2022 novembre 06\DEV\apps_js\vanilla'
    return None


def error_msg(msg: str) -> None:
    print(msg)


def info_msg(msg: str) -> None:
    print(msg)
