from peewee import Model, DateTimeField, SqliteDatabase
import datetime
from config import CONFIG


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)

    class Meta:
        database = SqliteDatabase(CONFIG['database']['db_file'],pragmas={'foreign_keys': 1})
