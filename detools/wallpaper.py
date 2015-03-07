#!/usr/bin/env python

import sys
import subprocess
import tempfile
import de
import os

class WallpaperSetter:
	def __init__(self, environment):
		self.environment = environment
	def set_wallpaper(self, filename):
		pass

wallpaper_setters = {}

try:
	import gi.repository.Gio
	class GnomeWallpaperSetter(WallpaperSetter):
		SCHEMA = 'org.gnome.desktop.background'
		KEY = 'picture-uri'
		def set_wallpaper(self, filename):
			gsettings = gi.repository.Gio.Settings.new(self.SCHEMA)
			gsettings.set_string(self.KEY, "file://" + filename)
	wallpaper_setters["gnome"] = GnomeWallpaperSetter
	wallpaper_setters["unity"] = GnomeWallpaperSetter
	wallpaper_setters["cinnamon"] = GnomeWallpaperSetter
except ImportError:
	pass

try:
	import ctypes
	class WindowsWallpaperSetter(WallpaperSetter):
                SPI_SETDESKWALLPAPER = 20
		def set_wallpaper(self, filename):
			ctypes.windll.user32.SystemParametersInfoA(self.SPI_SETDESKWALLPAPER, 0, filename, 0)
	wallpaper_setters["windows"] = WindowsWallpaperSetter
except ImportError:
	pass

class PopenWallpaperSetter(WallpaperSetter):
	def set_wallpaper(self, filename):
		subprocess.Popen(self.get_args(filename), shell=True)

class GSettingsWallpaperSetter(PopenWallpaperSetter):
	def get_args(self, filename):
		return ["gsettings", "set", SCOPE, ATTRIBUTE, filename]

class GConfWallpaperSetter(PopenWallpaperSetter):
	CONFTOOL = "gconftool-2"
	def get_args(self, filename):
		return [CONFTOOL, "-t", "string", "--set", PATH, filename]

class MateWallpaperSetter(GSettingsWallpaperSetter):
	SCOPE = "org.mate.background"
	ATTRIBUTE = "picture-filename"
wallpaper_setters["mate"] = MateWallpaperSetter

class KDEWallpaperSetter(PopenWallpaperSetter):
	def get_args(self, filename):
		return ['dcop', 'kdesktop', 'KBackgroundIface', 'setWallpaper', '0', filename, '6']
wallpaper_setters["kde"] = KDEWallpaperSetter

class XFCEWallpaperSetter(PopenWallpaperSetter):
	def get_args(self, filename):
		return ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-path", "-s", filename]
wallpaper_setters["xfce4"] = XFCEWallpaperSetter

class FluxBoxWallpaperSetter(PopenWallpaperSetter):
	def get_args(self, filename):
		return ["fbsetbg", filename]
wallpaper_setters["fluxbox"] = FluxBoxWallpaperSetter

class IceWMWallpaperSetter(PopenWallpaperSetter):
	def get_args(self, filename):
		return ["icewmbg", filename]
wallpaper_setters["icewm"] = IceWMWallpaperSetter

class BlackBoxWallpaperSetter(PopenWallpaperSetter):
	def get_args(self, filename):
		return ["bsetbg", "-full", filename]
wallpaper_setters["blackbox"] = BlackBoxWallpaperSetter

class PCManFMWallpaperSetter(PopenWallpaperSetter):
	def get_args(self, filename):
		return ["pcmanfm", "--set-wallpaper", filename]
wallpaper_setters["lxde"] = PCManFMWallpaperSetter

class WindowMakerWallpaperSetter(PopenWallpaperSetter):
	def get_args(self, filename):
		return ["wmsetbg", "-s", "-u", filename]
wallpaper_setters["windowmaker"] = WindowMakerWallpaperSetter

class MacWallpaperSetter(PopenWallpaperSetter):
	def get_args(self, filename):
		return 'osascript -e "tell application \\"Finder\\" to set desktop picture to POSIX file \\"%s\\""' % filename
wallpaper_setters["mac"] = MacWallpaperSetter

def get_wallpaper_setter():
	environment = de.get_desktop_environment()
	if environment in wallpaper_setters:
		return wallpaper_setters[environment](environment)
	return WallpaperSetter(environment)

class WallpaperSetterError(Exception):
	def __init__(self, environment):
		self.environment = environment
	def __str__(self):
		return "Cannot set wallpaper for %s" % self.environment

def set_wallpaper(filename):
	wallpaper_setter = get_wallpaper_setter()
	if wallpaper_setter is not None:
		try:
                        wallpaper_setter.set_wallpaper(filename)
		except:
			raise WallpaperSetterError(wallpaper_setter.environment)
	else:
		raise WallpaperSetterError(wallpaper_setter.environment)

def set_wallpaper_request(request):
	#i, path = tempfile.mkstemp(suffix=".jpg", dir=os.getcwd())
        path = os.path.join(os.getcwd(), "background.jpg")
	with open(path, 'wb') as fo:
		for chunk in request.iter_content(4096):
			fo.write(chunk)
	set_wallpaper(path)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		set_wallpaper(sys.argv[1])
