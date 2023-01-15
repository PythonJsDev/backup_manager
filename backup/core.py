from . import utils
from . import in_out
from typing import Tuple, Optional


def get_input_path() -> Tuple[Optional[str], Optional[str]]:
    """lecture des chemins pointant vers les dossiers racines
    entrés par l'utilisateur"""
    return in_out.input_path("path_source"), in_out.input_path("path_target")


def run_app():
    path_source = get_input_path()[0]
    path_target = get_input_path()[1]

    root_folder_src = utils.get_last_folder(path_source)
    src_dirs = utils.get_dir_list(path_source, root_folder_src)
    target_dirs = utils.get_dir_list(path_target, root_folder_src)

    if src_dirs and target_dirs:
        utils.directories_manager_create_delete(
            src_dirs, target_dirs, path_target
        )
        utils.files_manager_copy_delete(path_source, path_target, src_dirs)
        utils.files_manager_update(path_source, path_target, src_dirs)
