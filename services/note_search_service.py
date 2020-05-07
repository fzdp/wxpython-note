from whoosh.fields import NUMERIC, TEXT, Schema
from whoosh.qparser import MultifieldParser
from whoosh import query
import whoosh.index
from jieba.analyse import ChineseAnalyzer
from config import CONFIG


class NoteSearchService:
    def __init__(self):
        if whoosh.index.exists_in(CONFIG['app']['index_dir']):
            self.index = whoosh.index.open_dir(CONFIG['app']['index_dir'])
        else:
            chinese_analyzer = ChineseAnalyzer()
            schema = Schema(note_id=NUMERIC(stored=True, unique=True),
                            notebook_id=NUMERIC(stored=True),
                            title=TEXT(analyzer=chinese_analyzer),
                            snippet=TEXT(analyzer=chinese_analyzer))
            self.index = whoosh.index.create_in(CONFIG['app']['index_dir'], schema)

    def add_doc(self, note):
        with self.index.writer() as writer:
            writer.add_document(**self._get_fields(note))

    def update_doc(self, note):
        with self.index.writer() as writer:
            writer.update_document(**self._get_fields(note))

    def delete_doc(self, note):
        self.index.delete_by_term('note_id', note.id)

    def search(self, keyword, notebook_id=None):
        with self.index.searcher() as searcher:
            query_parser = MultifieldParser(["title", "snippet"], schema=self.index.schema).parse(keyword)
            notebook_filter = query.Term("notebook_id", notebook_id) if notebook_id else None
            results = searcher.search(query_parser, filter=notebook_filter, limit=None)
            return [res['note_id'] for res in results]

    @staticmethod
    def _get_fields(note):
        return {'note_id': note.id, 'notebook_id': note.notebook_id, 'title': note.title, 'snippet': note.snippet}
