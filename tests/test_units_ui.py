from backup import in_out
import io


def test_clear_console(capsys):
    """Verifie que le terminal soit effacé"""
    in_out.clear_console()
    captured = capsys.readouterr()
    assert captured.out == ''


def test_title(capsys):
    """Vérifie que le titre de l'application s'affiche dans le terminal"""
    in_out.title()
    assert capsys.readouterr().out == '\n****** Backup Manager  ******\n\n'


def test_info_msg(capsys):
    """Verifie que le message d'info s'affiche dans le terminal"""
    in_out.info_msg("info message")
    assert capsys.readouterr().out == "info message\n"


def test_error_msg(capsys):
    """Verifie que le message d'erreur s'affiche dans le terminal"""
    in_out.error_msg("error message")
    assert (
        capsys.readouterr().out
        == "*************\nerror message\n*************\n"
    )


def test_get_dir_ask_path(capsys, monkeypatch):
    """Verifie que la fonction 'get_dir' demande le chemin du dossier"""
    monkeypatch.setattr("sys.stdin", io.StringIO("path folder\n"))
    in_out.get_dir_path('source folder path')
    assert capsys.readouterr().out == "source folder path >> "


def test_get_dir_path(monkeypatch):
    """Verifie que la fonction 'get_dir_path' retourne le chemin du dossier
    entré par l'utilisateur"""
    monkeypatch.setattr("sys.stdin", io.StringIO("folder path\n"))
    path_returned = in_out.get_dir_path('source folder path')
    assert path_returned == "folder path"


def test_get_dir_remove_spaces(monkeypatch):
    """Verifie que la fonction 'get_dir' supprime les eventuels espaces
    emtrés par l'utilisateur"""
    monkeypatch.setattr("sys.stdin", io.StringIO("  folder path \n"))
    path_returned = in_out.get_dir_path('source folder path')
    assert path_returned == "folder path"


def test_display_list_of_items(capsys):
    """Verifie que la liste d'items s'affiche sur le terminal"""
    in_out.display_list_of_items(['dir_A', 'dir_B', 'dir_C'])
    assert capsys.readouterr().out == "dir_A,dir_B,dir_C\n"


def test_continue_or_stop_ask_question(capsys, monkeypatch):
    """Verifie que la fonction 'continue_or_stop' demande à l'utilisateur
    de continuer ou d'arrêter le programme"""
    monkeypatch.setattr("sys.stdin", io.StringIO("y\n"))
    in_out.continue_or_stop()
    assert (
        capsys.readouterr().out
        == "Taper 'y' pour continuer et 'n' pour arrêter: "
    )


def test_continue_or_stop_yes(monkeypatch):
    """Verifie que la fonction 'continue_or_stop' retourne True
    si l'utilisateur tape 'y'"""
    monkeypatch.setattr("sys.stdin", io.StringIO("y\n"))
    assert in_out.continue_or_stop()


def test_continue_or_stop_no(monkeypatch):
    """Verifie que la fonction 'continue_or_stop' retourne False
    si l'utilisateur tape 'n'"""
    monkeypatch.setattr("sys.stdin", io.StringIO("n\n"))
    assert not in_out.continue_or_stop()


def test_continue_or_stop_loop_until_yes(capsys, monkeypatch):
    """Verifie que la fonction 'continue_or_stop' boucle tant
    que l'utilisateur ne rentre pas 'y'
    La fonction retourne alors True"""
    monkeypatch.setattr("sys.stdin", io.StringIO("value\n123\ny"))
    valeur_returned = in_out.continue_or_stop()
    print(capsys.readouterr().out)
    assert capsys.readouterr().out == (
        "Taper 'y' pour continuer et 'n' pour arrêter: "
        "Taper 'y' pour continuer et 'n' pour arrêter: "
        "Taper 'y' pour continuer et 'n' pour arrêter: \n"
    )
    assert valeur_returned


def test_continue_or_stop_loop_until_non(capsys, monkeypatch):
    """Verifie que la fonction 'continue_or_stop' boucle tant
    que l'utilisateur ne rentre pas 'n'
    La fonction retourne alors False"""
    monkeypatch.setattr("sys.stdin", io.StringIO("value\n123\nn"))
    valeur_returned = in_out.continue_or_stop()
    print(capsys.readouterr().out)
    assert capsys.readouterr().out == (
        "Taper 'y' pour continuer et 'n' pour arrêter: "
        "Taper 'y' pour continuer et 'n' pour arrêter: "
        "Taper 'y' pour continuer et 'n' pour arrêter: \n"
    )
    assert not valeur_returned
