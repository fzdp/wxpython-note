import wx
from .header_panel import HeaderPanel
from .note_list_panel import NoteListPanel
from pubsub import pub
from models import Note
from services.note_search_service import NoteSearchService


class ListPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_NONE)
        self._init_ui()
        self._note_ids = []
        self._notebook = None
        self.searcher = NoteSearchService()
        pub.subscribe(self._on_notebook_selected, 'notebook.selected')
        pub.subscribe(self._on_root_selected, 'root.selected')
        pub.subscribe(self._on_note_created, 'note.created')
        pub.subscribe(self._on_note_updated, 'note.updated')
        pub.subscribe(self._on_note_deleting, 'note.deleting')
        pub.subscribe(self._on_note_sorting, 'note.sorting')
        pub.subscribe(self._on_note_searching, 'note.searching')

    def _init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header_panel = HeaderPanel(self)
        main_sizer.Add(self.header_panel,flag=wx.EXPAND)

        self.note_list_panel = NoteListPanel(self)
        main_sizer.Add(self.note_list_panel,flag=wx.EXPAND,proportion=1)

        self.SetSizer(main_sizer)

    def _on_note_created(self, note):
        self.header_panel.change_count(1)
        self.note_list_panel.prepend(note)
        self.note_list_panel.select(note)
        self._note_ids.insert(0, note.id)
        self.searcher.add_doc(note)

    def _on_note_searching(self, keyword, is_global_search):
        if keyword:
            if is_global_search or not self._notebook:
                notebook_id = None
            else:
                notebook_id = self._notebook.id
            note_ids = self.searcher.search(keyword, notebook_id=notebook_id)
            if note_ids:
                notes = list(Note.select().where(Note.id.in_(note_ids)).order_by(self.header_panel.sort_option))
            else:
                notes = []
            self._load(notes, keyword=keyword)
            self.header_panel.set_count(len(notes))
        else:
            if self._notebook:
                self._on_notebook_selected(self._notebook)
            else:
                self._on_root_selected()

    def _load(self, notes, preserve_select=False, keyword=None):
        if len(notes):
            self.note_list_panel.replace(notes, preserve_select, keyword)
        else:
            self.note_list_panel.clear()
        self._note_ids = list(map(lambda note: note.id, notes))

    def _on_notebook_selected(self, notebook):
        self._notebook = notebook
        notes = list(notebook.notes.order_by(self.header_panel.sort_option))
        self.header_panel.set_title(notebook.name)
        self.header_panel.set_count(len(notes))
        self.header_panel.reset_search_bar()
        self._load(notes)

    def _on_root_selected(self):
        self._notebook = None
        notes = list(Note.select().order_by(self.header_panel.sort_option))
        self.header_panel.set_title('所有笔记')
        self.header_panel.set_count(len(notes))
        self.header_panel.reset_search_bar()
        self._load(notes)

    def _on_note_updated(self, note):
        self.searcher.update_doc(note)

    def _on_note_deleting(self, note):
        self.searcher.delete_doc(note)
        note.delete_instance()
        self.note_list_panel.remove(note)
        if len(self._note_ids) > 1:
            note_id_index = self._note_ids.index(note.id)
            next_index = note_id_index + 1
            if next_index > len(self._note_ids) - 1:
                next_index = note_id_index - 1
            self.note_list_panel.select(Note.get_by_id(self._note_ids[next_index]))
        self._note_ids.remove(note.id)
        self.header_panel.change_count(-1)

    def _on_note_sorting(self, sort_param):
        notes = list(Note.select().where(Note.id.in_(self._note_ids)).order_by(sort_param))
        self._load(notes, preserve_select=True)
