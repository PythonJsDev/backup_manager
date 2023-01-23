from backup import core


def test_run_app_clear_console(mock_functions_core):
    """Verifie que 'run_app' appele la fonction clear_console"""
    core.run_app()
    mock_functions_core.get('clear_console').assert_called_once()


def test_run_app_title(mock_functions_core):
    """Verifie que 'run_app' appele la fonction 'title'"""
    core.run_app()
    mock_functions_core.get('title').assert_called_once()


def test_run_app_get_src_dirs_and_target_dirs(mock_functions_core):
    """Verifie que 'run_app' appele la fonction 'get_src_dirs_and_target_dirs'
    """
    core.run_app()
    mock_functions_core.get(
        'get_src_dirs_and_target_dirs'
    ).assert_called_once()


def test_run_app_directories_manager_create_delete(mock_functions_core):
    """Verifie que 'run_app' appele la fonction
    'directories_manager_create_delete' avec les bons arguments
    """
    src_dirs = ['source_dir_A', 'source_dir_B']
    target_dirs = ['target_dir_A', 'target_dir_B']
    path_target = r'target_path\dirname_B'

    core.run_app()
    mock_functions_core.get(
        'directories_manager_create_delete'
    ).assert_called_once_with(src_dirs, target_dirs, path_target)


def test_run_app_files_manager_copy_delete(mock_functions_core):
    """Verifie que 'run_app' appele la fonction
    'files_manager_copy_delete' avec les bons arguments
    """
    src_dirs = ['source_dir_A', 'source_dir_B']
    path_target = r'target_path\dirname_B'
    path_source = r'source_path\dirname_A'
    core.run_app()
    mock_functions_core.get(
        'files_manager_copy_delete'
    ).assert_called_once_with(path_source, path_target, src_dirs)


def test_run_app_files_manager_update(mock_functions_core):
    """Verifie que 'run_app' appele la fonction
    'files_manager_update' avec les bons arguments
    """
    src_dirs = ['source_dir_A', 'source_dir_B']
    path_target = r'target_path\dirname_B'
    path_source = r'source_path\dirname_A'
    core.run_app()
    mock_functions_core.get(
        'files_manager_update'
    ).assert_called_once_with(path_source, path_target, src_dirs)
