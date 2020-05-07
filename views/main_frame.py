import wx
import wx.aui
from .nav_panel import NavPanel
from .list_panel import ListPanel
from .text_editor import TextEditor
from pubsub import pub
from .notebook_dialog import NotebookDialog


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='UltraNote',size=(800,600))
        self.aui_manager = wx.aui.AuiManager(self,wx.aui.AUI_MGR_TRANSPARENT_HINT)

        self.nav_panel = NavPanel(self)
        self.list_panel = ListPanel(self)
        self.detail_panel = TextEditor(self)

        self.aui_manager.AddPane(self.nav_panel, self._get_default_pane_info().Left().Row(0).BestSize(300,-1))
        self.aui_manager.AddPane(self.list_panel, self._get_default_pane_info().Left().Row(1).BestSize(250, -1).MinSize(150,-1))
        self.aui_manager.AddPane(self.detail_panel, self._get_default_pane_info().CenterPane().Position(0).BestSize(400,-1))

        self.aui_manager.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_SASH_SIZE, 1)
        self.aui_manager.Update()

        self.Maximize(True)
        self._register_listeners()

    def _get_default_pane_info(self):
        return wx.aui.AuiPaneInfo().CaptionVisible(False).PaneBorder(False).CloseButton(False).PinButton(False).Gripper(
            False)

    def on_frame_closing(self, e):
        self.aui_manager.UnInit()
        del self.aui_manager
        self.Destroy()

    def _register_listeners(self):
        self.Bind(wx.EVT_CLOSE, self.on_frame_closing)
        pub.subscribe(self._on_notebook_editing, 'notebook.editing')
        pub.subscribe(self._on_notebook_deleting, 'notebook.deleting')

    def _on_notebook_deleting(self):
        dialog = wx.MessageDialog(self, '此笔记本中的任何笔记都将被删除，这个操作不能恢复。', '确定要删除吗？',style=wx.OK|wx.CANCEL|wx.CANCEL_DEFAULT)
        dialog.SetOKCancelLabels('确定', '取消')

        if dialog.ShowModal() == wx.ID_OK:
            self.nav_panel.note_tree.delete_selection()

    def _on_notebook_editing(self):
        notebook = self.nav_panel.note_tree.notebook
        with NotebookDialog(self, notebook) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                notebook.name = dialog.get_name()
                notebook.description = dialog.get_description()
                notebook.save()

                self.nav_panel.note_tree.set_text(notebook.name)
                self.list_panel.header_panel.set_title(notebook.name)