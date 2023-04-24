import sys
import ac
import acsys

l_lapcount=0
l_lastlaptime=0
lapcount=0
lastLapTime=0
validLaps=[]

def acMain(ac_version):
	global l_lapcount

	appWindow = ac.newApp("appName")
	ac.setSize(appWindow, 200, 200)

	ac.log("Hello, Assetto Corsa application world!")
	ac.console("Hello, Assetto Corsa console!")

	l_lapcount = ac.addLabel(appWindow, "Laps: 0");
	l_lastlaptime = ac.addLabel(appWindow, "Last Lap: N/A")
	ac.setPosition(l_lapcount, 3, 30)
	ac.setPosition(l_lastlaptime, 3, 50)
	return "appName"

def acUpdate(deltaT):
	global l_lapcount, lapcount
	laps = ac.getCarState(0, acsys.CS.LapCount)
	lastLap = ac.getCarState(0, acsys.CS.LastLap)
	lapInvalidated = ac.getCarState(0, acsys.CS.LapInvalidated)
	if laps > lapcount:
		lapcount = laps
		ac.console("{} laps completed".format(lapcount))
		ac.setText(l_lapcount, "Laps: {}".format(lapcount))
		if lapInvalidated == 0:
			lastLapTime = lastLap
			ac.console("{} last lap in MS".format(lastLapTime))
			validLaps.append(lastLapTime)
			ac.setText(l_lastlaptime, "Last Lap: {}".format(lastLapTime))
		else:
			lastLapTime = 0
			ac.setText(l_lastlaptime, "Last Lap: Invalid Lap")