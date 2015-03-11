#!/usr/bin/env python
from detools import imagefinder
from detools import wallpaper
import threading
import praw
import random
import wx
import os.path
import sys
import json

r = praw.Reddit(user_agent='mac:org.bauer.reddwall:v1.0.0 (by /u/mjbauer95)')

pasts = ['hour', 'day', 'week', 'month', 'year', 'all']
suggested_subreddits = ['wallpapers', 'wallpaper', 'EarthPorn', 'BackgroundArt', 'TripleScreenPlus', 'quotepaper', 'BigWallpapers', 'MultiWall', 'DesktopLego', 'VideoGameWallpapers']
select = ['random', 'top']

default_settings = dict(
	interval = 24,
	minVote = 0,
	subreddit = 'wallpapers',
	search = '',
	past = 'day',
	allowNSFW = False,
	select = 'top'
)

class PreferencesDialog(wx.Dialog):
	def __init__(self, app):
		wx.Dialog.__init__(self, None, wx.ID_ANY, 'ReddWall', size=(400, 400))
		self.app = app

		self.Bind(wx.EVT_CLOSE, self.OnClose)

		vbox = wx.BoxSizer(wx.VERTICAL)

		vbox.Add(((-1, 10)))

		selectBox = wx.BoxSizer(wx.HORIZONTAL)
		selectBox.Add((10, -1))
		selectBox.Add(wx.StaticText(self, label='Select '))
		self.selectCombo = wx.ComboBox(self, value=self.app.settings['select'], choices=select, style=wx.CB_READONLY)
		self.selectCombo.Bind(wx.EVT_TEXT, self.SetSelectCombo)
		self.selectCombo.Bind(wx.EVT_COMBOBOX, self.SetSelectCombo)
		selectBox.Add(self.selectCombo)
		selectBox.Add(wx.StaticText(self, label=' wallpapers...'))
		vbox.Add(selectBox)

		vbox.Add((-1, 15))

		subredditBox = wx.BoxSizer(wx.HORIZONTAL)
		subredditBox.Add((25, -1))
		subredditBox.Add(wx.StaticText(self, label='from the '))
		self.subredditCombo = wx.ComboBox(self, value=self.app.settings['subreddit'], choices=suggested_subreddits)
		self.subredditCombo.Bind(wx.EVT_TEXT, self.SetSubredditCombo)
		self.subredditCombo.Bind(wx.EVT_COMBOBOX, self.SetSubredditCombo)
		subredditBox.Add(self.subredditCombo)
		subredditBox.Add(wx.StaticText(self, label=' subreddit'))
		vbox.Add(subredditBox)
		vbox.Add((-1, 15))

		searchBox = wx.BoxSizer(wx.HORIZONTAL)
		searchBox.Add((25, -1))
		searchBox.Add(wx.StaticText(self, label='containing search terms '))
		self.searchText = wx.TextCtrl(self, value=self.app.settings['search'])
		self.searchText.Bind(wx.EVT_TEXT, self.SetSearchText)
		searchBox.Add(self.searchText)
		vbox.Add(searchBox)
		vbox.Add((-1, 15))

		minVoteBox = wx.BoxSizer(wx.HORIZONTAL)
		minVoteBox.Add((25, -1))
		minVoteBox.Add(wx.StaticText(self, label='with at least '))
		self.minVoteSpin = wx.SpinCtrl(self, value=str(self.app.settings['minVote']), min=0, max=10000)
		self.minVoteSpin.Bind(wx.EVT_SPINCTRL, self.SetMinVoteSpin)
		minVoteBox.Add(self.minVoteSpin)
		minVoteBox.Add(wx.StaticText(self, label=' upvotes'))
		vbox.Add(minVoteBox)
		vbox.Add((-1, 15))

		fromBox = wx.BoxSizer(wx.HORIZONTAL)
		fromBox.Add((25, -1))
		fromBox.Add(wx.StaticText(self, label='from the past '))
		self.pastCombo = wx.ComboBox(self, choices=pasts, value=self.app.settings['past'], style=wx.CB_READONLY)
		self.pastCombo.Bind(wx.EVT_TEXT, self.SetPastCombo)
		self.pastCombo.Bind(wx.EVT_COMBOBOX, self.SetPastCombo)
		fromBox.Add(self.pastCombo)
		vbox.Add(fromBox)
		vbox.Add((-1, 15))

		intervalBox = wx.BoxSizer(wx.HORIZONTAL)
		intervalBox.Add((25, -1))
		intervalBox.Add(wx.StaticText(self, label='and update the wallpaper every '))
		self.intervalSpin = wx.SpinCtrl(self, value=str(self.app.settings['interval']), min=1)
		self.intervalSpin.Bind(wx.EVT_SPINCTRL, self.SetIntervalSpin)
		intervalBox.Add(self.intervalSpin)
		intervalBox.Add(wx.StaticText(self, label=' hours.'))
		vbox.Add(intervalBox)
		vbox.Add((-1, 15))

		nsfwBox = wx.BoxSizer(wx.HORIZONTAL)
		nsfwBox.Add((25, -1))
		self.nsfwCheck = wx.CheckBox(self, label='Allowing NSFW wallpapers?')
		self.nsfwCheck.SetValue(self.app.settings['allowNSFW'])
		self.nsfwCheck.Bind(wx.EVT_CHECKBOX, self.SetNSFWCheck)
		nsfwBox.Add(self.nsfwCheck)
		vbox.Add(nsfwBox)
		vbox.Add((-1, 15))

		vbox.Add((-1, 10))
		vbox.Add(wx.StaticLine(self), 0, wx.EXPAND)
		vbox.Add((-1, 10))

		aboutBox = wx.BoxSizer(wx.HORIZONTAL)
		aboutBox.Add((50, -1))
		aboutBox.Add(wx.StaticText(self, label="ReddWall\nby Matthew Bauer <mjbauer95@gmail.com>"))
		vbox.Add(aboutBox)

		self.SetSizer(vbox)

	def SetIntervalSpin(self, evt):
		self.app.settings['interval'] = self.intervalSpin.GetValue()
		self.app.OnUpdateInterval()

	def SetNSFWCheck(self, evt):
		self.app.settings['allowNSFW'] = self.nsfwCheck.IsChecked()
		self.app.OnFilterUpdate()

	def SetPastCombo(self, evt):
		self.app.settings['past'] = self.pastCombo.GetValue()
		self.app.OnFilterUpdate()

	def SetMinVoteSpin(self, evt):
		self.app.settings['minVote'] = self.minVoteSpin.GetValue()
		self.app.OnFilterUpdate()

	def SetSearchText(self, evt):
		self.app.settings['search'] = self.searchText.GetValue()
		self.app.OnFilterUpdate()

	def SetSubredditCombo(self, evt):
		self.app.settings['subreddit'] = self.subredditCombo.GetValue()
		self.app.OnFilterUpdate()

	def SetSelectCombo(self, evt):
		self.app.settings['select'] = self.selectCombo.GetValue()
		self.app.OnFilterUpdate()

	def OnClose(self, evt):
		self.app.SaveSettings()
		self.Destroy()

