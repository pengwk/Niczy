# _*_ coding:utf-8 _*_

import os
import sys
from Queue import Queue
from threading import Thread
import wx
# import wx.lib.inspection

import widgets
import resource

from niczy_client import Niczy


class Frame(wx.Frame):

    def __init__(self, parent, id, title, pos, size, style, name,
                 ):

        super(Frame, self).__init__(parent, id, title, pos, size, style, name)

        self.url_input = widgets.DownloadBar(self, "url_input", )
        self.video_item = widgets.VideoItem(self, "video_item", )
        self.ad_poster = widgets.ADPoster(self, "ad_poster", )
        self.contact_author = widgets.TopBar(self, "top_bar")
        self.m_sizer = wx.BoxSizer(wx.VERTICAL)

        self.m_sizer.AddMany([(self.contact_author, 0, wx.EXPAND),
                                (self.url_input, 0, wx.ALL | wx.EXPAND, 2),
                              (self.video_item, 5, wx.ALL | wx.EXPAND, 2),
                              (self.ad_poster, 3, wx.ALL | wx.EXPAND, 2)])

        self.SetSizer(self.m_sizer)

        self._set_icon()

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def _set_icon(self, ):
        icon = wx.Icon(resource.ico_dgut)
        self.SetIcon(icon)

    def OnClose(self, event):
        app = wx.GetApp()
        app.task_queue.put("stop")
        app.worker.join()
        self.Destroy()

class App(wx.App):

    def __init__(self, redirect=True, filename=None, useBestVisual=False, clearSigInt=True,
                 ):
        self.client = Niczy()
        self.task_queue = Queue()
        
        self.worker = Thread(target=self.client.gui_downloader, args=(self.task_queue, self))
        self.worker.start()

        super(App, self).__init__(
            redirect, filename, useBestVisual, clearSigInt)
        
    def OnInit(self, ):
        self.frame = Frame(None, wx.ID_ANY, u"Niczy下载器", wx.DefaultPosition,
                           (800, 400), wx.DEFAULT_FRAME_STYLE, "frame",
                            )
        self.SetTopWindow(self.frame)
        self.frame.Show()
        self.frame.Center()
        
        # wx.lib.inspection.InspectionTool().Show()
        return True




if __name__ == "__main__":

    app = App(redirect=False,)
    app.MainLoop()
