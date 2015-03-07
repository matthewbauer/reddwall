#!/usr/bin/env python

import os
import sys

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

if __name__ == "__main__":
	print(get_desktop_environment())
