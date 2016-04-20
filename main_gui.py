# _*_ coding:utf-8 _*_

from multiprocessing import Process, freeze_support, Queue, Manager
import os
import sys

import wx
import wx.lib.inspection

import widgets

from niczy_client import Niczy, mp_downloader


class Frame(wx.Frame):

    def __init__(self, parent, id, title, pos, size, style, name,
                 process, queue, _dict, client):

        super(Frame, self).__init__(parent, id, title, pos, size, style, name)

        url_input = widgets.DownloadBar(self, "url_input", queue, _dict, client)
        video_item = widgets.VideoItem(self, "video_item", queue, _dict, client)
        ad_poster = widgets.ADPoster(self, "ad_poster", _dict)
        contact_author = widgets.TopBar(self, "top_bar")
        self.m_sizer = wx.BoxSizer(wx.VERTICAL)

        self.m_sizer.AddMany([(contact_author, 0, wx.EXPAND),
                                (url_input, 0, wx.ALL | wx.EXPAND, 5),
                              (video_item, 1, wx.ALL | wx.EXPAND, 5),
                              (ad_poster, 1, wx.ALL | wx.EXPAND, 5)])

        self.SetSizer(self.m_sizer)

        self._set_icon()

    def _set_icon(self, ):
        icon = wx.Icon("dgut_video.ico")
        self.SetIcon(icon)


class App(wx.App):

    def __init__(self, redirect=True, filename=None, useBestVisual=False, clearSigInt=True,
                 process=None, queue=None, _dict=None, client=None):
        
        self.process = process
        self.queue = queue
        self._dict = _dict
        self.client = client

        super(App, self).__init__(
            redirect, filename, useBestVisual, clearSigInt)
        
    def OnInit(self, ):
        self.frame = Frame(None, wx.ID_ANY, u"Niczy下载器", wx.DefaultPosition,
                           (800, 400), wx.DEFAULT_FRAME_STYLE, "frame",
                           self.process, self.queue, self._dict, self.client)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        self.frame.Center()
        
        wx.lib.inspection.InspectionTool().Show()
        return True

    

# Module multiprocessing is organized differently in Python 3.4+
try:
    # Python 3.4+
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking

if sys.platform.startswith('win'):
    # First define a modified version of Popen.
    class _Popen(forking.Popen):
        def __init__(self, *args, **kw):
            if hasattr(sys, 'frozen'):
                # We have to set original _MEIPASS2 value from sys._MEIPASS
                # to get --onefile mode working.
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                    # available. In those cases we cannot delete the variable
                    # but only set it to the empty string. The bootloader
                    # can handle this case.
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    # Second override 'Popen' class with our modified version.
    forking.Popen = _Popen

if __name__ == "__main__":
    freeze_support()

    client = Niczy()
    queue = Queue()
    manager = Manager()
    _dict = manager.dict(speed=None, done=None)
    worker = Process(target=mp_downloader, args=(queue, _dict,))
    worker.daemon = True
    worker.start()

    app = App(redirect=False, process=worker, queue=queue, _dict=_dict, client=client)
    app.MainLoop()
