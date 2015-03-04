import ez_setup
ez_setup.use_setuptools()

import sys
from setuptools import setup

mainscript = 'schedule.py'

if sys.platform == 'darwin':
 extra_options = dict(
	 setup_requires=['py2app'],
	 app=[mainscript],
	 # Cross-platform applications generally expect sys.argv to
	 # be used for opening files.
	 options=dict(py2app=dict(argv_emulation=True)),
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
name="reddwall",
**extra_options
)
