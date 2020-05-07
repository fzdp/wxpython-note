from peewee import CharField, ForeignKeyField
from .base_model import BaseModel
import shutil


class Notebook(BaseModel):
    parent = ForeignKeyField('self', null=True, on_delete='cascade', backref='notebooks')
    name = CharField()
    description = CharField(default="")

    def delete_instance(self, *args, **kwargs):
        for note in self.notes:
            shutil.rmtree(note.note_dir, ignore_errors=True)
        super().delete_instance(*args, **kwargs)
