import os
import csv

from models import Model
from utils import log

import pandas as pd
import numpy as np


def load_books(path):
    xls = pd.ExcelFile(path)
    sheet_name = xls.sheet_names[0]
    df = xls.parse(sheet_name)
    df = df[np.isfinite(df['编号'])]
    return df


class Book(Model):
    def __init__(self, form):
        self.id = int(form.get('编号', -1))
        self.name = form.get('标题', 'NaN')
        self.author = form.get('作者', 'NaN')
        self.date = form.get('出版时间', 'NaN')
        self.detail = form
        self.headers = form.keys()

    @classmethod
    def new(cls, form):
        b = cls(form)
        return b

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.xls'.format(classname)
        return path

    @classmethod
    def all(cls):
        path = cls.db_path()
        books = load_books(path)
        bs = []
        for _idx, row in books.iterrows():
            info_dict = row.to_dict()
            bs.append(cls.new(info_dict))
        return bs

    @classmethod
    def find_all(cls):
        all = cls.all()
        return all

    def save(self):
        pass


if __name__ == '__main__':
    books = Book.find_all()
    print(books[0])
