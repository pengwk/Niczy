# -*- mode: python -*-

block_cipher = None


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
          exclude_binaries=True,
          name='main_gui',
          debug=False,
          strip=False,
          upx=True,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main_gui')
               
a.datas += [("dgut_video_yellow.ico", "dgut_video_yellow.ico", "DATA")]
a.datas += [("poster.jpg", "poster.jpg", "DATA")]
a.datas += [("wechat200.jpg", "wechat200.jpg", "DATA")]
