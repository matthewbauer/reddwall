#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import urlparse

class NoImageFound(Exception):
	def __init__(self, url):
		self.url = url
	def __str__(self):
		return "Could not find an image for the url %s" % self.url

def get_image_links(soup):
	links = []
	links.extend(soup.select('.image a')) # imgur
	links.extend(soup.select('a.js-download')) # pexels
	links.extend(soup.select('#allsizes-photo img')) # flickr
	links.extend(soup.select('a[imageanchor]')) # blogspot
	links.extend(soup.select('.dev-view-deviation img')) # deviantart
	links.extend(soup.select('img#wallpaper')) # wallhaven
	links.extend(soup.select('.post a img')) # imgur
	return links

def get_image_request(url, follow=True, max_recurse=5):
	if max_recurse == 0:
		return
	max_recurse -= 1
	url = urlparse.urlparse(url, 'http')
	r = requests.get(url.geturl())
	content_type = r.headers['content-type'].split(';')[0]
	if follow and 'location' in r.headers:
		return get_image_request(r.headers['location'], False, max_recurse)
	if follow and content_type == 'text/html':
		soup = BeautifulSoup(r.text)
		links = get_image_links(soup)
		if len(links) == 0:
			raise NoImageFound(url.geturl())
		link = links[0]
		link_url = None
		if link.has_attr('href'):
			link_url = link['href']
		elif link.has_attr('src'):
			link_url = link['src']
		if link_url is None:
			raise NoImageFound(url.geturl())
		return get_image_request(link_url, False, max_recurse)
	if not content_type.startswith('image/'):
		raise NoImageFound(url.geturl())
	return r

if __name__ == "__main__":
	import praw

	r = praw.Reddit(user_agent='reddwall:v1.0.1 (by /u/mjbauer95)')

	for submission in r.get_subreddit('wallpaper').get_hot(limit=100):
		try:
			get_image_request(submission.url)
		except NoImageFound:
			print(submission.url)
