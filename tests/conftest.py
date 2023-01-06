import pytest


@pytest.fixture(scope="session")
def test_path(tmp_path_factory):
    """Creation de l'arborescence 'a_dir/last_dir'"""
    dir = tmp_path_factory.mktemp("a_dir", numbered=False) / "last_dir"
    dir.mkdir()
    return dir


@pytest.fixture
def test_tree(tmp_path_factory):
    """Réalise l'arborescence de test suivante:
    root_dir/
    dirname_A / sub_dirname / hello.txt
    dirname_B / hi.txt
    dirname_B / sub_dirname
    dirname_B / sub_dirname_B
    """
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
