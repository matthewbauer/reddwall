#!/usr/bin/env python

import sched
import time
import reddit

def run_schedule(sc):
	reddit.new_wallpaper()
	sc.enter(60, 1, run_schedule, (sc,))

if __name__ == "__main__":
	s = sched.scheduler(time.time, time.sleep)
	s.enter(0, 1, run_schedule, (s,))
	s.run()

