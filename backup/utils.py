import os
import pathlib
import shutil
from backup.in_out import (
    error_msg,
    get_dir_path,
    display_list_of_items,
    info_msg,
    continue_or_stop,
)


def get_last_folder(path: str) -> str:
    """Retourne le dernier dossier d'un chemin."""
    return pathlib.PurePath(path).name


def get_dir_list(path: str, root_folder: str) -> list[str] | None:
    """Retourne la liste des chemins des dossiers et des sous-dossiers à partir
    du répertoire racine."""
    dirs_list = []
    try:
        for element in pathlib.Path(path).iterdir():
            if element.is_dir():
                dirs_list.append(str(element).split(root_folder)[1][1:])
                folders = get_dir_list(str(element), root_folder)
                if folders:
                    dirs_list.extend(folders)
        return dirs_list
    except OSError as err:
        error_msg(str(err))
        return None


def get_src_dirs_and_target_dirs() -> tuple[
    tuple[str, list[str]], tuple[str, list[str]]
]:
    """Demande à l'utilisateur le chemin des dossiers source et cible
    et retourne la liste des sous dossiers qu'ils contiennent,
    ainsi que les chemins source et cible entrés par l'utilisateur."""
    src_dirs: list[str] | None = []
    target_dirs: list[str] | None = []

    while True:
        if not src_dirs:
            path_source = get_dir_path('chemin source')
        if not target_dirs:
            path_target = get_dir_path('chemin cible')
        root_folder_src = get_last_folder(path_source)
        root_folder_target = get_last_folder(path_target)
        if root_folder_src != root_folder_target:
            error_msg((f"Les dossiers racines {root_folder_src} et "
                      f"{root_folder_target} doivent avoir le même nom"))
            break
        src_dirs = get_dir_list(path_source, root_folder_src)
        target_dirs = get_dir_list(path_target, root_folder_src)
        if src_dirs and target_dirs:
            break
    return (path_source, src_dirs), (path_target, target_dirs)


def diff_between_two_lists(
    list_1: list | None, list_2: list | None
) -> list | None:
    """Retourne les éléments présents dans list_1 mais pas dans list_2."""
    if isinstance(list_1, list) and isinstance(list_2, list):
        return [el for el in list_1 if el not in list_2]
    if isinstance(list_1, list) and not list_2:
        return list_1
    return None


def create_folders(folders: list[str], path: str) -> None:
    """Création de la liste de dossiers passée en paramètre."""
    for folder in folders:
        dir = pathlib.PurePosixPath(path).joinpath(folder)
        pathlib.Path(dir).mkdir(exist_ok=True)


def remove_subfolders_paths(path_folders: list[str]) -> list[str]:
    """Supprime les chemins vers les sous-dossiers.

    Retourne la liste des chemins vers les dossiers racines
    """
    path_root_folders = [path_folders[0]]
    root_path = path_folders[0]
    for elem in path_folders:
        if not elem.startswith(root_path):
            root_path = elem
            path_root_folders.append(elem)
    return path_root_folders


def delete_folders(folders: list[str], path: str):
    """Supprime la liste de dossiers 'folders', des sous-dossiers et des
    fichiers qu'ils contiennent dans le répertoire racine pointé par path."""
    for folder in remove_subfolders_paths(folders):
        try:
            shutil.rmtree(os.path.join(path, folder))
        except OSError as err:
            error_msg(f"Une erreur s'est produite !! : {err}")


def files_names_list(path_dir: str) -> list[str] | None:
    """Retourne la liste des fichiers contenus dans le dossier passé en
    paramètre."""
    if os.path.exists(path_dir):
        names_and_sizes = get_files_names_and_sizes(path_dir).get(path_dir)
        if names_and_sizes:
            return list(names_and_sizes.keys())
    return None


def files_sizes_list(path_dir: str) -> dict[str, int] | None:
    """Retourne un dict {nom du fichier: taille des fichiers} contenus dans le
    dossier passé en paramètre."""
    return get_files_names_and_sizes(path_dir).get(path_dir)


