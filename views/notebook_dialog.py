import wx


class NotebookDialog(wx.Dialog):
    def __init__(self, parent, notebook=None):
        title = '编辑笔记本' if notebook else '新建笔记本'
        super().__init__(parent, title=title)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        g_sizer = wx.FlexGridSizer(cols=2,gap=(10, 10))
        g_sizer.AddGrowableCol(1)

        g_sizer.Add(wx.StaticText(self, label='名称'))
        self.tc_name = wx.TextCtrl(self, size=(400,-1))
        g_sizer.Add(self.tc_name, flag=wx.EXPAND)

        g_sizer.Add(wx.StaticText(self, label='描述'))
        self.tc_description = wx.TextCtrl(self, size=(400, 160),style=wx.TE_MULTILINE)
        g_sizer.Add(self.tc_description, flag=wx.EXPAND)

        main_sizer.Add(g_sizer, flag=wx.EXPAND|wx.ALL, border=10)

        btn_sizer = wx.StdDialogButtonSizer()
        btn_sizer.AddButton(wx.Button(self, wx.ID_CANCEL, '取消'))
        ok_button = wx.Button(self, wx.ID_OK, '确定')
        ok_button.SetDefault()

        btn_sizer.AddButton(ok_button)
        btn_sizer.Realize()
        main_sizer.Add(btn_sizer, flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, border=5)

        if notebook:
            self.tc_name.SetValue(notebook.name)
            self.tc_description.SetValue(notebook.description)
            self.tc_name.SelectAll()

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

        self.CenterOnScreen()
        self.Bind(wx.EVT_BUTTON, self._on_save, id=wx.ID_OK)

    def get_name(self):
        return self.tc_name.GetValue().strip()

    def get_description(self):
        return self.tc_description.GetValue().strip()

    def _on_save(self, e):
        if self.get_name():
            self.EndModal(wx.ID_OK)
