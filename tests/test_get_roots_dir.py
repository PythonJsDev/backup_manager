from backup import core


def test_get_root_path(source_path_root, target_path_root):
    assert core.get_input_path()[0] == source_path_root
    assert core.get_input_path()[1] == target_path_root
