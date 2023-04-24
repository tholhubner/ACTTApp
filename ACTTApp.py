import sys
import os
import platform
import ac
import acsys

def get_lib_dir():
	if platform.architecture()[0] == '64bit':
		return 'lib64'
	else:
		return 'lib'
	
lib_dir = 'apps/python/ACTTApp/{}'.format(get_lib_dir())
sys.path.insert(0, lib_dir)
os.environ['PATH'] += ';.'

from sim_info import info

l_lapcount=0
l_lastlaptime=0
lapcount=0
lastLapTime=0
lapInvalidated=False
validLaps=[]
time=0

def acMain(ac_version):
	global l_lapcount

	appWindow = ac.newApp("AC TT App")
	ac.setSize(appWindow, 150, 150)

	ac.log("Hello from AC TT!")

	l_lapcount = ac.addLabel(appWindow, "Laps: 0")
	l_lastlaptime = ac.addLabel(appWindow, "Last Lap: N/A")
	ac.setPosition(l_lapcount, 3, 30)
	ac.setPosition(l_lastlaptime, 3, 45)
	return "AC TT App"

def acUpdate(deltaT):
	global time, l_lapcount, l_lastlaptime, lapcount, lastLapTime, lapInvalidated
	laps = ac.getCarState(0, acsys.CS.LapCount)
	lastLap = ac.getCarState(0, acsys.CS.LastLap)
	wheelsOff = info.physics.numberOfTyresOut
	if wheelsOff > 3: lapInvalidated = True
	if laps > lapcount:
		lapcount = laps
		ac.log("{} laps completed".format(lapcount))
		ac.setText(l_lapcount, "Laps: {}".format(lapcount))
		if lapInvalidated == False:
			lastLapTime = lastLap
			ac.log("{} last lap in MS".format(str(lastLapTime)))
			ac.setText(l_lastlaptime, "Last Lap: Butthole")
			# ac.setFontColor(l_lastlaptime, 0, 0, 0, 1)
			validLaps.append(lastLapTime)
			ac.log("{} valid laps array".format(str(validLaps)))
		else:
			lastLapTime = 0
			lapInvalidated = False
			ac.log("Last Lap was invalid")
			ac.setText(l_lastlaptime, "Last Lap: Invalid Lap")
			# ac.setFontColor(l_lastlaptime, 1, 0, 0, 1)