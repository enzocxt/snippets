import os

from models import Model
from utils import log


class Upload(Model):
    def __init__(self, form):
        self.title = form.get('title', '')

    @classmethod
    def db_path(cls):
        """
        overwrite classmethod of Model
        :return:
        """
        path = 'static/uploads/'
        return path

    @classmethod
    def all(cls):
        path = cls.db_path()
        files = os.listdir(path)
        uploads = []
        for f in files:
            if f.startswith('.'):
                continue
            p = path + f
            if os.path.isfile(p):
                uploads.append(f)
        return uploads

    @classmethod
    def find_all(cls):
        all = cls.all()
        return all

    def save(self):
        pass
