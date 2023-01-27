from backup import utils
from unittest.mock import Mock, call


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


def test_diff_between_two_list_if_lists_are_none():
    """Test si la fonction 'diff_between_two_lists' retourne None
    si list_1 et list_2 sont None."""
    list_1 = None
    list_2 = None
    assert not utils.diff_between_two_lists(list_1, list_2)


def test_diff_between_two_list_if_list2_is_none():
    """Test si la fonction 'diff_between_two_lists' retourne list_1
    si list_2 est None."""
    list_1 = ["a", "b", "c", "d", "e", "g"]
    list_2 = None
    assert utils.diff_between_two_lists(list_1, list_2)


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


def test_delete_folders_call_shutil(monkeypatch):
    """Verifie que la fonction shutil.rmtree soit appelé le bon nombre de fois
    avec les bons arguments"""
    folders_tree = [
        r"Z:\backup\root_target\dirname_A",
        r"Z:\backup\root_target\dirname_B\sub_dirname_B",
    ]
    path_target = r'Z:\backup'
    mock_shutil = Mock()
    monkeypatch.setattr("backup.utils.shutil", mock_shutil)

    def mock_remove_subfolders_paths(path_folders: list) -> list:
        return [
            r"root_target\dirname_A",
            r"root_target\dirname_B\sub_dirname_B",
        ]

    monkeypatch.setattr(
        "backup.utils.remove_subfolders_paths",
        mock_remove_subfolders_paths,
    )
    utils.delete_folders(folders_tree, path_target)
    expected_calls = [
        call(r"Z:\backup\root_target\dirname_A"),
        call(r"Z:\backup\root_target\dirname_B\sub_dirname_B"),
    ]
    for called, expected_call in zip(
        mock_shutil.rmtree.mock_calls, expected_calls
    ):
        assert called == expected_call


def test_delete_folders_OSError(monkeypatch):
    """Verifie que si shutil.rmtree lève une exception OSError,
    celle-ci est gérée."""
    folders_tree = [
        r"Z:\backup\root_target\dirname_A",
    ]
    path_target = r'Z:\backup'
    mock_shutil = Mock()
    monkeypatch.setattr("backup.utils.shutil", mock_shutil)
    mock_shutil.rmtree.side_effect = OSError('error message')
    mock_error_msg = Mock()
    monkeypatch.setattr("backup.utils.error_msg", mock_error_msg)
    error_msg = "Une erreur s'est produite !! : error message"

    utils.delete_folders(folders_tree, path_target)
    mock_error_msg.assert_called_once_with(error_msg)


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

    def mock_get_last_folder(path_source: str) -> str:
        return "source_dir_A"

    monkeypatch.setattr("backup.utils.get_dir_path", mock_get_dir_path)
    monkeypatch.setattr("backup.utils.get_dir_list", mock_get_dir_list)
    monkeypatch.setattr("backup.utils.get_last_folder", mock_get_last_folder)
    expected = (
        (r'source_path\dirname_A', ['source_dir_A', 'source_dir_B']),
        (r'target_path\dirname_B', ['target_dir_A', 'target_dir_B']),
    )
    assert utils.get_src_dirs_and_target_dirs() == expected


def test_copy_or_update_files_call_shutil(monkeypatch):
    """Verifie que la fonction shutil.copy2 soit appelé le bon nombre de fois
    avec les bons arguments"""
    files_to_copy_update = ["file_a.txt", "file_b.py", "file_c.png"]
    path_src = 'dirname_source'
    path_target = 'dirname_target'
    mock_shutil = Mock()

    monkeypatch.setattr("backup.utils.shutil", mock_shutil)
    utils.copy_or_update_files(files_to_copy_update, path_src, path_target)

    expected_calls = [
        call(r"dirname_source\file_a.txt", r"dirname_target\file_a.txt"),
        call(r"dirname_source\file_b.py", r"dirname_target\file_b.py"),
        call(r"dirname_source\file_c.png", r"dirname_target\file_c.png"),
    ]
    for called, expected_call in zip(
        mock_shutil.copy2.mock_calls, expected_calls
    ):
        assert called == expected_call


def test_copy_or_update_files_OSError(monkeypatch):
    """Verifie que si shutil.copy2 lève une exception OSError,
    celle-ci est gérée."""
    files_to_copy = ["file_a.txt"]
    path_src = r'dirname_source\file_a.txt'
    path_target = r"dirname_target\file_a.txt"
    mock_shutil = Mock()
    mock_shutil.copy2.side_effect = OSError('error message')
    mock_error_msg = Mock()
    error_msg = "Une erreur s'est produite !! : error message"
    monkeypatch.setattr("backup.utils.shutil", mock_shutil)
    monkeypatch.setattr("backup.utils.error_msg", mock_error_msg)
    utils.copy_or_update_files(files_to_copy, path_src, path_target)
    mock_error_msg.assert_called_once_with(error_msg)


def test_sure_to_erase_call_info_msg(mock_functions_sure_to_erase_or_update):
    """vérifie que 'sure_to_erase' appele 'info_msg' une seule fois et avec
    le bon argument."""
    confirm_msg = mock_functions_sure_to_erase_or_update.get('confirm_msg')
    path = mock_functions_sure_to_erase_or_update.get('path')

    utils.sure_to_erase_or_update(
        mock_functions_sure_to_erase_or_update.get('items'), confirm_msg, path
    )
    mock_functions_sure_to_erase_or_update.get(
        'info_msg'
    ).assert_called_once_with(f"{confirm_msg} {path}")


def test_sure_to_erase_call_display_list_of_items(
    mock_functions_sure_to_erase_or_update,
):
    """vérifie que 'sure_to_erase' appele 'display_list_of_items' une seule
    fois et avec le bon argument."""
    confirm_msg = mock_functions_sure_to_erase_or_update.get('confirm_msg')
    path = mock_functions_sure_to_erase_or_update.get('path')
    items = mock_functions_sure_to_erase_or_update.get('items')
    utils.sure_to_erase_or_update(items, confirm_msg, path)
    mock_functions_sure_to_erase_or_update.get(
        'display_list_of_items'
    ).assert_called_once_with(items)

# files_names_list path_no valid
# get_files_names_and_sizes path no valid