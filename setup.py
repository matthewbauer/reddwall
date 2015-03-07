import ez_setup
ez_setup.use_setuptools()

import sys
from setuptools import setup

mainscript = 'reddwall.py'

if sys.platform == 'darwin':
	extra_options = dict(
		setup_requires=['py2app'],
		app=[mainscript],
		# Cross-platform applications generally expect sys.argv to
		# be used for opening files.
		options=dict(py2app=dict(
			plist={
				'CFBundleName': 'ReddWall',
				'CFBundleShortVersionString':'1.0.0', # must be in X.X.X format
				'CFBundleVersion': '1.0.0',
				'CFBundleIdentifier': 'com.bauer.reddwall', #optional
				'NSHumanReadableCopyright': '@ Matthew Bauer 2015', #optional
				'CFBundleDevelopmentRegion': 'English', #optional - English is default
#				'LSBackgroundOnly': 'true',
			},
		)),
	)
elif sys.platform == 'win32':
	extra_options = dict(
		setup_requires=['py2exe'],
		app=[mainscript],
	)
else:
	extra_options = dict(
		# Normally unix-like platforms will use "setup.py install"
		# and install the main script as such
		scripts=[mainscript],
	)

setup(
	name="ReddWall",
	version="1.0",
	author="Matthew Bauer",
	author_email="mjbauer95@gmail.com",
	url="http://matthewbauer.us/reddwall",
	install_requires=["wxpython", "praw", "beautifulsoup4"],
	data_files=["praw.ini", "alien.png"],
	**extra_options
)
