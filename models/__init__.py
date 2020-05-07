from .base_model import BaseModel
from .notebook import Notebook
from .note import Note


def create_tables():
    db = BaseModel._meta.database
    if not db.get_tables():
        db.create_tables([Notebook, Note])
    if not Notebook.select().count():
        Notebook.create(name='默认笔记本', description='系统创建的默认笔记本')
