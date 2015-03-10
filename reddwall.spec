# -*- mode: python -*-

block_cipher = None


a = Analysis(['reddwall.py'],
             pathex=['/Users/matthew/Projects/reddwall'])
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
          background=True,
          console=False )
app = BUNDLE(exe,
             name='reddwall.app',
             bundle_identifier='reddwall')
