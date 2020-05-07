import wx
from pubsub import pub
from models import Note


class NotePreviewPanel(wx.Panel):
    def __init__(self, parent, note):
        super().__init__(parent, size=(-1, 110), style=wx.BORDER_NONE, name=f"preview_{note.id}")
        self.note_id = note.id
        self._init_ui(note)
        self._init_context_menu()
        self._init_event()

    def _init_ui(self, note):
        v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.st_note_title = wx.StaticText(self, style=wx.ST_ELLIPSIZE_END)
        self.st_note_preview = wx.StaticText(self, style=wx.ST_ELLIPSIZE_END)
        self.st_note_date = wx.StaticText(self, label=note.updated_at.strftime('%Y-%m-%d'))

        self.st_note_title.SetFont(wx.Font(wx.FontInfo(14).Bold()))
        self.st_note_preview.SetFont(wx.Font(wx.FontInfo(14).Light()))
        self.st_note_preview.SetForegroundColour('#4e4e4e')
        self.st_note_date.SetForegroundColour('#4e4e4e')

        v_sizer.Add(self.st_note_title, flag=wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)
        v_sizer.AddSpacer(15)
        v_sizer.Add(self.st_note_preview, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)
        v_sizer.AddStretchSpacer(1)
        v_sizer.Add(self.st_note_date, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        self.st_note_title.SetLabel(note.title or '无标题')
        self.st_note_preview.SetLabel(note.snippet)

        line = wx.StaticLine(self, size=(-1, 1))
        line.SetBackgroundColour("#cbcbcb")
        v_sizer.Add(line, flag=wx.EXPAND)

        self.SetSizer(v_sizer)

    def _init_context_menu(self):
        self._menu_id_delete_note = wx.NewIdRef()
        self._context_menu = wx.Menu()
        self._context_menu.Append(self._menu_id_delete_note, '删除笔记')

    def _show_context_menu(self, _):
        self.PopupMenu(self._context_menu)

    def _init_event(self):
        self.Bind(wx.EVT_LEFT_UP, self._on_left_clicked)
        self.Bind(wx.EVT_CONTEXT_MENU, self._show_context_menu)
        self.Bind(wx.EVT_MENU, self._delete_note, self._menu_id_delete_note)

    def _delete_note(self, _):
        pub.sendMessage('note.deleting', note=Note.get_by_id(self.note_id))

    def update(self, note):
        self.st_note_title.SetLabel(note.title or '无标题')
        self.st_note_preview.SetLabel(note.snippet)
        self.st_note_date.SetLabel(note.updated_at.strftime('%Y-%m-%d'))

    def _on_left_clicked(self, _):
        pub.sendMessage('note.clicked', note=Note.get_by_id(self.note_id))

    def focus(self, enable_focus=True):
        if enable_focus:
            self.SetBackgroundColour('#dbdbdb')
        else:
            self.SetBackgroundColour('#ffffff')
        self.Refresh()
