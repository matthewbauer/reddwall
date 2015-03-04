#!/usr/bin/env python

import os
import sys
import subprocess

class WallpaperSetter:
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
			ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, filename, 0)
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

def get_desktop_environment():
	if sys.platform in ["win32", "cygwin"]:
		return "windows"
	elif sys.platform == "darwin":
		return "mac"
	else: #Most likely either a POSIX system or something not much common
		desktop_session = os.environ.get("DESKTOP_SESSION")
		if desktop_session is not None: #easier to match if we doesn't have  to deal with caracter cases
			desktop_session = desktop_session.lower()
			if desktop_session in ["gnome","unity", "cinnamon", "mate", "xfce4", "lxde", "fluxbox", 
								   "blackbox", "openbox", "icewm", "jwm", "afterstep","trinity", "kde"]:
				return desktop_session
			## Special cases ##
			# Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
			# There is no guarantee that they will not do the same with the other desktop environments.
			elif "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
				return "xfce4"
			elif desktop_session.startswith("ubuntu"):
				return "unity"       
			elif desktop_session.startswith("lubuntu"):
				return "lxde" 
			elif desktop_session.startswith("kubuntu"): 
				return "kde" 
			elif desktop_session.startswith("razor"): # e.g. razorkwin
				return "razor-qt"
			elif desktop_session.startswith("wmaker"): # e.g. wmaker-common
				return "windowmaker"
		if os.environ.get('KDE_FULL_SESSION') == 'true':
			return "kde"
		elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
			if not "deprecated" in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
				return "gnome2"
		#From http://ubuntuforums.org/showthread.php?t=652320
		elif self.is_running("xfce-mcs-manage"):
			return "xfce4"
		elif self.is_running("ksmserver"):
			return "kde"
	return "unknown"

def get_wallpaper_setter():
	environment = get_desktop_environment()
	if environment in wallpaper_setters:
		return wallpaper_setters[environment]()
	return None

def set_wallpaper(filename):
	wallpaper_setter = get_wallpaper_setter()
	if wallpaper_setter is not None:
		wallpaper_setter.set_wallpaper(filename)
	else:
		raise Exception("Wallpaper could not be set because you're desktop is not recognized.")

if __name__ == "__main__":
	if len(sys.argv) > 1:
		set_wallpaper(sys.argv[1])
