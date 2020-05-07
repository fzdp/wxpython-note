import wx
from cefpython3 import cefpython as cef
import sys


class Webview(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_NONE)
        self._init_cef()
        self._init_browser()
        self._init_event()

    def _init_cef(self):
        sys.excepthook = cef.ExceptHook
        settings = {}
        if wx.Platform == "__WXMAC__":
            settings['external_message_pump'] = True
        if wx.Platform == "__WXMSW__":
            cef.DpiAware.EnableHighDpiSupport()
        if wx.Platform == "__WXGTK__":
            cef.WindowUtils.InstallX11ErrorHandlers()
        if wx.Platform == "__WXMSW__":
            wx.CallAfter(self._fix_keyboard)
        cef.Initialize(settings=settings)

    def _init_browser(self):
        window_info = cef.WindowInfo()
        (width, height) = self.GetClientSize().Get()
        window_info.SetAsChild(self.GetHandle(), [0,0,width,height])
        self.browser = cef.CreateBrowserSync(window_info)

    def _init_event(self):
        self.Bind(wx.EVT_CLOSE, self._on_close)
        self.Bind(wx.EVT_SIZE, self._on_size)
        self.Bind(wx.EVT_SET_FOCUS, self._on_set_focus)

        self.timer = wx.Timer(self)
        self.timer.Start(10)
        self.Bind(wx.EVT_TIMER, self._on_timer, self.timer)

    def _fix_keyboard(self):
        ctrl = self
        while ctrl:
            ctrl.SetWindowStyle(ctrl.GetWindowStyle() & ~wx.TAB_TRAVERSAL)
            ctrl = ctrl.GetParent()

    def _on_set_focus(self, _):
        if wx.Platform == "__WXMSW__":
            cef.WindowUtils.OnSetFocus(self.GetHandle(),0, 0, 0)
        self.browser.SetFocus(True)

    def _on_size(self, _):
        if wx.Platform == "__WXMSW__":
            cef.WindowUtils.OnSize(self.GetHandle(),0, 0, 0)
        self.browser.NotifyMoveOrResizeStarted()

    def _on_timer(self, _):
        cef.MessageLoopWork()

    def _on_close(self, e):
        if wx.Platform == "__WXMAC__":
            self.browser.CloseBrowser()
            self.browser = None
            self.Destroy()
            cef.Shutdown()
        else:
            self.browser.ParentWindowWillClose()
            e.Skip()
            self.browser = None

    def load_url(self, url):
        self.browser.LoadUrl(url)

    def run_js(self, str_function, *param):
        self.browser.ExecuteFunction(str_function, *param)

    def set_js_bindings(self, bindings):
        js_bindings = cef.JavascriptBindings()
        for binding_item in bindings:
            js_bindings.SetFunction(binding_item[0], binding_item[1])
        self.browser.SetJavascriptBindings(js_bindings)