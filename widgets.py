# _*_ coding:utf-8 _*_

import os
import webbrowser

import wx
import wx.lib.buttons as GenButton

from niczy_client import Niczy
from tool import readable_size, file_dir, open_in_folder


class DownloadBar(wx.Panel):

    def __init__(self, parent, name, queue, _dict, client):

        super(DownloadBar, self).__init__(parent, name=name)

        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.hsizer)

        self.url = wx.TextCtrl(self, value=u"Niczy视频网址")
        self.download_button = wx.Button(self, label=u"下载")

        flags = wx.ALIGN_CENTER_VERTICAL
        self.hsizer.AddMany([(self.url, 5, flags | wx.ALL, 5),
                             (self.download_button, 1, flags | wx.ALL, 5)])

        self.Bind(wx.EVT_BUTTON, self.OnButton)

        self.niczy = client
        self.queue = queue

    def OnButton(self, event):
        url = self.url.GetValue().split()[0]
        if url.startswith("http://niczy.dgut.edu.cn"):

            video_info = self.niczy.video_info(url)
            video_name = video_info[u"video_name"]
            file_name = "".join([video_name, ".mp4"])

            # video_info = {"video_size": "100000000"}
            # file_name = "office.ios"
            nice_size = readable_size(int(video_info["video_size"]))
            message = u"选择存放地点（{}）".format(nice_size)

            style = wx.SAVE | wx.CHANGE_DIR
            dlg = wx.FileDialog(self, message=message,
                                defaultDir=os.getcwd(),
                                defaultFile=file_name,
                                style=style)
            if dlg.ShowModal() == wx.ID_OK:
                file_path = dlg.GetPath()

                # 更新videoitem 调用下载
                job = {"file_path": file_path,
                       "url": video_info["download_url"]}
                test = {"file_path": file_path,
                        "url": "http://192.168.199.202:8000/Protel99SE.zip",
                        "file_name": file_path}
                self.queue.put(job)
                video_info["file_path"] = file_path
                self._update_item(video_info)
        else:
            dlg = wx.MessageDialog(self, u"目前只支持 媒体资源网 视频下载", u"使用提示^_^")
            dlg.ShowModal()
            webbrowser.open("http://niczy.dgut.edu.cn")
            dlg.Destroy()

    def _update_item(self, video_info):
        import StringIO
        video_item = wx.FindWindowByName("video_item")

        res = self.niczy.s.get(video_info["poster_url"])
        stream = StringIO.StringIO(res.content)
        poster_bmp = wx.ImageFromStream(stream).ConvertToBitmap()
        video_item.update_info(video_info, poster_bmp)
        return None


class VideoItem(wx.Panel):

    def __init__(self, parent, name, queue, _dict, client):

        super(VideoItem, self).__init__(parent, name=name)

        # 更新下载进度条
        self._dict = _dict
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        self.m_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.m_sizer)

        path = "E:\UIDesign\poster.png"
        bmp = wx.Image(path).ConvertToBitmap()
        self.poster = wx.StaticBitmap(self, bitmap=bmp)

        self.video_name = wx.StaticText(self, label=u"星球大战")
        self.download_progress = wx.Gauge(self, -1, range=100)
        #self.cancel_btn = wx.Button(self, label=u"取消")
        self.path_label = wx.StaticText(self, label=u"存放在：")
        self._dir_btn = GenButton.GenButton(self, label=u"E:\字体")

        flags = wx.ALIGN_LEFT
        self.file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.file_sizer.AddMany([(self.path_label, 0, flags | wx.ALIGN_CENTER_VERTICAL | wx.ALL ^ wx.LEFT, 5),
                                 (self._dir_btn, 0,
                                  wx.ALIGN_CENTER_VERTICAL, wx.RIGHT, 5),
                                 #(self.cancel_btn, 0, flags | wx.ALL, 5)
                                 ])

        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.AddMany([(self.video_name, 0, flags | wx.ALL, 5),
                             (self.download_progress, 0, flags | wx.ALL, 5),
                             (self.file_sizer, 0, flags | wx.ALL, 5)])

        self.m_sizer.AddMany([(self.poster, 0, wx.ALL, 6),

                              (self.vsizer, 0, wx.ALL, 5)])

        self.Bind(wx.EVT_BUTTON, self.OnButton, self._dir_btn)

    def OnButton(self, event):
        _path = self._dir_btn.Name
        open_in_folder(_path)
        return None
    # api

    def update_info(self, video_info, poster_bmp):
        self.poster.SetBitmap(poster_bmp)
        self.video_name.SetLabel(video_info["video_name"])
        _file_dir = file_dir(video_info["file_path"])
        self._dir_btn.SetName(video_info["file_path"])
        self._dir_btn.SetLabel(_file_dir)
        self._dir_btn.Refresh()
        self.timer.Start(100)
        return None

    def OnTimer(self, event):
        _float = self._dict["done"]
        if _float is not None:
            _str = str(_float * 100).split(".")[0]
            self.download_progress.SetValue(int(_str))
            if _str == "100":
                self.timer.Stop()
        return None


