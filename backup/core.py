from . import utils
from . import in_out


def run_app():
    in_out.clear_console()
    in_out.title()
    source_datas, target_datas = utils.get_src_dirs_and_target_dirs()
    path_source, src_dirs = source_datas
    path_target, target_dirs = target_datas

    if src_dirs and target_dirs:
        utils.directories_manager_create_delete(
            src_dirs, target_dirs, path_target
        )
        utils.files_manager_copy_delete(path_source, path_target, src_dirs)
        utils.files_manager_update(path_source, path_target, src_dirs)
