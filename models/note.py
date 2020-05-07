from .base_model import BaseModel
from peewee import CharField, ForeignKeyField
from .notebook import Notebook
import uuid
import os
from config import CONFIG
import re
import shutil


def generate_uuid():
    dir_uuid = str(uuid.uuid4())
    note_dir = os.path.join(CONFIG['app']['note_dir'], dir_uuid)
    os.makedirs(note_dir, exist_ok=True)
    open(os.path.join(note_dir, 'content.html'), 'w').close()
    open(os.path.join(note_dir, 'snippet.txt'), 'w').close()
    return dir_uuid


class Note(BaseModel):
    notebook = ForeignKeyField(Notebook, on_delete='cascade', backref='notes')
    uuid = CharField(default=generate_uuid)
    title = CharField(default="")

    @property
    def note_dir(self):
        return os.path.join(CONFIG['app']['note_dir'], self.uuid)

    @property
    def content_file(self):
        return os.path.join(self.note_dir, 'content.html')

    @property
    def snippet_file(self):
        return os.path.join(self.note_dir, 'snippet.txt')

    @property
    def snippet(self):
        with open(self.snippet_file, 'r', encoding='utf-8') as reader:
            return reader.read()

    @property
    def content(self):
        with open(self.content_file, 'r', encoding='utf-8') as reader:
            return reader.read()

    def set_content(self, content):
        with open(self.content_file, 'w', encoding='utf-8') as writer:
            writer.write(content)
        with open(self.snippet_file, 'w', encoding='utf-8') as writer:
            writer.write(re.sub(r'<.*?>','', content))
        self.save()

    def delete_instance(self, *args, **kwargs):
        shutil.rmtree(self.note_dir, ignore_errors=True)
        super().delete_instance(*args, **kwargs)