class ADPoster(wx.Panel):

    def __init__(self, parent, name, _dict):

        super(ADPoster, self).__init__(parent, name=name)

        self.line = wx.StaticText(
            self, label=u"  后来许多人问我一个人夜晚踟蹰路上的心情，我想起的却不是孤单和路长，而是波澜壮阔的海和天空中闪耀的星光。")
        self.author = wx.StaticText(self, label=u"张小砚")

        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.line.SetFont(font)

        bmp = wx.Image("ad.png").ConvertToBitmap()
        self.ad = wx.StaticBitmap(self, bitmap=bmp)
        self.ad.Hide()

        msizer = wx.BoxSizer(wx.VERTICAL)
        msizer.AddMany([(self.line, 1, wx.ALL | wx.ALIGN_CENTER, 5),
                        (self.author, 1, wx.ALIGN_RIGHT | wx.ALL, 5),
                        (self.ad, 1, wx.ALL, 5)])
        self.SetSizer(msizer)

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

    def OnEnterWindow(self, event):
        print "Enter"
        self.ShowAD(True)
        return True

    def OnLeaveWindow(self, event):
        print "Leave"
        self.ShowAD(False)
        return True

    def ShowAD(self, flag=True):
        if flag == True:
            self.Freeze()
            self.line.Hide()
            self.author.Hide()
            self.ad.Show()
            self.Layout()
            self.Thaw()
            return None
        elif flag == False:
            self.Freeze()
            self.line.Show()
            self.author.Show()
            self.ad.Hide()
            self.Layout()
            self.Thaw()
            return None


class AboutDialog(wx.Dialog):
    u""""""

    def __init__(self, parent, name, title):
        style = wx.RESIZE_BORDER | wx.DEFAULT_DIALOG_STYLE
        super(AboutDialog, self).__init__(
            parent, name=name, style=style, title=title)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        about_panel = AboutPanel(self, u"about_panel")
        flags = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER
        self.vsizer.Add(about_panel, 0, flags, 30)

        self.SetSizerAndFit(self.vsizer)


class AboutPanel(wx.Panel):
    u""""""

    def __init__(self, parent, name):
        size = (-1, -1)  # (300, 400)
        super(AboutPanel, self).__init__(parent, name=name, size=size)

        self.gbsizer = wx.GridBagSizer(vgap=5, hgap=5)

        img_dir = "C:\Users\wk\OneDrive\W\QiangGui\img"
        path = os.path.join(img_dir, "wechat200.jpg")
        image = wx.Image(path).ConvertToBitmap()

        wechat_text = wx.StaticText(self, label=u"微信/WeChat：")
        wechat_bmp = wx.StaticBitmap(self, bitmap=image)

        mail_text = wx.StaticText(self, label=u"邮箱/Mail：")
        mail_addr = wx.StaticText(self, label=u"pengwk2@gmail.com")

        author_text = wx.StaticText(self, label=u"作者/Author：")
        author_name = wx.StaticText(self, label=u"彭未康")

        # school_msg = u"""不知道会不会影响你们的工作，如果给您添麻烦了，抱歉！\n """
        # to_school = wx.StaticText(self, label=school_msg)
        # school_text = wx.StaticText(self, label=u"网站管理：")
#
        # teacher_msg = u"""证件照和介绍信息是体育系官网找到的，抱歉！如果老师愿意提供靓照，感激不尽。\n """
        # to_teacher = wx.StaticText(self, label=teacher_msg)
        # teacher_text = wx.StaticText(self, label=u"亲爱的老师：")
#
        # others_msg = u"""希望能帮到你，有什么想法或问题加我微信聊，邮箱也没问题。\n \n """
        # to_others = wx.StaticText(self, label=others_msg)
        # others_text = wx.StaticText(self, label=u"同学、朋友：")
#
        # 版权声明
        copyright_text = wx.StaticText(self, label=u"版权声明：")
        copyright = wx.StaticText(self, label=u"保留所有权利。")

        self.gbsizer.AddMany([

            (author_text, (0, 0)),
            (author_name, (0, 1)),

            (mail_text, (1, 0)),
            (mail_addr, (1, 1)),

            (wechat_text, (2, 0)),
            (wechat_bmp, (2, 1)),

            (copyright_text, (3, 0)),
            (copyright, (3, 1)),
        ])

        self.SetSizer(self.gbsizer)


class TopBar(wx.Panel):
    u"""窗口顶部 登录，退出，显示网络状态，联系作者"""

    def __init__(self, parent, name):
        style = 0
        super(TopBar, self).__init__(parent, name=name, style=style)

        author = GenButton.GenButton(
            self, label=u"联系作者", style=wx.BORDER_NONE, size=(-1, 18))
        self.Bind(wx.EVT_BUTTON, self.OnAbout, author)

        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer.AddMany([((1, 0), 10),
                             (author, 1, wx.EXPAND | wx.RIGHT | wx.ALIGN_RIGHT, 5),
                             ])
        self.SetSizer(self.hsizer)

    def OnAbout(self, event):
        dlg = AboutDialog(self, u"about_dialog", u"联系作者")
        dlg.CenterOnScreen()
        dlg.ShowModal()
        dlg.Destroy()
