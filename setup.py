#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

setup(name='ReddWall',
      version='0.2',
      description='Get random wallpapers from Reddit',
      author='Matthew Bauer',
      author_email='mjbauer95@gmail.com',
      url='http://github.com/matthewbauer/reddwall',
      install_requires=['requests', 'beautifulsoup4', 'praw', 'wxpython'],
      packages=['detools'],
      scripts=['reddwall.py'],
)
