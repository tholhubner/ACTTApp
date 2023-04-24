import sys
import os
import ac
import acsys
sys.path.insert(len(sys.path), "apps/python/ACTTApp/third_party")

from sim_info import info

l_lapcount=0
l_lastlaptime=0
lapcount=0
lastLapTime=0
validLaps=[]
time=0

def acMain(ac_version):
	global l_lapcount

	appWindow = ac.newApp("ACTTApp")
	ac.setSize(appWindow, 200, 200)

	ac.log("Hello, Assetto Corsa application world!")
	ac.console("Hello, Assetto Corsa console!")

	l_lapcount = ac.addLabel(appWindow, "Laps: 0")
	l_lastlaptime = ac.addLabel(appWindow, "Last Lap: N/A")
	ac.setPosition(l_lapcount, 3, 30)
	ac.setPosition(l_lastlaptime, 3, 50)
	return "ACTTApp"

def acUpdate(deltaT):
	global time, l_lapcount, l_lastlaptime, lapcount, lastLapTime
	time += deltaT
	if time > 10:
		laps = ac.getCarState(0, acsys.CS.LapCount)
		lastLap = ac.getCarState(0, acsys.CS.LastLap)
		if laps > lapcount:
			lapcount = laps
			ac.log("{} laps completed".format(lapcount))
			ac.setText(l_lapcount, "Laps: {}".format(lapcount))
			lapInvalidated = ac.getCarState(0, acsys.CS.LapInvalidated)
			ac.log("{} lap validation value RAW".format(str(lapInvalidated)))
			if not lapInvalidated:
				lastLapTime = lastLap
				ac.log("{} last lap in MS".format(str(lastLapTime)))
				ac.setText(l_lastlaptime, "Last Lap: {}".format(str(lastLapTime)))
				ac.setFontColor(l_lastlaptime, 0, 0, 0, 1)
				validLaps.append(lastLapTime)
				ac.log("{} valid laps array".format(str(validLaps)))
				time = 0
			else:
				lastLapTime = 0
				ac.log("Last Lap was invalid")
				ac.setText(l_lastlaptime, "Last Lap: Invalid Lap")
				ac.setFontColor(l_lastlaptime, 1, 0, 0, 1)
				time = 0