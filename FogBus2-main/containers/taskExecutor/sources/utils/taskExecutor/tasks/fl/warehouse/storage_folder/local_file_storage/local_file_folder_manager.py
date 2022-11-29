import os
import inspect


class local_file_folder_manager:
    def __init__(self):
        pass

    @classmethod
    def folder_dir(cls):
        return os.path.dirname(inspect.getsourcefile(cls))
