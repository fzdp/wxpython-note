import wx
from .note_tree import NoteTree
import images
from pubsub import pub
from models import Note


class NavPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        v_sizer = wx.BoxSizer(wx.VERTICAL)

        self.btn_new_note = wx.Button(self,style=wx.NO_BORDER)
        self.btn_new_note.SetBitmap(images.add_note.Bitmap)
        self.btn_new_note.SetLabelMarkup('<span fgcolor="white" weight="bold" size="large">  新建笔记</span>')

        v_sizer.Add(self.btn_new_note, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
        v_sizer.AddSpacer(20)
        self.note_tree = NoteTree(self)
        v_sizer.Add(self.note_tree, proportion=1,flag=wx.EXPAND)
        self.SetSizer(v_sizer)

        self.SetBackgroundColour("#2a2a2a")
        self.btn_new_note.Bind(wx.EVT_BUTTON, self._create_note)

    def _create_note(self, _):
        if self.note_tree.notebook_id:
            note = Note.create(notebook_id=self.note_tree.notebook_id)
            pub.sendMessage('note.created', note=note)
