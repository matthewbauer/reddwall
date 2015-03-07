# -*- mode: python -*-
a = Analysis(['reddwall.py'],
             pathex=['C:\\Users\\jbaue_000\\Documents\\GitHub\\reddwall'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)


a.datas.append(('alien.png', 'alien.png', 'DATA'))
a.datas.append(('praw\\praw.ini', 'praw.ini', 'DATA'))
			 
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='reddwall.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False)