class ReddWallIcon(wx.TaskBarIcon):
	ID_NEW_OPTION = wx.NewId()
	ID_PREF_OPTION = wx.NewId()

	def __init__(self, parent):
		wx.TaskBarIcon.__init__(self)
		if getattr(sys, 'frozen', False):
			basedir = sys._MEIPASS
		else:
			basedir = os.path.dirname(__file__)
		ICON_PATH = os.path.join(basedir, "alien.png")
		self.SetIcon(wx.Icon(ICON_PATH, wx.BITMAP_TYPE_PNG), "alien")
		self.Bind(wx.EVT_MENU, parent.NextWallpaper, id=self.ID_NEW_OPTION)
		self.Bind(wx.EVT_MENU, parent.CreatePrefWindow, id=self.ID_PREF_OPTION)
		self.Bind(wx.EVT_MENU, parent.Quit, id=wx.ID_EXIT)

	def CreatePopupMenu(self):
		menu = wx.Menu()
		menu.Append(self.ID_NEW_OPTION, "&Next Wallpaper")
		menu.Append(self.ID_PREF_OPTION, "&Preferences...")
		menu.Append(wx.ID_EXIT, "&Quit")
		return menu

class ReddWall(wx.App):
	SETTINGS_PATH = os.path.join(os.path.expanduser("~"), ".reddwall.json")
	MIN_NUM = 1
	MAX_TRIES = 10
	submissions = []
	needSubmissionsUpdate = False
	is_running = False
	submission_ids = []
	settings = default_settings
	updatingSubmissions = False

	def __init__(self):
		wx.App.__init__(self)

		self.LoadSettings()
		self.icon = ReddWallIcon(self)

		thread = threading.Thread(target=self.Init)
		thread.setDaemon(True)
		thread.start()

		self.timer = wx.Timer(self, -1)
		self.Bind(wx.EVT_TIMER, self.NextWallpaper, self.timer)
		self.StartTimer()

		self.frame = wx.Frame(None, -1, style=wx.NO_BORDER|wx.FRAME_NO_TASKBAR)
		self.MainLoop()

		self.SaveSettings()

	def Init(self):
		self.GetSubmissions()
		self.NextWallpaper()

	def SubmissionOkay(self, submission):
		return submission.score > self.settings['minVote'] and (self.settings['allowNSFW'] or not submission.over_18) and not submission.id in self.submission_ids

	def GetSubmissions(self):
		#if self.updatingSubmissions:
		#	return
		self.updatingSubmissions = True
		subreddit = r.get_subreddit(self.settings['subreddit'])
		pasts = {
			'hour': subreddit.get_top_from_hour,
			'day': subreddit.get_top_from_day,
			'week': subreddit.get_top_from_week,
			'month': subreddit.get_top_from_month,
			'year': subreddit.get_top_from_year,
			'all': subreddit.get_top_from_all
		}
		self.submissions = []
		num_submissions = self.MIN_NUM
		limit = 100
		if self.settings['select'] == 'random':
			limit = 100
		elif self.settings['select'] == 'top':
			limit = 1
		request = pasts[self.settings['past']](limit=limit)
		for submission in request:
			if self.SubmissionOkay(submission):
				self.submissions.append(submission)
				#self.submission_ids.append(submission.id)
				num_submissions -= 1
		if self.settings['select'] == 'random':
			random.shuffle(self.submissions)
		self.needSubmissionsUpdate = False
		self.updatingSubmissions = False

	def UntilValidImageUrl(self):
		tries = self.MAX_TRIES
		while tries > 0:
			try:
				if len(self.submissions) == 0:
					self.GetSubmissions()
					if len(self.submissions) == 0:
						return
				submission = self.submissions.pop()
				return imagefinder.get_image_request(submission.url)
			except imagefinder.NoImageFound:
				tries -= 1
				continue

	def NextWallpaper(self, evt=None):
		#if self.is_running:
		#	return
		self.is_running = True
		if self.needSubmissionsUpdate or self.settings['select'] == 'top':
			self.GetSubmissions()
		wallpaper.set_wallpaper_request(self.UntilValidImageUrl())
		self.is_running = False

	def CreatePrefWindow(self, evt=None):
		self.preferences = PreferencesDialog(self)
		self.preferences.Show()
		self.preferences.Raise()
		self.preferences.Iconize(False)

	def StartTimer(self):
		self.timer.Start(self.settings['interval'] * 60 * 60 * 1000)

	def OnUpdateInterval(self):
		self.timer.Stop()
		self.StartTimer()

	def OnFilterUpdate(self):
		self.needSubmissionsUpdate = True

	def OSXIsGUIApplication(self):
		return False

	def SaveSettings(self):
		with open(self.SETTINGS_PATH, 'w') as outfile:
		    json.dump(self.settings, outfile)

	def LoadSettings(self):
		try:
			with open(self.SETTINGS_PATH, 'r') as infile:
				self.settings.update(json.load(infile))
		except:
			pass

	def Quit(self, evt=None, frame=None):
		self.SaveSettings()
		self.ExitMainLoop()

ReddWall()
