# _*_ coding:utf-8 _*_

import wx

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

        school_msg = u"""不知道会不会影响你们的工作，如果给您添麻烦了，抱歉！\n """
        to_school = wx.StaticText(self, label=school_msg)
        school_text = wx.StaticText(self, label=u"网站管理：")

        teacher_msg = u"""证件照和介绍信息是体育系官网找到的，抱歉！如果老师愿意提供靓照，感激不尽。\n """
        to_teacher = wx.StaticText(self, label=teacher_msg)
        teacher_text = wx.StaticText(self, label=u"亲爱的老师：")

        others_msg = u"""希望能帮到你，有什么想法或问题加我微信聊，邮箱也没问题。\n \n """
        to_others = wx.StaticText(self, label=others_msg)
        others_text = wx.StaticText(self, label=u"同学、朋友：")

        # 版权声明
        copyright_text = wx.StaticText(self, label=u"版权声明：")
        copyright = wx.StaticText(self, label=u"保留所有权利。")

        self.gbsizer.AddMany([(school_text, (0, 0)),
                              (to_school, (0, 1)),

                              (teacher_text, (1, 0)),
                              (to_teacher, (1, 1)),

                              (others_text, (2, 0)),
                              (to_others, (2, 1)),

                              (author_text, (3, 0)),
                              (author_name, (3, 1)),

                              (mail_text, (4, 0)),
                              (mail_addr, (4, 1)),

                              (wechat_text, (5, 0)),
                              (wechat_bmp, (5, 1)),

                              (copyright_text, (7, 0)),
                              (copyright, (7, 1)),
                              ])

        self.SetSizer(self.gbsizer)
