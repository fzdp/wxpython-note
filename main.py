import wx
from views import MainFrame
from models import create_tables


class NoteApp(wx.App):
    def OnInit(self):
        create_tables()
        MainFrame().Show()
        return True


if __name__ == "__main__":
    app = NoteApp()
    app.MainLoop()
