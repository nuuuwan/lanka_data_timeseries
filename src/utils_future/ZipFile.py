import zipfile

from utils import Log

log = Log(__name__)


class ZipFile:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extractall(self, dir_path: str):
        with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
            zip_ref.extractall(dir_path)
        log.debug(f'Extracted {self.file_path} to {dir_path}')
