import os
import pathlib
import shutil
from backup.in_out import error_msg


def get_last_folder(path: str) -> str:
    """Retourne le dernier dossier d'un chemin."""
    return pathlib.PurePath(path).name
    # return os.path.basename(os.path.normpath(path))


def get_dir_list(path: str, root_folder: str) -> list[str]:
    """Retourne la liste des chemins des dossiers et des sous-dossiers à partir
    du répertoire racine."""
    dirs_list = []
    try:
        for element in pathlib.Path(path).iterdir():
            if element.is_dir():
                dirs_list.append(str(element).split(root_folder)[1][1:])
                folders = get_dir_list(element, root_folder)
                if folders:
                    dirs_list.extend(folders)
        return dirs_list
    except FileNotFoundError:
        error_msg(f"Le chemin '{path}' n'est pas valide.")


# def get_dir_list(path: str, root_folder: str) -> list[str]:
#     """Retourne la liste des chemins des dossiers et des sous-dossiers à partir
#     du répertoire racine."""
#     dirs_list = []
#     try:
#         with os.scandir(path) as dir:
#             for element in dir:
#                 if element.is_dir():
#                     dirs_list.append(element.path.split(root_folder)[1][1:])
#                     folders = get_dir_list(element.path, root_folder)
#                     if folders:
#                         dirs_list.extend(folders)
#         return dirs_list
#     except FileNotFoundError:
#         error_msg(f"Le message '{path}' n'est pas valide.")


def diff_between_two_lists(list_1: list, list_2: list) -> list:
    """Retourne les éléments présents dans list_1 mais pas dans list_2."""
    return [el for el in list_1 if el not in list_2]


def create_folders(folders: list, path: str):
    """Création de la liste de dossiers passée en paramètre."""
    for folder in folders:
        dir = pathlib.PurePosixPath(path).joinpath(folder)
        pathlib.Path(dir).mkdir(exist_ok=True)
        # os.makedirs(os.path.join(path, folder), exist_ok=True)


def remove_subfolders_paths(path_folders: list):
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


def delete_folders(folders: list, path: str):
    """Supprime une liste de dossiers, des sous-dossiers et des fichiers qu'ils
    contiennent."""
    for folder in remove_subfolders_paths(folders):
        try:
            shutil.rmtree(os.path.join(path, folder))
        except OSError as error:
            error_msg(error)


def files_names_list(path_dir: str) -> list[str]:
    """Retourne la liste des fichiers contenus dans le dossier passé en
    paramètre."""
    return list(get_files_names_and_sizes(path_dir).get(path_dir).keys())


def files_sizes_list(path_dir: str) -> dict[str:str]:
    """Retourne un dict nom du fichier: taille des fichiers contenus dans le
    dossier passé en paramètre."""
    return get_files_names_and_sizes(path_dir).get(path_dir)


def directories_manager_create_delete(src_dirs_list, target_dirs_list, path_target):
    """Création des dossiers manquants sur la cible et suppression des dossiers
    présents sur la cible mais pas sur la source."""
    missing_folders = diff_between_two_lists(src_dirs_list, target_dirs_list)
    excess_folders = diff_between_two_lists(target_dirs_list, src_dirs_list)
    print('missing', missing_folders)
    print('excess', excess_folders)
    # if missing_folders:
    #     create_folders(missing_folders, path_target)
    # if excess_folders:
    #     delete_folders(excess_folders, path_target)


def build_paths(root_path: str, folders: list) -> list:
    """Retourne la list des chemins complets de toute l'arborescence."""
    paths = [os.path.join(root_path, dir) for dir in folders]
    paths[0] = root_path
    return paths


def files_manager_copy_delete(path_source, path_target, src_dirs):
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
            src_files_name, target_files_name)
        files_to_delete = diff_between_two_lists(
            target_files_name, src_files_name)
        if files_to_copy:
            for file in files_to_copy:
                try:
                    shutil.copy2(os.path.join(path_src, file),
                                 os.path.join(paths_target[i], file))
                except Exception as err:
                    error_msg(f"Une erreur s'est produite : {err}")
        if files_to_delete:
            for file in files_to_delete:
                file_path = os.path.join(paths_target[i], file)
                os.remove(file_path) if os.path.exists(file_path) else error_msg(
                    f"Le fichier '{file_path}' n'existe pas.")


def files_manager_update(path_source, path_target, src_dirs):
    """Mise à jour des fichiers cible n'ayant pas la même taille en octet que
    les fichiers source."""
    paths_src = build_paths(path_source, src_dirs)
    paths_target = build_paths(path_target, src_dirs)
    for i, path_src in enumerate(paths_src):
        dicts_src = files_sizes_list(path_src)
        dicts_target = files_sizes_list(paths_target[i])
        files_to_update = [file for file in dicts_src if dicts_src.get(
            file) != dicts_target.get(file)]
        if files_to_update:
            for file in files_to_update:
                try:
                    shutil.copy2(os.path.join(path_src, file),
                                 os.path.join(paths_target[i], file))
                except Exception as err:
                    error_msg(f"Une erreur s'est produite : {err}")


def get_files_names_and_sizes(path: str) -> dict[str:dict[str:str]]:
    """ retourne un dictionnaire contenant:
        clé: le chemin du dossier
        valeur: dictionnaire
                            clé : nom du fichier
                            valeur: taille du fichier"""
    dir_files_size = {}
    with os.scandir(path) as file:
        dir_files_size[path] = {elem.name: elem.stat().st_size
                                for elem in file if elem.is_file()}
    return dir_files_size
