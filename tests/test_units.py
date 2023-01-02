# from backup import core
from backup import utils


SOURCE_PATH = r"D:\users\test backup manager\vanilla"


def test_get_last_folder():
    """Test si la fonction get_last_folder retourne bien le dernier dossier du
    chemin."""
    assert "vanilla" == utils.get_last_folder(SOURCE_PATH)


def test_get_dir_list():
    """Test si la fonction retourne la liste des dossiers et sous-dossiers
    présents dans le dossier parent root_folder_src."""
    root_folder_src = "vanilla"
    expected_directories = [
        ".vscode",
        "jason c",
        "jason c\\test new folder",
        "node_modules",
        "node_modules\\.bin",
        "node_modules\\uuid",
        "node_modules\\uuid\\dist",
        "node_modules\\uuid\\dist\\bin",
        "node_modules\\uuid\\dist\\commonjs-browser",
        "node_modules\\uuid\\dist\\esm-browser",
        "node_modules\\uuid\\dist\\esm-node",
        "test folder",
    ]

    assert utils.get_dir_list(SOURCE_PATH, root_folder_src) == expected_directories


def test_diff_between_two_lists():
    """Test si la fonction 'diff_between_two_lists' retourne les éléments
    présents dans la liste 1 mais pas dans la liste 2 et inversement."""
    list_1 = ["a", "b", "c", "d", "e", "g"]
    list_2 = ["a", "b", "d", "e", "f", "h", "i"]
    assert utils.diff_between_two_lists(list_1, list_2) == ["c", "g"]
    assert utils.diff_between_two_lists(list_2, list_1) == ["f", "h", "i"]


def test_create_folders(tmp_path):
    """Test la création de la liste de dossiers 'folders' dans un dossier
    temporaire."""
    folders = ["toto", "tata", "titi"]
    utils.create_folders(folders, tmp_path)

    get_folders = [f.name for f in list(tmp_path.iterdir()) if f.is_dir()]
    assert folders.sort() == get_folders.sort()
