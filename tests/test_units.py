# from backup import core
from backup import utils
from unittest.mock import Mock


def test_get_last_folder_empty(test_path):
    """Test si la fonction get_last_folder retourne bien le dernier dossier du
    chemin 'test_path' lorsque ce dernier dossier est vide."""
    assert "last_dir" == utils.get_last_folder(test_path)


def test_get_last_folder_not_empty(test_path):
    """Test si la fonction get_last_folder retourne bien le dernier dossier du
    chemin 'test_path' lorsque ce dernier dossier contient un fichier."""
    file_test = test_path / "file.txt"
    file_test.write_text("test file")
    assert file_test.read_text() == "test file"
    assert "last_dir" == utils.get_last_folder(test_path)


def test_get_dir_list(test_tree):
    """Test si la fonction retourne la liste des dossiers et sous-dossiers
    présents dans le dossier parent root_folder_src."""
    expected_directories = [
        r"dirname_A",
        r"dirname_A\sub_dirname",
        r"dirname_B",
        r"dirname_B\sub_dirname",
        r"dirname_B\sub_dirname_B",
        r"dirname_B\sub_dirname_B\sub_sub_dirname_B",
    ]
    root_folder_src = "root_dir"
    assert (
        utils.get_dir_list(str(test_tree), root_folder_src)
        == expected_directories
    )


def test_diff_between_list1_and_list2():
    """Test si la fonction 'diff_between_two_lists' retourne les éléments
    présents dans la liste 1 mais pas dans la liste 2."""
    list_1 = ["a", "b", "c", "d", "e", "g"]
    list_2 = ["a", "b", "d", "e", "f", "h", "i"]
    assert utils.diff_between_two_lists(list_1, list_2) == ["c", "g"]


def test_diff_between_list2_and_list1():
    """Test si la fonction 'diff_between_two_lists' retourne les éléments
    présents dans la liste 2 mais pas dans la liste 1."""
    list_1 = ["a", "b", "c", "d", "e", "g"]
    list_2 = ["a", "b", "d", "e", "f", "h", "i"]
    assert utils.diff_between_two_lists(list_2, list_1) == ["f", "h", "i"]


def test_diff_between_list1_is_empty_and_list2():
    """Test si la fonction 'diff_between_two_lists' retourne une liste vide si
    la liste 1 est vide."""
    list_1 = []
    list_2 = ["a", "b", "d", "e", "f", "h", "i"]
    assert utils.diff_between_two_lists(list_1, list_2) == []


def test_diff_between_list1_and_list2_is_empty():
    """Test si la fonction 'diff_between_two_lists' retourne liste 1 si la
    liste 2 est vide."""
    list_1 = ["a", "b", "c", "d", "e", "g"]
    list_2 = []
    assert utils.diff_between_two_lists(list_1, list_2) == [
        "a",
        "b",
        "c",
        "d",
        "e",
        "g",
    ]


def test_diff_between_two_list_if_list1_not_list():
    """Test si la fonction 'diff_between_two_lists' retourne None si list_1
    n'est pas une liste."""
    list_1 = "not a list"
    list_2 = ["a", "b", "d", "e", "f", "h", "i"]
    assert not (utils.diff_between_two_lists(list_1, list_2))
    assert not (utils.diff_between_two_lists(list_2, list_1))


def test_diff_between_two_list_if_list2_not_list():
    """Test si la fonction 'diff_between_two_lists' retourne None si list_2
    n'est pas une liste."""
    list_1 = ["a", "b", "c", "d", "e", "g"]
    list_2 = "not a list"
    assert not (utils.diff_between_two_lists(list_1, list_2))
    assert not (utils.diff_between_two_lists(list_2, list_1))


def test_diff_between_two_list_if_list2_is_none():
    """Test si la fonction 'diff_between_two_lists' retourne list_1
    si list_2 est None."""
    list_1 = ["a", "b", "c", "d", "e", "g"]
    list_2 = None
    assert utils.diff_between_two_lists(list_1, list_2) == list_1


