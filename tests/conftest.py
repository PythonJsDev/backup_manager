import pytest
from unittest.mock import Mock


@pytest.fixture(scope="session")
def test_path(tmp_path_factory):
    """Creation de l'arborescence 'a_dir/last_dir'."""
    dir = tmp_path_factory.mktemp("a_dir", numbered=False) / "last_dir"
    dir.mkdir()
    return dir


@pytest.fixture(scope="session")
def test_tree(tmp_path_factory):
    """Réalise l'arborescence de test suivante:
    root_dir/ dirname_A / sub_dirname / hello.txt
    root_dir/ dirname_B / hi.txt
    root_dir/ dirname_B / sub_dirname
    root_dir/ dirname_B / sub_dirname_B / sub_sub_dirname_B."""
    root_dir = tmp_path_factory.mktemp("root_dir", numbered=False)
    dir_A = root_dir / "dirname_A"
    dir_A.mkdir()
    sub_dir_A = dir_A / "sub_dirname"
    sub_dir_A.mkdir()
    (sub_dir_A / "hello.txt").write_text("hello")

    dir_B = root_dir / "dirname_B"
    dir_B.mkdir()
    (dir_B / "hi.txt").write_text("hi !")
    sub_dir_B = dir_B / "sub_dirname"
    sub_dir_B.mkdir()

    other_sub_dir_B = dir_B / "sub_dirname_B"
    other_sub_dir_B.mkdir()

    sub_sub_dir_B = other_sub_dir_B / "sub_sub_dirname_B"
    sub_sub_dir_B.mkdir()
    return root_dir


@pytest.fixture(scope="session")
def test_files_name_and_size(tmp_path_factory):
    """Creation des fichiers hello.txt et lorem.txt dans le dossier root."""
    f1_content = "Hello World !!"
    f2_content = """Dolor velit modi dolor voluptatem dolore ut. Eius adipisci
    consectetur modi. Magnam labore non velit aliquam. Modi etincidunt adipisci
    quaerat quiquia dolore. Voluptatem sit etincidunt numquam porro eius. Ipsum
    aliquam magnam dolor labore. Voluptatem quaerat consectetur quiquia
    etincidunt. Velit consectetur modi ipsum velit neque. Sed adipisci dolor
    dolor non labore. Ipsum numquam consectetur voluptatem quaerat quisquam non
    magnam."""
    root = tmp_path_factory.mktemp("root", numbered=False)
    (root / "hello.txt").write_text(f1_content)
    (root / "lorem.txt").write_text(f2_content)
    return root


@pytest.fixture(autouse=True)
def mock_clear(monkeypatch):
    def mock_clear_console():
        return None
    monkeypatch.setattr("backup.in_out.clear_console", mock_clear_console)


@pytest.fixture()
def mock_functions_core(monkeypatch):
    expected_datas = (
        (r'source_path\dirname_A', ['source_dir_A', 'source_dir_B']),
        (r'target_path\dirname_B', ['target_dir_A', 'target_dir_B']),
    )
    mock_clear_console = Mock()
    mock_title = Mock()
    mock_get_src_dirs_and_target_dirs = Mock(return_value=expected_datas)
    mock_directories_manager_create_delete = Mock()
    mock_files_manager_copy_delete = Mock()
    mock_files_manager_update = Mock()

    monkeypatch.setattr("backup.in_out.clear_console", mock_clear_console)
    monkeypatch.setattr("backup.in_out.title", mock_title)
    monkeypatch.setattr(
        "backup.utils.directories_manager_create_delete",
        mock_directories_manager_create_delete,
    )

    monkeypatch.setattr(
        "backup.utils.get_src_dirs_and_target_dirs",
        mock_get_src_dirs_and_target_dirs,
    )
    monkeypatch.setattr(
        "backup.utils.files_manager_copy_delete",
        mock_files_manager_copy_delete,
    )
    monkeypatch.setattr(
        "backup.utils.files_manager_update",
        mock_files_manager_update,
    )
    return {
        'clear_console': mock_clear_console,
        'title': mock_title,
        'get_src_dirs_and_target_dirs': mock_get_src_dirs_and_target_dirs,
        'directories_manager_create_delete':
            mock_directories_manager_create_delete,
        'files_manager_copy_delete': mock_files_manager_copy_delete,
        'files_manager_update': mock_files_manager_update,
    }