def directories_manager_create_delete(
    src_dirs_list: list, target_dirs_list: list, path_target: str
):
    """Création des dossiers manquants sur la cible et suppression des dossiers
    présents sur la cible mais pas sur la source."""
    missing_folders = diff_between_two_lists(src_dirs_list, target_dirs_list)
    excess_folders = diff_between_two_lists(target_dirs_list, src_dirs_list)
    if missing_folders:
        create_folders(missing_folders, path_target)
    if excess_folders:
        if len(excess_folders) > 1:
            msg = (
                "Les dossiers suivants vont être supprimés du dossier"
                " cible:\n"
            )
        else:
            msg = "Le dossier suivant va être supprimé du dossier cible:\n"
        sure_to_erase_or_update(excess_folders, msg, path_target)

        if continue_or_stop():
            delete_folders(excess_folders, path_target)


def build_paths(root_path: str, folders: list[str]) -> list[str]:
    """Retourne la list des chemins complets de toute l'arborescence."""
    paths = [os.path.join(root_path, dir) for dir in folders]
    paths.insert(0, root_path)
    return paths


def files_manager_copy_delete(
    path_source: str, path_target: str, src_dirs: list[str]
) -> None:
    """Copie les fichiers présents sur la source dans les dossiers 'src_dirs'
    mais manquants dans les dossiers 'cible'.

    Supprime les fichiers présents sur la cible dans les dossiers
    'dir_targets' mais qui n'existent pas sur la source dans les
    dossiers 'dirs_source'
    """
    paths_src = build_paths(path_source, src_dirs)
    paths_target = build_paths(path_target, src_dirs)
   
    for i, path_src in enumerate(paths_src):
        src_files_name = files_names_list(path_src)
        target_files_name = files_names_list(paths_target[i])
        files_to_copy = diff_between_two_lists(
            src_files_name, target_files_name
        )
        files_to_delete = diff_between_two_lists(
            target_files_name, src_files_name
        )
        if files_to_copy:
            copy_or_update_files(files_to_copy, path_src, paths_target[i])
        if files_to_delete:
            if len(files_to_delete) > 1:
                msg = (
                    "Les fichiers suivants vont être supprimés du dossier"
                    " cible:\n"
                )
            else:
                msg = "Le fichier suivant va être supprimé du dossier cible:\n"
            sure_to_erase_or_update(files_to_delete, msg, paths_target[i])
            if continue_or_stop():
                delete_files(files_to_delete, paths_target[i])


def copy_or_update_files(
    files_to_copy: list[str], path_src: str, path_target: str
):
    for file in files_to_copy:
        try:
            shutil.copy2(
                os.path.join(path_src, file),
                os.path.join(path_target, file),
            )
        except OSError as err:
            error_msg(f"Une erreur s'est produite !! : {err}")


def delete_files(files_to_delete: list[str], paths_target: str):
    for file in files_to_delete:
        file_path = os.path.join(paths_target, file)
        os.remove(file_path) if os.path.exists(file_path) else error_msg(
            f"Le fichier '{file_path}' n'existe pas."
        )


def files_manager_update(
    path_source: str, path_target: str, src_dirs: list[str]
) -> None:
    """Mise à jour des fichiers cible n'ayant pas la même taille en octet que
    les fichiers source."""
    paths_src = build_paths(path_source, src_dirs)
    paths_target = build_paths(path_target, src_dirs)
    for i, path_src in enumerate(paths_src):
        dicts_src = files_sizes_list(path_src)
        dicts_target = files_sizes_list(paths_target[i])
        if dicts_src and dicts_target:
            files_to_update = [
                file
                for file in dicts_src
                if dicts_src.get(file) != dicts_target.get(file)
            ]
            if files_to_update:
                if len(files_to_update) > 1:
                    msg = "Les fichiers suivants vont être mise à jour\n"
                else:
                    msg = "Le fichier suivant va être mise à jour\n"
                sure_to_erase_or_update(files_to_update, msg, path_target)

                if continue_or_stop():
                    copy_or_update_files(
                        files_to_update, path_src, paths_target[i]
                    )


def sure_to_erase_or_update(
    items_to_delete: list[str], confirm_msg: str, path: str
) -> None:
    info_msg(f"{confirm_msg} {path}")
    display_list_of_items(items_to_delete)


def get_files_names_and_sizes(path: str) -> dict[str, dict[str, int]]:
    """retourne un dictionnaire contenant:
    clé: le chemin du dossier
    valeur: dictionnaire
                        clé : nom du fichier
                        valeur: taille du fichier
    {chemin du dossier racine : {nom du fichier : taille du fichier, ...}}"""

    dir_files_size = {}
    if os.path.exists(path):
        with os.scandir(path) as file:
            dir_files_size[path] = {
                elem.name: elem.stat().st_size
                for elem in file
                if elem.is_file()
            }
    return dir_files_size