def test_diff_between_two_list_if_list1_is_none():
    """Test si la fonction 'diff_between_two_lists' retourne list_2
    si list_1 est None."""
    list_1 = None
    list_2 = ["a", "b", "c", "d", "e", "g"]
    assert utils.diff_between_two_lists(list_1, list_2) == list_2


def test_diff_between_two_list_if_lists_are_none():
    """Test si la fonction 'diff_between_two_lists' retourne None
    si list_1 et list_2 sont None."""
    list_1 = None
    list_2 = None
    assert not utils.diff_between_two_lists(list_1, list_2)


def test_create_folders(tmp_path):
    """Test la création de la liste de dossiers 'folders' dans un dossier
    temporaire."""
    folders = ["dir_A", "dir_B", "dir_C"]
    utils.create_folders(folders, tmp_path)

    get_folders = [f.name for f in list(tmp_path.iterdir()) if f.is_dir()]
    assert folders.sort() == get_folders.sort()


def test_build_paths():
    """vérifie que 'build_path' retourne une liste dontenant les chemins
    complets de l'arborescence."""
    root_path = r"C:\root_dir"
    folders = ["dirname_A", r"dirname_B\sub_dirname"]
    expected_paths = [
        r"C:\root_dir",
        r"C:\root_dir\dirname_A",
        r"C:\root_dir\dirname_B\sub_dirname",
    ]
    assert expected_paths == utils.build_paths(root_path, folders)


def test_get_files_names_and_sizes(test_files_name_and_size):
    """Teste si la fonction 'get_files_names_and_sizes' retourne un
    dictionnaire contenant les noms et tailles des fichiers dans le répertoire
    passé en argument.

    {chemin du dossier racine : {nom du fichier : taille, ...}}
    """

    expected = {test_files_name_and_size: {"hello.txt": 14, "lorem.txt": 465}}
    assert expected == utils.get_files_names_and_sizes(
        test_files_name_and_size
    )


def test_files_names_list(test_files_name_and_size, monkeypatch):
    """teste que la fonction 'files_names_list' retourne la liste des fichiers
    présents dans le dossier passé en argument"""

    def mock_get_files_names_and_sizes(path):
        return {test_files_name_and_size: {"hello.txt": 14, "lorem.txt": 465}}

    monkeypatch.setattr(
        "backup.utils.get_files_names_and_sizes",
        mock_get_files_names_and_sizes,
    )
    expected_list = ["hello.txt", "lorem.txt"]
    assert expected_list == utils.files_names_list(test_files_name_and_size)


def test_files_names_list_key_error(test_files_name_and_size, monkeypatch):
    """teste que la fonction 'files_names_list' retourne None si la clé du
    dictionnaire généré par get_files_names_and_sizes n'est pas trouvé"""

    def mock_get_files_names_and_sizes(path):
        return {'error key': {"hello.txt": 14, "lorem.txt": 465}}

    monkeypatch.setattr(
        "backup.utils.get_files_names_and_sizes",
        mock_get_files_names_and_sizes,
    )
    expected_list = None
    assert expected_list == utils.files_names_list(test_files_name_and_size)


def test_files_sizes_list(test_files_name_and_size, monkeypatch):
    """teste que la fonction 'files_sizes_list' retourne un dict
    'nom du fichier' : taille du fichier qui sont dans le dossier passé
    en argument"""

    def mock_get_files_names_and_sizes(path):
        return {test_files_name_and_size: {"hello.txt": 14, "lorem.txt": 465}}

    monkeypatch.setattr(
        "backup.utils.get_files_names_and_sizes",
        mock_get_files_names_and_sizes,
    )
    expected_list = {"hello.txt": 14, "lorem.txt": 465}
    assert expected_list == utils.files_sizes_list(test_files_name_and_size)


