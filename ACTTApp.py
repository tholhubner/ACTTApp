import sys
import os
import requests
import platform
import datetime
import json
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

requestsUrl = 'http://http://137.184.145.119/api/raw_data'

from datetime import datetime
from sim_info import info

l_lapcount=0
l_lastlaptime=0
l_lapcountmet=0
b_sendbutton=0
lapcount=0
lastLapTime=0
lapInvalidated=False
validLaps=[]
time=0

class sessionValues:
	def __init__(self, name, car, track, laps):
		self.name = name
		self.car = car
		self.track = track
		self.laps = laps

def acMain(ac_version):
	global l_lapcount, l_lastlaptime, b_sendbutton
	ac.log("Hello from AC TT!")
	appWindow = ac.newApp("AC TT App")
	ac.setSize(appWindow, 200, 200)
	l_lapcount = ac.addLabel(appWindow, "Laps: 0")
	l_lastlaptime = ac.addLabel(appWindow, "Last Lap: N/A")
	l_lapcountmet = ac.addLabel(appWindow, "5 Valid Laps Complete")
	b_sendbutton = ac.addButton(appWindow, "Send Data")
	ac.setFontColor(l_lastlaptime, 0, 1, 0, 0)
	ac.setPosition(l_lapcount, 3, 30)
	ac.setPosition(l_lastlaptime, 3, 50)
	ac.setPosition(l_lapcountmet, 3, 70)
	ac.setPosition(b_sendbutton, 3, 90)
	ac.addOnClickedListener(b_sendbutton, onSendButtonPress)

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
			if len(validLaps) > 4:
				ac.setFontColor(l_lastlaptime, 0, 1, 0, 1)
			ac.log("{} valid laps array".format(str(validLaps)))
			finished = sessionValues(info.static.playerNick, info.static.carModel, info.static.track, validLaps)
			ac.log(json.dump(finished))
		else:
			lapInvalidated = False
			lastLapTime = lastLap
			ac.log("Last Lap was invalid")
			ac.setText(l_lastlaptime, "Last Lap: {}".format(formatDate(lastLapTime)))
			ac.setFontColor(l_lastlaptime, 1, 0, 0, 1)

# def acShutdown():
	# finished = {
	# 	"name": info.static.playerNick,
	# 	"car_model": info.static.carModel,
	# 	"track": info.static.track,
	# 	"laps": validLaps
	# }
	# ac.log(json.dumps(finished))
	# jsonVals = json.dumps(finished)
	# x = requests.post(requestsUrl, data={'intake_data': jsonVals})
	# ac.log('Response from server: {}'.format(x.status_code))

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

def onSendButtonPress():
	finished = {
		"name": info.static.playerNick,
		"car_model": info.static.carModel,
		"track": info.static.track,
		"laps": validLaps
	}
	ac.log(json.dumps(finished))
	jsonVals = json.dumps(finished)
	x = requests.post(requestsUrl, data={'intake_data': jsonVals})
	ac.log('Response from server: {}'.format(x.status_code))