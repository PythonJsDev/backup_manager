# from backup import core
from backup import utils


def test_get_last_folder_empty(test_path):
    """Test si la fonction get_last_folder retourne bien le dernier dossier du
    chemin 'test_path' lorsque ce dernier dossier est vide"""
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
        'dirname_A',
        'dirname_A\\sub_dirname',
        'dirname_B',
        'dirname_B\\sub_dirname',
        'dirname_B\\sub_dirname_B',
        'dirname_B\\sub_dirname_B\\sub_sub_dirname_B'
    ]
    root_folder_src = "root_dir"
    assert utils.get_dir_list(str(test_tree), root_folder_src) == expected_directories


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
    """Test si la fonction 'diff_between_two_lists' retourne
    une liste vide si la liste 1 est vide."""
    list_1 = []
    list_2 = ["a", "b", "d", "e", "f", "h", "i"]
    assert utils.diff_between_two_lists(list_1, list_2) == []


def test_diff_between_list1_and_list2_is_empty():
    """Test si la fonction 'diff_between_two_lists' retourne
    liste 1 si la liste 2 est vide."""
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


def test_create_folders(tmp_path):
    """Test la création de la liste de dossiers 'folders' dans un dossier
    temporaire."""
    folders = ["toto", "tata", "titi"]
    utils.create_folders(folders, tmp_path)

    get_folders = [f.name for f in list(tmp_path.iterdir()) if f.is_dir()]
    assert folders.sort() == get_folders.sort()