def test_files_sizes_list_key_error(test_files_name_and_size, monkeypatch):
    """teste que la fonction 'files_sizes_list' retourne None si la clé du
    dictionnaire généré par get_files_names_and_sizes n'est pas trouvé"""

    def mock_get_files_names_and_sizes(path):
        return {'error key': {"hello.txt": 14, "lorem.txt": 465}}

    monkeypatch.setattr(
        "backup.utils.get_files_names_and_sizes",
        mock_get_files_names_and_sizes,
    )
    expected_list = None
    assert expected_list == utils.files_sizes_list(test_files_name_and_size)


def test_remove_subfolders_paths():
    """Verifie que 'remove_subfolders_paths' supprime du chemin les sous-
    dossiers lorsqu'ils existent."""
    path_folders = [
        r"root\dirname_A",
        r"root\dirname_A\sub_dirname_A",
        r"root\dirname_A\sub_dirname_A\sub_sub_dirname_A",
        r"root\dirname_B\sub_dirname_B",
    ]
    expected_path = [r"root\dirname_A", r"root\dirname_B\sub_dirname_B"]
    assert expected_path == utils.remove_subfolders_paths(path_folders)


def test_delete_folders_path_not_found(folders_tree, monkeypatch, capsys):
    """vérifie que lorsque le chemin du dossier à effacer n'est pas trouvé
    alors le message affiché dans la console est correcte"""
    path_target = r'Z:\backup'

    def mock_remove_subfolders_paths(path_folders: list) -> list:
        return [
            r"root_target\dirname_A",
        ]

    monkeypatch.setattr(
        "backup.utils.remove_subfolders_paths",
        mock_remove_subfolders_paths,
    )
    utils.delete_folders(folders_tree, path_target)
    captured = capsys.readouterr()
    expected_msg = (
        "[WinError 3] Le chemin d’accès spécifié est introuvable:"
        " 'Z:\\\\backup\\\\root_target\\\\dirname_A'"
    )
    expected = (
        "*" * len(expected_msg)
        + '\n'
        + expected_msg
        + '\n'
        + "*" * len(expected_msg)
        + '\n'
    )
    assert captured.out == expected


# def test_delete_folders(folders_tree, monkeypatch):
#     """Verifie que les dossiers dirname_A et sub_dirname_B et ce qu'ils
#     contiennent sont supprimés de la cible path_target """
#     path_target = r'Z:\backup'

#     def mock_remove_subfolders_paths(path_folders: list) -> list:
#         return [
#             r"root_target\dirname_A",
#             r"root_target\dirname_B\sub_dirname_B"
#         ]

#     monkeypatch.setattr(
#         "backup.utils.remove_subfolders_paths",
#         mock_remove_subfolders_paths,
#     )
#     utils.delete_folders(folders_tree, path_target)


def test_get_src_dirs_and_target_dirs(monkeypatch):
    """Verifie que la fonction 'get_src_dirs_and_target_dirs' retourne la
    liste des sous dossiers contenus dans les dossiers source et cible"""
    mock_get_dir_path = Mock()
    mock_get_dir_path.side_effect = [
        r"source_path\dirname_A",
        r"target_path\dirname_B",
    ]
    mock_get_dir_list = Mock()
    mock_get_dir_list.side_effect = [
        ["source_dir_A", "source_dir_B"],
        ["target_dir_A", "target_dir_B"],
    ]

    def mock_get_last_folder(path_source):
        return "source_dir_A"

    monkeypatch.setattr("backup.utils.get_dir_path", mock_get_dir_path)
    monkeypatch.setattr("backup.utils.get_dir_list", mock_get_dir_list)
    monkeypatch.setattr("backup.utils.get_last_folder", mock_get_last_folder)
    expected = (
        ('source_path\\dirname_A', ['source_dir_A', 'source_dir_B']),
        ('target_path\\dirname_B', ['target_dir_A', 'target_dir_B']),
    )
    assert utils.get_src_dirs_and_target_dirs() == expected


def test_files_manager_copy_delete():
    ...


# files_manager_update
# files_manager_copy_delete
# directories_manager_create_delete
