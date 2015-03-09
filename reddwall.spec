# -*- mode: python -*-
a = Analysis(['reddwall.py'],
             pathex=['/Users/matthew/Projects/reddwall'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          TOC([('praw/praw.ini', 'praw.ini', 'DATA'), ('alien.png', 'alien.png', 'DATA')]),
          name='reddwall',
          debug=False,
          strip=True,
          upx=True,
          console=False,
          background=True )
app = BUNDLE(exe,
             name='reddwall.app',
             icon=None)
