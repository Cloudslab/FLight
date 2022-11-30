"""File that gives reference to folder position"""
import os
import inspect
from .ftp_file_storage import ftp_folder_manager
from .local_file_storage import local_file_folder_manager


class folder_position:
    @staticmethod
    def local_file_storage_folder():
        return local_file_folder_manager.local_file_folder_manager.folder_dir()

    @staticmethod
    def ftp_folder():
        return ftp_folder_manager.ftp_folder_manager.folder_dir()
