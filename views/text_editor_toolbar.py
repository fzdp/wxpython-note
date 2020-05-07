import wx
import images
from .generic_bitmap_button import GenericBitmapButton


class _ToolColor(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self._init_ui()
        self.display_color('#000000')

    def _init_ui(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(GenericBitmapButton(self, 'tool_color'))
        self.color_indicator = wx.StaticLine(self, size=(-1, 2))
        self.main_sizer.Add(self.color_indicator, flag=wx.EXPAND)
        self.SetSizer(self.main_sizer)

    def display_color(self, color):
        self.color_indicator.SetBackgroundColour(color)


class TextEditorToolbar(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.editor = parent
        self._init_ui()
        self._init_event()

    def _init_ui(self):
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.tool_font_name = wx.Choice(self, choices=['Helvetica', 'Arial', 'sans-serif'])
        self.tool_font_size = wx.Choice(self, choices=['12', '13', '14', '16', '18', '24', '36', '48', '72'])
        self.tool_bold = GenericBitmapButton(self, 'tool_bold')
        self.tool_color = _ToolColor(self)
        self.tool_background = GenericBitmapButton(self, 'tool_background')
        self.tool_code_block = GenericBitmapButton(self, 'tool_code_block')

        self.main_sizer.AddSpacer(2)
        self.main_sizer.Add(self.tool_font_name, flag=wx.RIGHT, border=5)
        self.main_sizer.Add(self.tool_font_size, flag=wx.RIGHT, border=5)
        self.main_sizer.Add(self.tool_bold, flag=wx.RIGHT, border=5)
        self.main_sizer.Add(self.tool_color, flag=wx.RIGHT, border=5)
        self.main_sizer.Add(self.tool_background, flag=wx.RIGHT, border=5)
        self.main_sizer.Add(self.tool_code_block, flag=wx.RIGHT, border=5)

        self.SetSizer(self.main_sizer)

    def _init_event(self):
        self.tool_font_name.Bind(wx.EVT_CHOICE, self._on_font_name_selected)
        self.tool_font_size.Bind(wx.EVT_CHOICE, self._on_font_size_selected)
        self.tool_bold.Bind(wx.EVT_BUTTON, self._on_bold_clicked)
        self.tool_color.Bind(wx.EVT_BUTTON, self._on_fg_color_clicked)
        self.tool_background.Bind(wx.EVT_BUTTON, self._on_bg_color_clicked)
        self.tool_code_block.Bind(wx.EVT_BUTTON, self._on_code_block_clicked)

    def _on_font_name_selected(self, e):
        self.editor.format_content('font', e.String)

    def _on_font_size_selected(self, e):
        self.editor.format_content('size', f'{e.String}px')

    def _on_bold_clicked(self, e):
        format_val = not self.editor.content_format['bold']
        self.editor.format_content('bold', format_val)
        self._display_bold_format(format_val)

    def _on_fg_color_clicked(self, e):
        color = wx.GetColourFromUser(self, self.editor.content_format['color'] or '#000000').GetAsString(wx.C2S_HTML_SYNTAX)
        self.editor.format_content('color', color)
        self._display_color_format(color)

    def _on_bg_color_clicked(self, e):
        color = wx.GetColourFromUser(self, self.editor.content_format['background'] or '#ffffff').GetAsString(wx.C2S_HTML_SYNTAX)
        self.editor.format_content('background', color)
        self._display_background_format(color)

    def _on_code_block_clicked(self, e):
        format_val = not self.editor.content_format['code-block']
        self.editor.format_content('code-block',format_val)
        self._display_code_block_format(format_val)

    def _display_bold_format(self, format_val):
        bitmap = images.tool_bold_active.Bitmap if format_val else images.tool_bold.Bitmap
        self.tool_bold.SetBitmap(bitmap)

    def _display_code_block_format(self, format_val):
        bitmap = images.tool_code_block_active.Bitmap if format_val else images.tool_code_block.Bitmap
        self.tool_code_block.SetBitmap(bitmap)

    def _display_font_format(self, format_val):
        if format_val is False:
            index = 0
        elif format_val in self.tool_font_name.GetItems():
            index = self.tool_font_name.GetItems().index(format_val)
        else:
            index = self.tool_font_name.Append(format_val)
        self.tool_font_name.SetSelection(index)

    def _display_size_format(self, format_val):
        if format_val is False or format_val not in self.tool_font_size.GetItems():
            index = 0
        else:
            index = self.tool_font_size.GetItems().index(format_val[:-2])
        self.tool_font_size.SetSelection(index)

    def _display_color_format(self, color):
        self.tool_color.display_color(color or '#000000')

    def _display_background_format(self, color):
        self.tool_background.SetBackgroundColour(color or '#ffffff')
        self.tool_background.Refresh()

    def display_format(self, changed_format):
        if 'bold' in changed_format:
            self._display_bold_format(changed_format.pop('bold'))
        if 'font' in changed_format:
            self._display_font_format(changed_format.pop('font'))
        if 'size' in changed_format:
            self._display_size_format(changed_format.pop('size'))
        if 'color' in changed_format:
            self._display_color_format(changed_format.pop('color'))
        if 'background' in changed_format:
            self._display_background_format(changed_format.pop('background'))
        if 'code-block' in changed_format:
            self._display_code_block_format(changed_format.pop('code-block'))
