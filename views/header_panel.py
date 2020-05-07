import wx
from .generic_bitmap_button import GenericBitmapButton
from functools import partial
from models import Note
from pubsub import pub


class HeaderPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_NONE)
        self._sort_menu_ids = wx.NewIdRef(6)
        self._checked_menu_id = self._sort_menu_ids[0]
        self._rename_notebook_menu_id = wx.NewIdRef()
        self._delete_notebook_menu_id = wx.NewIdRef()
        self._global_search_menu_id = wx.NewIdRef()
        self.is_global_search = False
        self.note_count = 0
        self.sort_option = Note.updated_at.desc()
        self._init_ui()
        self._init_event()

    def _init_ui(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.st_notebook_name = wx.StaticText(self, label='所有笔记')
        self.main_sizer.Add(self.st_notebook_name, flag=wx.ALL, border=10)

        self._build_note_actions()
        self._build_search_bar()
        self.main_sizer.AddSpacer(10)
        self.SetSizer(self.main_sizer)

        self.SetBackgroundColour("#ebebeb")

    def _init_event(self):
        self.btn_display_order_options.Bind(wx.EVT_BUTTON, self._show_sort_menu)
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.updated_at.desc()), id=self._sort_menu_ids[0])
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.updated_at.asc()), id=self._sort_menu_ids[1])
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.created_at.desc()), id=self._sort_menu_ids[2])
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.created_at.asc()), id=self._sort_menu_ids[3])
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.title.desc()), id=self._sort_menu_ids[4])
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.title.asc()), id=self._sort_menu_ids[5])
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.title.asc()), id=self._sort_menu_ids[5])

        self.btn_display_notebook_options.Bind(wx.EVT_BUTTON, self._show_action_menu)
        self.Bind(wx.EVT_MENU, lambda _: pub.sendMessage('notebook.editing'), id=self._rename_notebook_menu_id)
        self.Bind(wx.EVT_MENU, lambda _: pub.sendMessage('notebook.deleting'), id=self._delete_notebook_menu_id)
        self.search_bar.Bind(wx.EVT_TEXT, self._on_searching)
        self.Bind(wx.EVT_MENU, self._on_global_search_menu_checked, id=self._global_search_menu_id)

    def _on_note_sorting(self, e, sort_param):
        if self._checked_menu_id != e.GetId():
            self._checked_menu_id = e.GetId()
            self.sort_option = sort_param
            pub.sendMessage('note.sorting', sort_param=sort_param)

    def _build_sort_menu(self):
        menu = wx.Menu()

        sub_menu1 = wx.Menu()
        sub_menu1.AppendCheckItem(self._sort_menu_ids[0], '最新到最旧')
        sub_menu1.AppendCheckItem(self._sort_menu_ids[1], '最旧到最新')
        menu.AppendSubMenu(sub_menu1, '按更新时间')

        sub_menu2 = wx.Menu()
        sub_menu2.AppendCheckItem(self._sort_menu_ids[2], '最新到最旧')
        sub_menu2.AppendCheckItem(self._sort_menu_ids[3], '最旧到最新')
        menu.AppendSubMenu(sub_menu2, '按创建时间')

        sub_menu3 = wx.Menu()
        sub_menu3.AppendCheckItem(self._sort_menu_ids[4], '逆字母排序')
        sub_menu3.AppendCheckItem(self._sort_menu_ids[5], '字母排序')
        menu.AppendSubMenu(sub_menu3, '按标题')

        return menu

    def _show_sort_menu(self, _):
        menu = self._build_sort_menu()
        menu.Check(self._checked_menu_id, True)
        self.PopupMenu(menu)
        menu.Destroy()

    def _show_action_menu(self, _):
        menu = self._build_action_menu()
        self.PopupMenu(menu)
        menu.Destroy()

    def _build_action_menu(self):
        menu = wx.Menu()
        menu.Append(self._rename_notebook_menu_id, '重命名笔记本...')
        menu.Append(self._delete_notebook_menu_id, '删除笔记本...')
        return menu

    def _build_note_actions(self):
        note_action_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.st_note_count = wx.StaticText(self, label="0条笔记")
        note_action_sizer.Add(self.st_note_count)

        note_action_sizer.AddStretchSpacer()

        self.btn_display_order_options = GenericBitmapButton(self, 'sort')
        note_action_sizer.Add(self.btn_display_order_options)

        self.btn_display_notebook_options = GenericBitmapButton(self, 'more')
        note_action_sizer.Add(self.btn_display_notebook_options,flag=wx.LEFT,border=10)

        self.main_sizer.Add(note_action_sizer, flag=wx.ALL|wx.EXPAND, border=10)

    def _build_search_bar(self):
        self.search_bar = wx.SearchCtrl(self,style=wx.TE_PROCESS_ENTER)
        self.search_bar.ShowCancelButton(True)
        self._build_search_bar_menu()
        self.main_sizer.Add(self.search_bar, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=8)

    def _on_searching(self, e):
        pub.sendMessage('note.searching', keyword=self.keyword, is_global_search=self.is_global_search)

    def _on_global_search_menu_checked(self, e):
        self.is_global_search = e.IsChecked()
        self._build_search_bar_menu()
        if self.keyword:
            pub.sendMessage('note.searching', keyword=self.keyword, is_global_search=self.is_global_search)

    def _build_search_bar_menu(self):
        menu = wx.Menu()
        menu.AppendCheckItem(self._global_search_menu_id, '搜索所有笔记本').Check(self.is_global_search)
        self.search_bar.SetMenu(menu)
        if self.is_global_search:
            self.search_bar.SetHint('搜索所有笔记本')
        else:
            self.search_bar.SetHint('搜索当前笔记本')

    def set_title(self, title):
        self.st_notebook_name.SetLabel(title)

    def set_count(self, count):
        self.note_count = count
        if self.keyword:
            self.st_note_count.SetLabel(f'找到{self.note_count}条笔记')
        else:
            self.st_note_count.SetLabel(f'{self.note_count}条笔记')

    def change_count(self, changed_count):
        self.note_count += changed_count
        self.st_note_count.SetLabel(f'{self.note_count}条笔记')

    def reset_search_bar(self):
        self.search_bar.ChangeValue('')

    @property
    def keyword(self):
        return self.search_bar.GetValue().strip()
