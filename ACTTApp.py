import sys
import os
import platform
import datetime
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

from datetime import datetime
from sim_info import info

l_lapcount=0
l_lastlaptime=0
lapcount=0
lastLapTime=0
lapInvalidated=False
validLaps=[]
time=0

def acMain(ac_version):
	global l_lapcount, l_lastlaptime
	ac.log("Hello from AC TT!")
	appWindow = ac.newApp("AC TT App")
	ac.setSize(appWindow, 200, 200)
	l_lapcount = ac.addLabel(appWindow, "Laps: 0")
	l_lastlaptime = ac.addLabel(appWindow, "Last Lap: N/A")
	ac.setPosition(l_lapcount, 3, 30)
	ac.setPosition(l_lastlaptime, 3, 50)
	ac.log("Available Info: {}".format(dir(info.static)))
	ac.log("Player: {}".format(info.static.playerNick))
	ac.log("Car Model: {}".format(info.static.carModel))
	ac.log("Track: {}".format(info.static.track))

	return "AC TT App"

def acUpdate(deltaT):
	global time, l_lapcount, l_lastlaptime, lapcount, lastLapTime, lapInvalidated
	laps = ac.getCarState(0, acsys.CS.LapCount)
	lastLap = ac.getCarState(0, acsys.CS.LastLap)
	wheelsOff = info.physics.numberOfTyresOut
	if wheelsOff > 3: lapInvalidated = True
	if laps > lapcount:
		lapcount = laps
		ac.setText(l_lapcount, "Laps: {}".format(lapcount))
		if lapInvalidated == False:
			lastLapTime = lastLap
			ac.setText(l_lastlaptime, "Last Lap: {}".format(formatDate(lastLapTime)))
			ac.setFontColor(l_lastlaptime, 1, 1, 1, 1)
			validLaps.append(lastLapTime)
			ac.log("{} valid laps array".format(str(validLaps)))
		else:
			lapInvalidated = False
			lastLapTime = lastLap
			ac.log("Last Lap was invalid")
			ac.setText(l_lastlaptime, "Last Lap: {}".format(formatDate(lastLapTime)))
			ac.setFontColor(l_lastlaptime, 1, 0, 0, 1)

def formatDate(time):
	ac.log("Time in MS: {}".format(time))
	formattedTime = datetime.fromtimestamp(time / 1000)
	s = formattedTime.strftime('%M:%S.%f')
	head = s[:-7]
	tail = s[-7:]
	f = float(tail)
	temp = "{:.3f}".format(f)
	new_tail = temp[1:]
	return head + new_tail