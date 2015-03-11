# -*- mode: python -*-
block_cipher = None
a = Analysis(['reddwall.py'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          TOC([('praw/praw.ini', 'praw.ini', 'DATA'), ('alien.png', 'alien.png', 'DATA')]),
          name='reddwall.exe',
          debug=False,
          strip=False,
          upx=True,
          background=True,
          console=False )
app = BUNDLE(exe,
             name='reddwall.app',
             bundle_identifier='com.bauer.reddwall')
