# -*- mode: python -*-

block_cipher = pyi_crypto.PyiBlockCipher(key='pengwkiloveyou')

data_file = [("dgut_video_yellow.ico", "."),
              ("poster.jpg", "."),
              ("wechat200.jpg", ".")]

a = Analysis(['main_gui.py'],
             pathex=['E:\\temp\\Niczy'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=u'DGUT VIDEO Downloader',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          version='version.txt', 
          icon='dgut_video_yellow.ico')
