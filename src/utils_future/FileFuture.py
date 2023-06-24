import os

from utils import File


class FileFuture(File):
    def start(self):
        os.startfile(self.path)
