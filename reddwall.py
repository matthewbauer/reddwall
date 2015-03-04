#!/usr/bin/env python

import wallpaper
import praw
import tempfile
import requests
import random
from bs4 import BeautifulSoup

r = praw.Reddit(user_agent='mac:org.bauer.reddwall:v1.0.0 (by /u/mjbauer95)')

def download_image(source, dest):
	response = requests.get(source)
	if response.status_code == 200:
		with open(dest, 'wb') as fo:
			for chunk in response.iter_content(4096):
				fo.write(chunk)

def download_submission(source, dest):
	if 'http://imgur.com/' in source:
		html_source = requests.get(source).text
		soup = BeautifulSoup(html_source)
		source = soup.select('.image a')[0]['href']
		if source.startswith('//'):
			source = 'http:' + source
	download_image(source, dest)

def new_wallpaper():
	f, path = tempfile.mkstemp()
	choices = []
	#submission = r.get_random_submission('wallpapers')
	#submission = next(r.get_subreddit('wallpapers').get_top(limit=1))
	for submission in r.get_subreddit('wallpapers').get_top(limit=100):
		choices.append(submission.url)
	download_submission(random.choice(choices), path)
	wallpaper.set_wallpaper(path)

if __name__ == "__main__":
	new_wallpaper()
