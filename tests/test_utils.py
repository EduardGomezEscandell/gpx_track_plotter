import pathlib
import os
import sys

class WorkFolderScope:
    """
    Modified version of the one found in

    https://github.com/KratosMultiphysics/Kratos/blob/master/kratos/python_scripts/KratosUnittest.py

    """
    def __init__(self, rel_path_work_folder: str, file_path: str, add_to_path: bool=False):
        self.currentPath = pathlib.Path(os.getcwd())
        self.add_to_path = add_to_path
        if self.add_to_path:
            self.currentPythonpath = pathlib.Path(sys.path)
        self.scope = pathlib.Path(os.path.realpath(file_path)).parent / rel_path_work_folder

    def __enter__(self):
        os.chdir(self.scope)
        if self.add_to_path:
            sys.path.append(self.scope)

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.currentPath)
        if self.add_to_path:
            sys.path.remove(self.scope)