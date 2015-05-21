ReddWall
================

ReddWall sets your wallpaper to a random image from one of the many Reddit wallpaper subreddits.

What it Does
------------

On the first run, ReddWall will find a random wallpaper from /r/wallpapers and minimize to the status bar. By default, it will select a new wallpaper every 1 hour. This behavior can be changed in the preferences window that can be opened by clicking the ReddWall icon in the status bar.

Downloads
---------
* Windows: [reddwall-v0.3.exe](https://github.com/matthewbauer/reddwall/releases/download/0.3/reddwall.exe)
* Mac OS X: [reddwall-v0.2.app](https://github.com/matthewbauer/reddwall/releases/download/0.2/reddwall.app.zip)
* Linux: [reddwall-v0.2.tar.gz](https://github.com/matthewbauer/reddwall/archive/0.2.tar.gz) (source code)

Running from Source
-------------------
To run from source, first make sure you have Git, Python 2.7, setuptools, and wxPython 2.7 installed. Then, clone the repo:

``git clone https://github.com/matthewbauer/reddwall.git``

and install it using the setup.py script:

``python2 setup.py install``

Reporting Issues
----------------

This program has not been tested on many different platforms. The cross platform toolkits used (wxWidgets, Python, and PRAW) mean that it should work without a problem. However, problems are bound to arise. If you have any issues with ReddWall, please [file an issue](https://github.com/matthewbauer/reddwall/issues/new) and I'll be sure to get back to you.
